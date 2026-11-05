# Data

## processed/

| File | Description |
|---|---|
| `Customers.csv` | One row per customer with RFM values, scores, segment and churn flag |
| `Sales.zip` | Contains `Sales.csv`, one row per invoice line (about 74 MB unzipped, so it's zipped to stay under GitHub's file size limits) |

Unzip `Sales.zip` into this folder before loading the data into Power BI.

## raw/ (not in the repo)

The source file `EcommerceDashboardData.xlsx` (about 67 MB) is too large for GitHub. It holds the cleaned transactions from the [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) dataset (both yearly sheets combined, rows without a customer ID and cancelled orders removed).

To rebuild the processed files, put the file in `data/raw/` and run:

```bash
python scripts/prepare_powerbi_data.py
```
