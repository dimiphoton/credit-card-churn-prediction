# Credit Card Churn Prediction

Projet BeCode — prédiction du churn client pour une institution financière.
Pipeline complet : ingestion SQLite, EDA, preprocessing, ML (classification + clustering), API FastAPI, dashboard Streamlit.

## Description

Une banque souhaite identifier les clients à risque de fermer leur compte carte de crédit (churn ~16 %).
Ce projet fournit :

- Une **base SQLite** alimentée depuis le dataset Kaggle
- Un **modèle ML** (Random Forest / Logistic Regression + SMOTE) pour scorer le risque de churn
- Un **clustering KMeans** pour segmenter les clients
- Une **API REST** (`/predict`) pour l'équipe marketing
- Un **dashboard Streamlit** avec KPIs, métriques et profils clients

Voir aussi [`CRITERIA.md`](CRITERIA.md) (brief BeCode) et [`PROJECT_PLAN.md`](PROJECT_PLAN.md) (plan technique).

## Installation

```bash
git clone https://github.com/dimiphoton/credit-card-churn-prediction.git
cd credit-card-churn-prediction

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

### 1. Entraîner le pipeline ML

```bash
python scripts/run_training.py
```

Génère : `data/processed/churn.db`, modèles dans `models/`.

### 2. Lancer l'API FastAPI

```bash
set PYTHONPATH=src
uvicorn app.api.main:app --reload --port 8000
```

- Health : http://localhost:8000/health
- Swagger : http://localhost:8000/docs
- Prédiction : `POST /predict`

### 3. Lancer le dashboard Streamlit

```bash
set PYTHONPATH=src
streamlit run app/dashboard/app.py
```

→ http://localhost:8501

### 4. Docker

```bash
docker compose up --build
```

- API : http://localhost:8000
- Dashboard : http://localhost:8501

### 5. Tests

```bash
pytest
```

## Visuals

| Composant | Contenu |
|-----------|---------|
| Notebook `notebooks/01_eda.ipynb` | KPIs churn, distributions, corrélations |
| Dashboard Streamlit | KPIs live, segments, prédiction interactive |
| API `/metrics` | Recall, F1, ROC-AUC du modèle retenu |

## Résultats et limitations

### Modèle

- **Cible** : `Attrition_Flag` (binaire)
- **Techniques** : SMOTE (déséquilibre classes), comparaison LR vs RF
- **Métrique prioritaire** : **Recall** (ne pas rater un client qui part)
- **Clustering** : KMeans, K optimal via silhouette score

### Limitations

- Données historiques uniquement — pas de variables macro-économiques
- Label encoding sur catégorielles (ordre non métier)
- Recall élevé → plus de faux positifs (coût marketing)
- Modèle statique — réentraînement périodique recommandé

## Déploiement Render

Compte Render lié à GitHub. Déploiement via Blueprint [`render.yaml`](render.yaml) :

1. Render Dashboard → **New Blueprint** → repo GitHub
2. Deux services créés automatiquement :
   - `churn-api` — FastAPI
   - `churn-dashboard` — Streamlit

Variables d'environnement : `PYTHONPATH=src`

## Structure du projet

```text
src/churn/          # library métier
app/api/            # FastAPI
app/dashboard/      # Streamlit
tests/              # pytest (27+ tests)
notebooks/          # EDA
data/raw_data/      # bank_data.csv
scripts/            # run_training.py
```

## Contributors

- Dimitri Marchand (`dimiphoton`) — Data Engineering, ML, Dashboard, Déploiement

## Timeline

| Étape | Branche | Statut |
|-------|---------|--------|
| Reset + plan | main | ✅ |
| Scaffold | feature/01-scaffold | ✅ |
| SQLite | feature/02-database | ✅ |
| EDA | feature/03-eda | ✅ |
| Preprocessing | feature/04-preprocessing | ✅ |
| ML models | feature/05-ml-models | ✅ |
| Tests | feature/06-tests | ✅ |
| API + Docker | feature/07-fastapi-docker | ✅ |
| Dashboard | feature/08-streamlit | ✅ |
| Docs + Render | feature/09-deploy-docs | ✅ |

## Personal situation

Projet solo réalisé dans le cadre BeCode (consolidation churn prediction).
Approche feature branches avec merge par étape sur `main`.
