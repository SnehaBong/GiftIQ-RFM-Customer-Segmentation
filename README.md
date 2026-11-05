<p align="center">
  <img src="assets/GiftIQ_Logo.png" alt="GiftIQ logo" width="260">
</p>

<h1 align="center">GiftIQ – RFM Customer Segmentation</h1>

<p align="center">
  Customer segmentation and churn analysis for an online gift retailer, using <b>Python</b> and <b>Power BI</b>.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-Pandas-5B2A86">
  <img alt="Power BI" src="https://img.shields.io/badge/Power%20BI-DAX-F2A541">
  <img alt="Data" src="https://img.shields.io/badge/Data-779K%20transactions-5B2A86">
</p>

---

## Business problem

An online gift retailer sells to thousands of customers but treats them all the same. The business wants to know:

1. **Who are our most valuable customers?**
2. **Which good customers are about to leave?**
3. **When does revenue come in, and from where?**

This project answers those questions with an **RFM (Recency, Frequency, Monetary)** model and an interactive 3-page Power BI dashboard.

## Key insights

| | Insight |
|---|---|
| 👑 | **Champions are 22% of customers but bring in 68% of revenue** ($11.8M of $17.4M). |
| ⚠️ | **$1.79M is at risk.** 1,208 At Risk customers have stopped buying recently. |
| 📉 | **50.86% of customers have churned** (no purchase in 90+ days). |
| 🎁 | **Q4 brings in 35% of yearly revenue.** Sales climb from September and peak in November. |
| 🌍 | **83% of revenue comes from the UK**, which leaves room to grow abroad. |

### Recommendations
- **Champions:** loyalty perks and early access to new collections.
- **At Risk:** personalised win-back offers before the Q4 gift season.
- **New:** a welcome series that pushes a second purchase.
- **Lost:** low-cost reactivation emails only.

## Dataset

- **Source:** [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii), transactions from a UK-based online gift retailer
- **Period:** December 2009 to December 2011
- **Size after cleaning:** 779,495 invoice lines · 36,975 orders · 5,881 customers · 41 countries · $17.37M revenue

## Tools and Tech Stack

| Tool | Used for |
|---|---|
|SQL Server / SSMS | Data import, cleaning, deduplication, and exploratory querying on the full 1M+ row dataset
| Python (Pandas, Matplotlib) | Cleaning, RFM calculation, scoring, segmentation and churn flagging |
| Jupyter Notebook | Interactive development environment for the Python analysis |
| Power BI Desktop| Three page interactive dashboard: executive summary and RFM deep dive |
| DAX | Measures for customer counts, revenue totals, and average customer value |

## Core Concepts Demonstrated

```
RFM Analysis — scoring customers on Recency, Frequency, and Monetary value to quantify customer worth on a comparable scale
Customer Segmentation — translating raw RFM scores into business meaningful groups (Champions, Loyal, At Risk, New, Needs Attention, Lost)
Churn Definition and Flagging — applying a fixed inactivity threshold to identify customers at risk of lapsing
Data Quality Handling — resolving mixed date formats, invalid type conversions, and duplicate detection using SQL window functions
Dimensional Modeling for BI — structuring a single unified table so multiple report pages can share one clean source without manual relationships
Interactive BI Design — slicers, bookmark based toggles, and a multi page navigation structure inside Power BI

```
## Project Workflow

Step 1 — Business Requirements Document. Defined scope, business questions, key definitions, and success criteria before any data work began.

Step 2 — SQL, Data Cleaning and Exploration. Imported both raw sheets into SQL Server, corrected data types, resolved a mixed date format issue affecting over half the dataset, removed 32,907 exact duplicate rows, and validated row counts at every step against the published UCI total.

Step 3 — Python, RFM Segmentation. Loaded the cleaned data into pandas, calculated Recency, Frequency, and Monetary value per customer, scored each customer on a 1 to 5 scale per dimension, and assigned each of the 5,881 customers to one of six segments. Added a 90 day churn flag.

Step 4 — Power BI, Dashboard Build. Merged the segmentation results back onto transaction level data to create a single analysis ready table, then built a three page report.
```
## How to run

Download the Online Retail II dataset from the UCI Machine Learning Repository

1. Run the SQL scripts in `01_sql` in order to recreate the cleaned `RetailCleaned` table
2. Export `RetailCleaned` to CSV and run the notebook in `02_python` to generate the segmented dataset
3. Open the Power BI file in `03_powerbi` and point it to the exported Excel file to refresh

## What I learned

- Building an RFM model from raw transactions, and why scoring direction matters. An early version scored Frequency backwards and found only 26 Champions instead of 1,291.
- Why a star schema matters: scores stored once per customer don't get double-counted across purchase rows.
- Writing DAX with `DISTINCTCOUNT`, `CALCULATE`, `DIVIDE`, `AVERAGEX` and `SUMMARIZE`, and using field parameters for interactive toggles.
- Designing a consistent visual identity: theme, logo and backgrounds.

## Author

**Sneha Bose** · [GitHub](https://github.com/SnehaBong)
