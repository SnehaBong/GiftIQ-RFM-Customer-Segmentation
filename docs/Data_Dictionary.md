# Data Dictionary

## Sales.csv (fact table, one row per invoice line)

| Column | Type | Description |
|---|---|---|
| Invoice | Whole number | Invoice (order) number |
| StockCode | Text | Product code |
| Description | Text | Product name |
| Quantity | Whole number | Units bought (always > 0 after cleaning) |
| InvoiceDate | Date/time | When the order was placed |
| Price | Decimal | Unit price in GBP |
| Revenue | Decimal | Quantity × Price |
| Customer_ID | Whole number | Customer key, joins to `Customers` |
| Country | Text | Country the order was shipped to |

`OrderDate` (date only) is added in Power Query to join to `DateTable`.

## Customers.csv (dimension table, one row per customer)

| Column | Type | Description |
|---|---|---|
| Customer_ID | Whole number | Customer key |
| Recency | Whole number | Days between the last purchase and the snapshot date (10 Dec 2011) |
| Frequency | Whole number | Number of separate orders |
| Monetary | Decimal | Total amount spent |
| R_Score | 1–5 | Recency score (5 = bought most recently) |
| F_Score | 1–5 | Frequency score (5 = orders most often) |
| M_Score | 1–5 | Monetary score (5 = spends the most) |
| RFM_Score | Text | The three scores joined together, for example `545` |
| Segment | Text | Champions, Loyal, At Risk, New, Needs Attention or Lost |
| IsChurned | True/False | True if Recency > 90 days |

## Segment rules

Rules are checked from top to bottom. A customer gets the first segment that matches.

| Segment | Rule |
|---|---|
| Champions | R ≥ 4 and F ≥ 4 and M ≥ 4 |
| Loyal | R ≥ 3 and F ≥ 3 |
| At Risk | R ≤ 2 and F ≥ 3 |
| New | R ≥ 4 and F ≤ 2 |
| Needs Attention | R = 3 and F ≤ 2 |
| Lost | Everything else |
