# Visuels Tableau — EDA + ML + clustering

## Page : Churn & ML Overview

### Row 1 — KPIs

| Visuel | Champ |
|--------|-------|
| Texte / BAN | `Churn Rate` |
| BAN | `COUNT(CLIENTNUM)` |
| BAN | `High Risk Count` |
| BAN | `Model Accuracy` |

### Row 2 — EDA classique

| Visuel | Config |
|--------|--------|
| Barres | `Card_Category` / Churn Rate |
| Camembert | `ChurnLabel` / COUNT |

### Row 3 — ML classification

| Visuel | Config |
|--------|--------|
| Histogramme | `ChurnProbability` (bins), couleur `IsChurn` |
| Barres empilées | `RiskLevel` / COUNT, couleur `PredictedChurn` |
| Matrice | Lignes `IsChurn`, colonnes `PredictedChurn` — comparaison modèle vs réalité |

### Row 4 — ML clustering (critère BeCode)

| Visuel | Config |
|--------|--------|
| Barres | `ML_Cluster` / Churn Rate moyen |
| Tableau croisé | Lignes `ML_Cluster`, colonnes `Card_Category`, valeurs Churn Rate |
| Scatter | X `Total_Trans_Amt`, Y `Customer_Age`, détail `ML_Cluster`, couleur `IsChurn` |

### Filtres

- `Gender`
- `Income_Category`
- `RiskLevel`

## Question BeCode à répondre dans ta présentation

> « Est-ce que les segments Tableau/Power BI ressemblent aux clusters du ML engineer ? »

Compare visuellement **ML_Cluster** (KMeans Python) avec une segmentation manuelle par `Income_Category` + `Card_Category` dans Tableau.
