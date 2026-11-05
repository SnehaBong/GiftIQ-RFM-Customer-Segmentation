"""
GiftIQ RFM Customer Segmentation - data prep for Power BI.

Reads the cleaned transaction export, recalculates RFM scores (with the
F_Score direction fixed and the 'Needs Attention' segment added), and writes
two CSV files for a star-schema model in Power BI:

    Sales.csv      one row per invoice line   (fact table)
    Customers.csv  one row per customer       (dimension table)

Usage:
    python scripts/prepare_powerbi_data.py [path/to/EcommerceDashboardData.xlsx]
"""
import sys
from pathlib import Path

import pandas as pd

repo_root = Path(__file__).resolve().parents[1]
src = Path(sys.argv[1]) if len(sys.argv) > 1 else repo_root / "data" / "raw" / "EcommerceDashboardData.xlsx"
out_dir = repo_root / "data" / "processed"
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(src)

# 1. Keep valid sales lines only
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]
df = df.drop_duplicates(["Invoice", "StockCode", "Quantity", "InvoiceDate", "Price", "Customer_ID"])
df["Revenue"] = (df["Quantity"] * df["Price"]).round(2)

# 2. RFM per customer
snapshot_date = df["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)

rfm = df.groupby("Customer_ID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
    Frequency=("Invoice", "nunique"),
    Monetary=("Revenue", "sum"),
).reset_index()

# Low recency is good -> 5; high frequency / monetary is good -> 5
rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)


def segment_customer(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "Champions"
    elif row["R_Score"] >= 3 and row["F_Score"] >= 3:
        return "Loyal"
    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"
    elif row["R_Score"] >= 4 and row["F_Score"] <= 2:
        return "New"
    elif row["R_Score"] == 3 and row["F_Score"] <= 2:
        return "Needs Attention"
    else:
        return "Lost"


rfm["Segment"] = rfm.apply(segment_customer, axis=1)
rfm["IsChurned"] = rfm["Recency"] > 90
rfm["Monetary"] = rfm["Monetary"].round(2)

# 3. Write the two tables
sales_cols = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate",
              "Price", "Revenue", "Customer_ID", "Country"]
df[sales_cols].to_csv(out_dir / "Sales.csv", index=False)
rfm.to_csv(out_dir / "Customers.csv", index=False)

print(f"Sales.csv:     {len(df):,} rows")
print(f"Customers.csv: {len(rfm):,} customers")
print(f"Total revenue: {df['Revenue'].sum():,.0f}")
print(rfm["Segment"].value_counts().to_string())
