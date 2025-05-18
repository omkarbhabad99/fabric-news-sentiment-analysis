```markdown
# Fabric News Sentiment Pipeline

An end-to-end Azure Data Engineering project using Microsoft Fabric. This solution ingests news articles from the Bing News Search API, processes raw JSON into a Delta lakehouse, applies sentiment analysis with SynapseML, and surfaces results in Power BI with Data Activator alerts.

---

## 📗 Table of Contents

1. [Project Overview](#project-overview)  
2. [Architecture](#architecture)  
3. [Prerequisites](#prerequisites)  
4. [Repository Structure](#repository-structure)  
5. [Configuration](#configuration)  
6. [Usage](#usage)  
   - [Raw JSON Processing Job](#raw-json-processing-job)  
   - [Sentiment Analysis Job](#sentiment-analysis-job)  
7. [Power BI Dashboard](#power-bi-dashboard)  
8. [Next Steps & Extensions](#next-steps--extensions)  

---

## 📝 Project Overview

This pipeline implements:

1. **Data Ingestion**  
   - Copy the latest news JSON from the **Bing News Search v7** API into OneLake using Fabric Data Factory.

2. **Data Transformation**  
   - Explode and flatten the JSON into a clean Delta table (`tbl_latest_news`) using Synapse Data Engineering with a Type 1 SCD pattern.

3. **Sentiment Analysis**  
   - Call a pre-trained sentiment model via **SynapseML** (`AnalyzeText`) to classify each article’s tone and write results to a new Delta table (`tbl_sentiment_analysis`).

4. **Reporting & Alerts**  
   - Build a Power BI dashboard on the sentiment table and configure **Data Activator** to send Teams alerts for negative sentiment spikes.

---

## 🏗 Architecture

<p align="center">
  <!-- Add your architecture diagram to docs/architecture.png -->
  ![Architecture Diagram](docs/architecture.png)
</p>

1. **Bing News API** → 2. **Data Factory** → raw JSON in OneLake  
3. **Synapse Data Engineering** → clean Delta table  
4. **Synapse Data Science (SynapseML)** → sentiment Delta table  
5. **Power BI** + **Data Activator** → Teams alerts  

---

## ⚙️ Prerequisites

- **Azure Subscription** with permission to create:
  - Resource Group  
  - **Bing Search v7** Cognitive Service (F1 free tier)  
- **Power BI Pro** or **Premium Per User (PPU)** license  
- **Fabric-enabled** workspace (via Power BI Service → Fabric view)  
- Python environment in your cluster with:
  - `pyspark`
  - `synapseml`  

---

## 📁 Repository Structure

```

.
├── README.md
├── spark\_job\_process\_raw\_json.py   # Raw JSON → clean Delta pipeline
├── sentiment\_analysis.py           # SynapseML-based sentiment job
└── docs/
├── architecture.png            # Architecture diagram placeholder
└── powerbi\_screenshot.png      # Power BI dashboard screenshot placeholder

````

---

## 🔧 Configuration

1. **Update your Cognitive Service credentials** in `sentiment_analysis.py` if running outside Fabric:
   ```python
   ENDPOINT = "https://<your-cogsvc-name>.cognitiveservices.azure.com/"
   KEY      = "<your-text-analytics-key>"
````

2. **Adjust table names** and **OneLake paths** in both scripts to match your environment:

   * Delta database: `bing_lake_db`
   * Raw JSON path: `Files/bing-latest-news.json`
   * Tables: `tbl_latest_news`, `tbl_sentiment_analysis`

---

## ▶️ Usage

### Raw JSON Processing Job

Transforms raw JSON articles into a clean Delta table:

```bash
spark-submit \
  spark_job_process_raw_json.py \
  Files/bing-latest-news.json \
  bing_lake_db.tbl_latest_news
```

* **Argument 1**: Input JSON path in OneLake
* **Argument 2**: Target Delta table

### Sentiment Analysis Job

Runs SynapseML sentiment analysis and writes/merges results:

```bash
spark-submit \
  sentiment_analysis.py \
  bing_lake_db.tbl_latest_news \
  bing_lake_db.tbl_sentiment_analysis
```

* **Argument 1**: Clean news Delta table
* **Argument 2**: Output sentiment Delta table

---

## 📊 Power BI Dashboard

<p align="center">
  <!-- Add your Power BI dashboard screenshot to docs/powerbi_screenshot.png -->
  ![Power BI Dashboard](docs/powerbi_screenshot.png)
</p>

* Connect to the **tbl\_sentiment\_analysis** table as a semantic model
* Build visuals for category counts, date trends, and sentiment breakdown
* Configure **Data Activator** alerts for negative sentiment via Teams

---

## 🚀 Next Steps & Extensions

* **Orchestration**: Schedule both jobs with Fabric Data Factory triggers (e.g. daily at 6 AM).
* **Alert tuning**: Refine threshold/rules in Data Activator for timely Teams notifications.
* **Type 2 SCD**: Extend transformation logic to capture historical changes.
* **Copilot & Private Link**: Upgrade to paid Fabric capacity to enable Copilot AI and secure VNet integration.

---

*Built with Microsoft Fabric — happy data engineering!*

```
```
