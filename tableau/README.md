# Tableau — Credit Card Churn (avec ML)

Dashboard Tableau connecté aux **mêmes prédictions ML** que Streamlit et Power BI.

## Fichier de données

Importe : [`data/bank_churn_tableau.csv`](data/bank_churn_tableau.csv)

Colonnes ML incluses :

| Colonne | Description |
|---------|-------------|
| `ChurnProbability` | Score 0–1 du modèle Random Forest |
| `PredictedChurn` | 1 = risque churn prédit |
| `RiskLevel` | low / medium / high |
| `ML_Cluster` | Segment KMeans (comparer avec churn réel) |
| `PredictionMatch` | Correct / Incorrect vs `IsChurn` |
| `IsChurn` | Vérité terrain (1 = parti) |

> Générer les fichiers : `python scripts/run_training.py` puis `python scripts/export_for_powerbi.py`

## Étape 1 — Installer Tableau Public (gratuit)

https://public.tableau.com/app/discover

Ou **Tableau Desktop** (trial / licence école BeCode).

## Étape 2 — Connexion

1. **Connecter** → **Fichier texte** → `tableau/data/bank_churn_tableau.csv`
2. Feuille **Source de données** → vérifier types (nombres / textes)

## Étape 3 — Champs calculés

Crée les champs dans **Colonne** → **Créer un champ calculé** :

```
Churn Rate
SUM([IsChurn]) / COUNT([CLIENTNUM])

High Risk Count
SUM(IF [RiskLevel] = "high" THEN 1 ELSE 0 END)

Model Accuracy
SUM(IF [PredictionMatch] = "Correct" THEN 1 ELSE 0 END) / COUNT([CLIENTNUM])
```

Plus de formules : [`calculated_fields.md`](calculated_fields.md)

## Étape 4 — Visuels

Plan détaillé : [`VISUALS.md`](VISUALS.md)

Minimum BeCode (EDA + ML + comparaison clustering) :

1. **KPI** — Churn Rate, High Risk Count, Model Accuracy
2. **Barres** — Churn Rate par `Card_Category`
3. **Scatter** — `ChurnProbability` vs `Total_Trans_Amt`, couleur `IsChurn`
4. **Heatmap** — `ML_Cluster` × `Card_Category`, couleur Churn Rate
5. **Tableau** — profils par `ML_Cluster` (avg age, avg transactions, churn rate)

## Étape 5 — Publier

1. **Server** → **Tableau Public** → enregistrer sur ton compte
2. Copie l’URL publique → ajoute-la dans le README principal

## Comparaison ML : Tableau vs Streamlit vs Power BI

| | Streamlit | Power BI | Tableau |
|---|-----------|----------|---------|
| ML scores | ✅ live API | ✅ colonnes CSV | ✅ colonnes CSV |
| Clustering | ✅ KMeans | ✅ ML_Cluster | ✅ ML_Cluster |
| Prédiction 1 client | ✅ formulaire | ⚠️ scatter/filtres | ⚠️ tooltip |
| Déploiement | Render | powerbi.com | Tableau Public |

Les trois outils lisent le **même modèle** exporté depuis Python — c’est la comparaison demandée par BeCode (DA vs ML).
