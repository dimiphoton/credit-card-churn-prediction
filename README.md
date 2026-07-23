# Credit Card Churn Prediction

## What is this?

A **customer retention toolkit** for a bank facing rising credit card churn (~16%).

Marketing teams get three things out of the box:

1. **Risk scoring** — flag clients likely to leave before they do
2. **Customer segments** — group clients by behaviour for targeted campaigns
3. **Live dashboard** — KPIs, model performance, and interactive predictions

Built as a BeCode consolidation project (Data Engineer + ML Engineer + Data Analyst).

---

## Results at a glance

### Key metrics

| KPI | Value |
|-----|------:|
| Total customers | 10,127 |
| Churn rate | **16.1%** |
| Existing customers | 8,500 |
| Attrited customers | 1,627 |

### Churn split

```text
Existing Customer  ████████████████████████████████████████████████  84%
Attrited Customer  █████████                                         16%
```

### Screenshots

**Dashboard KPIs**

![Dashboard KPIs](docs/images/dashboard_kpis.png)

**Churn overview**

![Churn overview](docs/images/churn_overview.png)

**Churn by card category**

![Churn by card category](docs/images/churn_by_card.png)

**Feature correlations**

![Correlation heatmap](docs/images/correlation_heatmap.png)

**Customer segments (KMeans)**

![Cluster churn rates](docs/images/cluster_churn.png)

**Model performance (Random Forest)**

![Model metrics](docs/images/model_metrics.png)

> Regenerate images: `python scripts/run_training.py` then `python scripts/generate_readme_images.py`

### What the charts show

**EDA notebook** (`notebooks/01_eda.ipynb`)

- Churn rate breakdown (Existing vs Attrited)
- Numeric feature distributions by churn status (age, credit limit, transactions…)
- Churn rate by card category, income, education
- Correlation heatmap — top signals: `Total_Trans_Amt`, `Total_Trans_Ct`, `Contacts_Count_12_mon`, `Months_Inactive_12_mon`

**Streamlit dashboard** (`app/dashboard/app.py`)

| Tab | Visual output |
|-----|---------------|
| Exploration | KPI cards, churn bar chart, churn-by-card-category chart |
| ML Model | Recall / F1 / ROC-AUC metrics for the best classifier |
| Customer Segments | Cluster table + churn-rate bar chart per segment |
| Prediction | Live churn probability + risk level (low / medium / high) |

### Main findings

- Churn is **imbalanced** (~16% positive class) → SMOTE applied during training
- **Low activity** (inactive months, low transaction count) strongly correlates with churn
- **Blue card** holders show higher churn rates — priority segment for retention campaigns
- **Random Forest** wins on recall vs Logistic Regression (**0.87 recall** on test set)

---

## Technical documentation

### Stack

| Layer | Technology |
|-------|------------|
| Storage | SQLite |
| EDA | Jupyter |
| ML | scikit-learn + imbalanced-learn (SMOTE) |
| Clustering | KMeans (silhouette score) |
| API | FastAPI |
| Dashboard | Streamlit |
| Deploy | Docker + Render |

See also [`CRITERIA.md`](CRITERIA.md) (BeCode brief) · [`PROJECT_PLAN.md`](PROJECT_PLAN.md) (technical plan)

### Installation

**Requirements:** Python 3.10+

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

### Usage

**1. Train the pipeline**

```bash
python scripts/run_training.py
```

Outputs: `data/processed/churn.db`, models in `models/`.

**2. Start the API**

```bash
# Windows
set PYTHONPATH=src

# Linux / macOS
export PYTHONPATH=src

uvicorn app.api.main:app --reload --port 8000
```

| Endpoint | Description |
|----------|-------------|
| `GET /health` | API health check |
| `GET /ready` | Model loaded |
| `GET /metrics` | ML metrics (recall, F1, ROC-AUC) |
| `POST /predict` | Churn prediction |
| `GET /docs` | Swagger UI |

**3. Start the dashboard**

```bash
streamlit run app/dashboard/app.py
```

→ http://localhost:8501

**4. Docker**

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Dashboard | http://localhost:8501 |

**5. Tests**

```bash
pytest
```

31 tests covering ingestion, preprocessing, ML, API, and full pipeline.

### Model choices & limitations

**Classification**

- Target: `Attrition_Flag` (binary)
- Models: Logistic Regression (baseline) + Random Forest
- Imbalance handled with SMOTE on the training set
- Best model selected by **recall** on the test set

**Clustering**

- KMeans on scaled features, optimal K via silhouette score (K = 2–8)
- Output: cluster profiles (size, churn rate, avg age, avg transactions)

**Limitations**

- Static historical data — no macro-economic or competitor variables
- Label encoding on categoricals (not one-hot)
- High recall → more false positives (broader marketing outreach)
- Periodic retraining recommended in production

### Deploy on Render

Linked GitHub account: `dimiphoton`. Blueprint file: [`render.yaml`](render.yaml)

1. Render Dashboard → **New Blueprint** → select this repo
2. Two services are created:
   - `churn-api` — FastAPI
   - `churn-dashboard` — Streamlit

Env var: `PYTHONPATH=src` — training runs automatically at build time.

### Project structure

```text
credit-card-churn-prediction/
├── src/churn/              # Core library
│   ├── ingest.py           # CSV → SQLite
│   ├── cleaning.py
│   ├── features.py
│   ├── train.py            # Classification + SMOTE
│   ├── clustering.py       # KMeans
│   └── predict.py
├── app/
│   ├── api/main.py         # FastAPI
│   └── dashboard/app.py    # Streamlit
├── tests/
├── notebooks/01_eda.ipynb
├── scripts/run_training.py
├── data/raw_data/bank_data.csv
├── Dockerfile
├── docker-compose.yml
└── render.yaml
```

### Git workflow

Feature branches merged into `main` step by step:

`feature/01-scaffold` → `02-database` → `03-eda` → `04-preprocessing` → `05-ml-models` → `06-tests` → `07-fastapi-docker` → `08-streamlit` → `09-deploy-docs`

### Contributors

- **Dimitri Marchand** ([@dimiphoton](https://github.com/dimiphoton)) — Data Engineering, ML, Dashboard, Deployment

### Dataset

[Credit Card Customers (Kaggle)](https://www.kaggle.com/sakshigoyal7/credit-card-customers)
