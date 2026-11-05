# DAX Measures

All measures live in a `_Measures` table in the Power BI model.

## Model

| From (one) | To (many) | Direction |
|---|---|---|
| `Customers[Customer_ID]` | `Sales[Customer_ID]` | Single |
| `DateTable[Date]` | `Sales[OrderDate]` | Single |

## Date table

```dax
DateTable =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2009, 12, 1 ), DATE ( 2011, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Quarter", "Qtr " & QUARTER ( [Date] ),
    "Month", FORMAT ( [Date], "MMMM" ),
    "Month No", MONTH ( [Date] )
)
```

`Month` is sorted by `Month No`. The table is marked as a date table.

## KPI measures

```dax
Total Revenue = SUM ( Sales[Revenue] )

Total Customers = DISTINCTCOUNT ( Sales[Customer_ID] )

Total Orders = DISTINCTCOUNT ( Sales[Invoice] )

Avg Customer Value = DIVIDE ( [Total Revenue], [Total Customers] )

Churned Customers =
CALCULATE ( [Total Customers], Customers[IsChurned] = TRUE () )

Churned % = DIVIDE ( [Churned Customers], [Total Customers] )
```

## RFM score averages

Each customer is counted once, however many purchase rows they have.

```dax
Avg R Score =
AVERAGEX (
    SUMMARIZE ( Sales, Customers[Customer_ID], Customers[R_Score] ),
    Customers[R_Score]
)

Avg F Score =
AVERAGEX (
    SUMMARIZE ( Sales, Customers[Customer_ID], Customers[F_Score] ),
    Customers[F_Score]
)

Avg M Score =
AVERAGEX (
    SUMMARIZE ( Sales, Customers[Customer_ID], Customers[M_Score] ),
    Customers[M_Score]
)
```

## Insight measures

```dax
Champions Revenue % =
DIVIDE (
    CALCULATE ( [Total Revenue], Customers[Segment] = "Champions" ),
    [Total Revenue]
)

Revenue at Risk =
CALCULATE ( [Total Revenue], Customers[Segment] = "At Risk" )
```

## Calculated column

```dax
Status = IF ( Customers[IsChurned], "Churned", "Active" )
```

## Field parameters

| Parameter | Fields | Used by |
|---|---|---|
| Metric Selector | `[Total Revenue]`, `[Total Customers]` | Retention by Segment chart |
| View By | `Customers[Segment]`, `Sales[Country]` | Avg Customer Value chart |

## Expected values (no filters)

| Measure | Value |
|---|---:|
| Total Customers | 5,878 |
| Total Revenue | $17.37M |
| Avg Customer Value | $2,956 |
| Churned % | 50.9% |
| Champions Revenue % | 68.1% |
| Revenue at Risk | $1.59M |
