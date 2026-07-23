# Credit Card Churn Prediction

Projet BeCode — prédiction et segmentation du churn client pour une institution financière.

Pipeline data complet : **SQLite → EDA → preprocessing → ML → API FastAPI → dashboard Streamlit**, déployable sur **Render** via Docker.

---

## Description

Une banque observe un taux de churn supérieur à **16 %** sur ses porteurs de cartes de crédit. L'équipe marketing a besoin d'outils pour :

1. **Identifier** les clients à risque de résiliation
2. **Segmenter** la base en groupes homogènes
3. **Prioriser** les actions de rétention

Ce dépôt implémente les trois rôles du brief BeCode (Data Engineer, ML Engineer, Data Analyst) dans un pipeline intégré.

| Composant | Rôle | Technologie |
|-----------|------|-------------|
| Ingestion | Stockage structuré | SQLite + pandas |
| EDA | Exploration & KPIs | Jupyter + notebook `01_eda.ipynb` |
| Preprocessing | Nettoyage & encodage | `src/churn/cleaning.py`, `features.py` |
| Classification | Prédiction churn | scikit-learn + SMOTE |
| Clustering | Segments clients | KMeans (silhouette) |
| API | Scoring temps réel | FastAPI |
| Dashboard | KPIs & profils | Streamlit |

Documents complémentaires : [`CRITERIA.md`](CRITERIA.md) · [`PROJECT_PLAN.md`](PROJECT_PLAN.md)

---

## Installation

**Prérequis** : Python 3.10+

```bash
git clone https://github.com/dimiphoton/credit-card-churn-prediction.git
cd credit-card-churn-prediction

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Usage

### Étape 1 — Entraîner le pipeline

Importe le CSV en base SQLite, entraîne le classifieur et le clustering, sauvegarde les modèles dans `models/`.

```bash
python scripts/run_training.py
```

**Artefacts générés :**

- `data/processed/churn.db`
- `models/classifier.pkl`
- `models/clustering.pkl`
- `models/metrics.json`

### Étape 2 — API FastAPI

```bash
# Windows
set PYTHONPATH=src

# Linux / macOS
export PYTHONPATH=src

uvicorn app.api.main:app --reload --port 8000
```

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Santé de l'API |
| `GET /ready` | Modèle chargé |
| `GET /metrics` | Métriques ML (recall, F1, ROC-AUC) |
| `POST /predict` | Prédiction churn |
| `GET /docs` | Documentation Swagger |

**Exemple de prédiction :**

```bash
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Customer_Age\":45,\"Gender\":\"M\",\"Dependent_count\":3,\"Education_Level\":\"High School\",\"Marital_Status\":\"Married\",\"Income_Category\":\"$60K - $80K\",\"Card_Category\":\"Blue\",\"Months_on_book\":39,\"Total_Relationship_Count\":5,\"Months_Inactive_12_mon\":1,\"Contacts_Count_12_mon\":3,\"Credit_Limit\":12691,\"Total_Revolving_Bal\":777,\"Avg_Open_To_Buy\":11914,\"Total_Amt_Chng_Q4_Q1\":1.335,\"Total_Trans_Amt\":1144,\"Total_Trans_Ct\":42,\"Total_Ct_Chng_Q4_Q1\":1.625,\"Avg_Utilization_Ratio\":0.061}"
```

### Étape 3 — Dashboard Streamlit

```bash
streamlit run app/dashboard/app.py
```

Ouvrir http://localhost:8501 — onglets : Exploration, Modèle ML, Segments clients, Prédiction.

### Étape 4 — Docker

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Dashboard | http://localhost:8501 |

### Étape 5 — Tests

```bash
pytest
```

31 tests : ingestion, preprocessing, ML, API, pipeline complet.

---

## Visuals

- **Notebook EDA** (`notebooks/01_eda.ipynb`) — taux de churn, distributions, corrélations
- **Dashboard Streamlit** — KPIs, segments KMeans, formulaire de prédiction
- **API `/metrics`** — comparaison Logistic Regression vs Random Forest

---

## Résultats & choix du modèle

### Classification

- **Cible** : `Attrition_Flag` → binaire (churn = 1)
- **Modèles testés** : Logistic Regression (baseline) + Random Forest
- **Déséquilibre** : SMOTE sur le jeu d'entraînement
- **Sélection** : meilleur **recall** sur le test set (priorité métier : ne pas rater un client qui part)
- **Métriques suivies** : recall, F1, ROC-AUC

### Clustering

- **Algorithme** : KMeans sur features normalisées
- **K optimal** : score de silhouette (K de 2 à 8)
- **Livrable** : profils par cluster (taille, churn rate, âge moyen, transactions)

### Limitations

- Données historiques statiques — pas de variables macro-économiques ni concurrence
- Label encoding sur les catégorielles (pas de one-hot)
- Recall élevé → davantage de faux positifs (campagnes marketing ciblées plus larges)
- Réentraînement périodique recommandé en production

---

## Déploiement Render

Compte Render lié au GitHub `dimiphoton`. Fichier [`render.yaml`](render.yaml) :

1. Render Dashboard → **New Blueprint**
2. Sélectionner ce dépôt
3. Deux services créés :
   - `churn-api` — FastAPI (`uvicorn`)
   - `churn-dashboard` — Streamlit

Variable d'environnement : `PYTHONPATH=src`

Le build exécute `python scripts/run_training.py` avant le démarrage.

---

## Structure du projet

```text
credit-card-churn-prediction/
├── src/churn/              # Library métier
│   ├── ingest.py           # CSV → SQLite
│   ├── cleaning.py         # Nettoyage
│   ├── features.py         # Encodage + split
│   ├── train.py            # Classification + SMOTE
│   ├── clustering.py       # KMeans
│   └── predict.py          # Inférence
├── app/
│   ├── api/main.py         # FastAPI
│   └── dashboard/app.py    # Streamlit
├── tests/                  # pytest (31 tests)
├── notebooks/01_eda.ipynb
├── scripts/run_training.py
├── data/raw_data/bank_data.csv
├── Dockerfile
├── docker-compose.yml
└── render.yaml
```

---

## Workflow Git

Développement par **feature branches** avec merge sur `main` à chaque étape :

`feature/01-scaffold` → `02-database` → `03-eda` → `04-preprocessing` → `05-ml-models` → `06-tests` → `07-fastapi-docker` → `08-streamlit` → `09-deploy-docs`

---

## Contributors

- **Dimitri Marchand** ([@dimiphoton](https://github.com/dimiphoton)) — Data Engineering, ML, Dashboard, Déploiement

---

## Timeline

| Phase | Branche | Statut |
|-------|---------|--------|
| Reset baseline | main | ✅ |
| Scaffold | feature/01-scaffold | ✅ |
| SQLite | feature/02-database | ✅ |
| EDA | feature/03-eda | ✅ |
| Preprocessing | feature/04-preprocessing | ✅ |
| ML | feature/05-ml-models | ✅ |
| Tests | feature/06-tests | ✅ |
| API + Docker | feature/07-fastapi-docker | ✅ |
| Dashboard | feature/08-streamlit | ✅ |
| Docs + Render | feature/09-deploy-docs | ✅ |

---

## Personal situation

Projet solo réalisé dans le cadre du challenge BeCode **Churn Prediction** (consolidation).
Approche professionnelle : branches par étape, tests automatisés, déploiement Render.

Dataset : [Credit Card Customers (Kaggle)](https://www.kaggle.com/sakshigoyal7/credit-card-customers)
