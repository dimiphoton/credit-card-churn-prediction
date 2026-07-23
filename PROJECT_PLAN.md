# Plan de projet — Credit Card Churn Prediction

> Projet BeCode (consolidation) — pipeline complet DE / ML / DA, déployé sur Render.

## Stack retenue

| Composant | Choix | Justification |
|-----------|-------|---------------|
| API prédiction | **FastAPI** | Typage simple, doc auto `/docs`, Docker + Render |
| Dashboard | **Streamlit** | 100 % Python, KPIs + EDA + résultats modèle |
| Base de données | **SQLite** | ~10k lignes, fichier local, simple en Docker |
| ML | **scikit-learn + imbalanced-learn** | Explicable, SMOTE pour churn déséquilibré (~16 %) |
| Code | **`src/churn/`** | Library réutilisable par API, tests et dashboard |
| Git | **Feature branches → PR → main** | Historique propre, une branche par étape |
| Déploiement | **Render.com** | Compte lié à GitHub (`dimiphoton`) |

## Architecture

```text
bank_data.csv  →  ingest  →  churn.db (SQLite)
                                ↓
                         cleaning → features → train (classif + clustering)
                                ↓                    ↓
                          Streamlit dashboard    FastAPI /predict
```

## Structure cible

```text
credit-card-churn-prediction/
├── src/churn/              # library métier
│   ├── config.py
│   ├── ingest.py
│   ├── cleaning.py
│   ├── features.py
│   ├── train.py
│   ├── clustering.py
│   └── predict.py
├── app/
│   ├── api/main.py         # FastAPI
│   └── dashboard/app.py    # Streamlit
├── tests/
├── notebooks/01_eda.ipynb
├── data/
│   ├── raw_data/bank_data.csv
│   └── processed/churn.db  # généré, gitignored
├── models/                 # gitignored
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── CRITERIA.md
├── PROJECT_PLAN.md
└── README.md
```

## Branches et livrables

| # | Branche | Contenu | Critère BeCode couvert |
|---|---------|---------|------------------------|
| 1 | `feature/01-scaffold` | Structure, config, requirements, stubs API/dashboard | Code propre sur GitHub |
| 2 | `feature/02-database` | Schéma SQLite, ingestion CSV → DB | Pipeline data storage (DE) |
| 3 | `feature/03-eda` | Notebook EDA (KPIs, distributions, corrélations) | EDA réalisée |
| 4 | `feature/04-preprocessing` | Nettoyage, encodage, split train/test | Data cleaned & preprocessed |
| 5 | `feature/05-ml-models` | Classification (LR/RF + SMOTE) + KMeans (elbow/silhouette) | Modèles + clustering |
| 6 | `feature/06-tests` | pytest (import, clean, features, train, predict) | Code testé |
| 7 | `feature/07-fastapi-docker` | API `/predict`, `/health`, Dockerfile, docker-compose | App Docker (DE) |
| 8 | `feature/08-streamlit` | Dashboard KPIs, profils clients, intégration modèle | Dashboard déployé |
| 9 | `feature/09-deploy-docs` | README Deliverables, `render.yaml`, limitations | Render + doc finale |

Chaque branche = **1 PR** vers `main`. `main` reste stable après chaque merge.

## ML — choix techniques

### Classification (churn)

- **Cible** : `Attrition_Flag` → binaire (Existing / Attrited Customer)
- **Modèles** : Logistic Regression (baseline) + Random Forest (performance)
- **Déséquilibre** : SMOTE via `imbalanced-learn`
- **Métriques** : recall, F1, ROC-AUC (recall prioritaire — coût de rater un churner)
- **Exclusions** : colonnes Naive Bayes (fuite de données), index CSV

### Clustering (segments clients)

- **Algorithme** : KMeans sur features normalisées
- **K optimal** : méthode coude + silhouette score
- **Livrable** : description des clusters + profils types (DA + ML)

## Déploiement Render

Compte Render lié à GitHub. Déploiement prévu en fin de projet (`feature/09-deploy-docs`) :

| Service Render | Source | Port |
|----------------|--------|------|
| **Web Service** | `app/api/main.py` (FastAPI + uvicorn) | 8000 |
| **Web Service** | `app/dashboard/app.py` (Streamlit) | 8501 |

Fichier `render.yaml` (Blueprint) pour déclarer les 2 services + variables d'environnement.

## README final (format Deliverables BeCode)

1. Description du projet et contexte métier
2. Installation (venv, `pip install -r requirements.txt`)
3. Usage (pipeline, API, dashboard, Docker)
4. Visuals (captures dashboard / métriques)
5. Résultats et **limitations** des modèles
6. Déploiement Render (URLs)
7. Timeline / situation personnelle

## Note Tableau

Le brief BeCode mentionne Tableau pour comparer le clustering. En solo, la comparaison ML vs analyse descriptive sera intégrée dans le **dashboard Streamlit** (section dédiée). Option Tableau possible en complément si besoin.

## Présentation client (hors repo)

Présentation business 10 min : churn rate, segments, recommandations marketing, limites du modèle.
