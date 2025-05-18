# Fabric News Sentiment Pipeline

> _Ingest Bing news into OneLake, transform to Delta, analyze sentiment with SynapseML, and visualize in Power BI._

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

---

## 📝 Project Overview

This end-to-end pipeline:

- Pulls the latest news articles from the **Bing News Search v7** API  
- Copies raw JSON into **OneLake** via **Fabric Data Factory**  
- Transforms and flattens JSON into a clean **Delta table** using **Synapse Data Engineering**  
- Runs sentiment analysis on article descriptions with **SynapseML**  
- Writes results to a Delta table for reporting  
- Builds a **Power BI** dashboard and configures **Data Activator** alerts to Teams  

---

## 🏗 Architecture

<img width="1470" alt="Screenshot 2025-05-18 at 11 32 24 AM" src="https://github.com/user-attachments/assets/66e8d13f-f58e-4fd1-b918-e771b8abed08" />



```text
1. Bing News API → Data Factory → raw JSON in OneLake  
2. Synapse Data Engineering → clean Delta table (tbl_latest_news)  
3. Synapse Data Science (SynapseML) → sentiment Delta table (tbl_sentiment_analysis)  
4. Power BI + Data Activator → Teams alerts
```

## Power BI Dashboard
<img width="1470" alt="Screenshot 2025-05-18 at 11 17 21 AM" src="https://github.com/user-attachments/assets/79f9f039-e21d-4f33-9bbf-4c8a5cfeac00" />

