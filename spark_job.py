import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, to_date, date_format
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.utils import AnalysisException

def main(input_json_path, delta_table):
    # 1) Start Spark
    spark = SparkSession.builder.appName("BingNewsPipeline").getOrCreate()

    # 2) Ingest raw JSON
    df = spark.read.option("multiline", "true") \
                   .json(input_json_path)

    # 3) Explode the "value" array into one row per article
    df_exploded = df.select( explode(df["value"]).alias("json_object") )

    # 4) Convert each row to a Python JSON string
    json_list = df_exploded.toJSON().collect()

    # 5) Pull out fields into Python lists
    title = []; description = []; category = []; url = []
    image = []; provider = []; datePublished = []
    for js in json_list:
        try:
            obj = json.loads(js)["json_object"]
            title.append(obj.get("name"))
            description.append(obj.get("description"))
            category.append(obj.get("category"))
            url.append(obj.get("url"))
            image.append(obj["image"]["thumbnail"]["contentUrl"])
            provider.append(obj["provider"][0]["name"])
            datePublished.append(obj.get("datePublished"))
        except Exception as e:
            # skip malformed articles
            print(f"[WARN] skipping record: {e}", file=sys.stderr)

    # 6) Zip into rows + define schema
    rows = list(zip(title,description,category,url,image,provider,datePublished))
    schema = StructType([
        StructField("title",        StringType(), True),
        StructField("description",  StringType(), True),
        StructField("category",     StringType(), True),
        StructField("url",          StringType(), True),
        StructField("image",        StringType(), True),
        StructField("provider",     StringType(), True),
        StructField("datePublished",StringType(), True)
    ])

    # 7) Build DataFrame & format date
    df_cleaned = spark.createDataFrame(rows, schema=schema) \
                      .withColumn("datePublished",
                                  date_format(to_date("datePublished"), "dd-MMM-yyyy"))

    # 8) Write or merge into Delta table
    try:
        df_cleaned.write.format("delta").saveAsTable(delta_table)
        print(f"[INFO] created new table: {delta_table}")
    except AnalysisException:
        print(f"[INFO] table exists, doing MERGE INTO {delta_table}")
        df_cleaned.createOrReplaceTempView("vw_cleaned")
        spark.sql(f"""
            MERGE INTO {delta_table} AS target
            USING vw_cleaned            AS src
              ON src.url = target.url
            WHEN MATCHED AND (
                 src.title           <> target.title
              OR src.description     <> target.description
              OR src.category        <> target.category
              OR src.image           <> target.image
              OR src.provider        <> target.provider
              OR src.datePublished   <> target.datePublished
            )
              THEN UPDATE SET *
            WHEN NOT MATCHED
              THEN INSERT *
        """)

    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: bing_news_pipeline.py <input_json_path> <delta_table>", file=sys.stderr)
        sys.exit(1)

    input_path  = sys.argv[1]   
    target_table = sys.argv[2]  
    main(input_path, target_table)
