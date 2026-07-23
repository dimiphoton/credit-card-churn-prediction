# Comparaison des dashboards — Streamlit vs Power BI vs Tableau

Tous les outils consomment le **même pipeline ML Python** :

```text
bank_data.csv → run_training.py → modèles .pkl
                      ↓
         export_for_powerbi.py → CSV avec ChurnProbability + ML_Cluster
                      ↓
        ┌─────────────┼─────────────┐
   Streamlit      Power BI       Tableau
   (live API)     (Desktop)      (Public)
```

## Colonnes ML dans les exports BI

| Colonne | Source |
|---------|--------|
| `ChurnProbability` | Random Forest `predict_proba` |
| `PredictedChurn` | Seuil 0.5 |
| `RiskLevel` | low / medium / high |
| `ML_Cluster` | KMeans + silhouette |
| `PredictionMatch` | Modèle vs `IsChurn` réel |

## Rôles BeCode

| Rôle | Outil | Livrable |
|------|-------|----------|
| ML Engineer | Python `src/churn/` | Modèle + clusters |
| Data Analyst | Power BI + Tableau | Dashboards KPI + comparaison segments |
| Data Engineer | Streamlit + FastAPI + Render | App déployée intégrée au modèle |

## Ce n'est PAS une exclusion du ML

Power BI et Tableau ne ré-entraînent pas le modèle — ils **visualisent les scores exportés**.
C'est le pattern standard en entreprise : ML en Python, BI pour le business.
