# Plan des visuels Power BI

Page unique : **Churn Overview** (layout type dashboard)

## Row 1 — KPIs (cartes)

| Visuel | Champ |
|--------|-------|
| Carte | `Churn Rate %` (mesure) |
| Carte | `Total Customers` |
| Carte | `Churned Customers` |
| Carte | `Avg Credit Limit` |

## Row 2 — Répartition churn

| Visuel | Axis / Values |
|--------|----------------|
| Donut chart | Légende : `ChurnLabel` — Valeurs : `Total Customers` |
| Bar chart (horizontal) | Axe Y : `Card_Category` — Valeurs : `Churn Rate` |

## Row 3 — Profils à risque

| Visuel | Configuration |
|--------|----------------|
| Clustered bar | Axe : `Income_Category` — Valeurs : `Churn Rate` |
| Column chart | Axe : `Months_Inactive_12_mon` — Valeurs : `Churn Rate` — Moyenne par bucket si besoin |

## Row 4 — Activité & corrélation

| Visuel | Configuration |
|--------|----------------|
| Scatter | X : `Total_Trans_Ct` — Y : `Total_Trans_Amt` — Légende : `ChurnLabel` |
| Matrix / Table | Lignes : `Education_Level`, `Gender` — Valeurs : `Churn Rate`, `Total Customers` |

## Filtres (panneau latéral)

- Segment : `Card_Category`
- Segment : `Gender`
- Segment : `Marital_Status`

## Insights à mentionner (BeCode / présentation)

1. Churn ≈ **16 %** — classe minoritaire
2. Carte **Blue** — churn plus élevé
3. **Months_Inactive_12_mon** élevé → risque accru
4. Faible **Total_Trans_Amt** → signal de départ

Ces points doivent **correspondre** au notebook EDA et au dashboard Streamlit (comparaison DA vs ML).
