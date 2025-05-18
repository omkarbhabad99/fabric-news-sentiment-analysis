import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.utils import AnalysisException
from synapse.ml.cognitive import AnalyzeText

def main(input_table: str, output_table: str):
    # 1) Start Spark session
    spark = SparkSession.builder.appName("SynapseMLNewsSentiment").getOrCreate()

    # 2) Read your cleaned news Delta table
    df = spark.table(input_table)

    # 3) Configure the SynapseML sentiment model
    model = (
        AnalyzeText()
        .setTextCol("description")
        .setKind("SentimentAnalysis")
        .setOutputCol("response")
        .setErrorCol("error")
    )

    # 4) Apply the model
    result = model.transform(df)

    # 5) Extract the sentiment label and drop helper columns
    sentiment_df = result.withColumn("sentiment", col("response.documents.sentiment"))
    sentiment_df_final = sentiment_df.drop("response", "error")

    # 6) Write out to Delta, or merge if the table already exists
    try:
        sentiment_df_final.write.format("delta").saveAsTable(output_table)
        print(f"[INFO] Created new table {output_table}")
    except AnalysisException:
        print(f"[INFO] Table {output_table} exists, performing MERGE...")
        sentiment_df_final.createOrReplaceTempView("vw_sentiment")
        spark.sql(f"""
            MERGE INTO {output_table} AS target
            USING vw_sentiment       AS source
              ON source.url = target.url
            WHEN MATCHED AND source.sentiment <> target.sentiment
              THEN UPDATE SET target.sentiment = source.sentiment
            WHEN NOT MATCHED
              THEN INSERT *
        """)

    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: sentiment_analysis.py <input_delta_table> <output_delta_table>", file=sys.stderr)
        sys.exit(1)

    input_tbl  = sys.argv[1]  
    output_tbl = sys.argv[2]  
    main(input_tbl, output_tbl)
