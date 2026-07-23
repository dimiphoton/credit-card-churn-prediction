# Champs calculés Tableau

```
// Taux de churn global
Churn Rate
SUM([IsChurn]) / COUNT([CLIENTNUM])

// Clients à haut risque (modèle ML)
High Risk Count
SUM(IF [RiskLevel] = "high" THEN 1 ELSE 0 END)

// Précision du modèle sur tout le dataset
Model Accuracy
SUM(IF [PredictionMatch] = "Correct" THEN 1 ELSE 0 END) / COUNT([CLIENTNUM])

// Churn rate par cluster ML
Cluster Churn Rate
{ FIXED [ML_Cluster] : SUM([IsChurn]) / COUNT([CLIENTNUM]) }

// Probabilité moyenne par segment
Avg Churn Probability
AVG([ChurnProbability])
```
