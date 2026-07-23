# Guide Power BI — Credit Card Churn

Ce dossier contient tout pour créer ton dashboard Power BI **sans coder**.

## Fichiers

| Fichier | Rôle |
|---------|------|
| `data/bank_churn_powerbi.csv` | Données prêtes à importer |
| `measures.dax` | Mesures DAX à copier-coller |
| `VISUALS.md` | Liste des graphiques à créer |

## Étape 1 — Installer Power BI Desktop (gratuit)

1. Télécharge : https://powerbi.microsoft.com/desktop/
2. Installe et lance **Power BI Desktop** (Windows)

## Étape 2 — Importer les données

1. **Accueil** → **Obtenir des données** → **Texte/CSV**
2. Sélectionne : `powerbi/data/bank_churn_powerbi.csv`
3. Clique **Charger** (ou **Transformer** si tu veux vérifier les types)

> Regénérer le CSV : `python scripts/export_for_powerbi.py`

## Étape 3 — Créer les mesures DAX

1. Onglet **Modélisation** → **Nouvelle mesure**
2. Copie les mesures depuis [`measures.dax`](measures.dax) une par une

Mesures principales :

- `Churn Rate` — taux de churn global
- `Total Customers` — nombre de clients
- `Model Accuracy` — accord prédictions ML vs réalité
- `High Risk Customers` — clients `RiskLevel = high`

## Étape 3b — Colonnes ML (déjà dans le CSV)

Pas besoin de ré-entraîner dans Power BI. Le CSV contient :

- `ChurnProbability`, `PredictedChurn`, `RiskLevel`
- `ML_Cluster` (KMeans)
- `PredictionMatch` (Correct / Incorrect)

Voir visuels ML dans [`VISUALS.md`](VISUALS.md) page **ML Predictions**.

## Étape 4 — Créer les visuels

Suis le plan dans [`VISUALS.md`](VISUALS.md). Minimum recommandé :

1. **Carte** — Churn Rate (%)
2. **Graphique en anneau** — Active vs Churned
3. **Graphique en barres** — Churn Rate par Card_Category
4. **Graphique en barres** — Churn Rate par Income_Category
5. **Histogramme** — Customer_Age par ChurnLabel
6. **Table** — KPIs par segment

## Étape 5 — Sauvegarder le rapport

1. **Fichier** → **Enregistrer sous**
2. Enregistre dans ce dossier : `powerbi/churn_report.pbix`
3. Commit le `.pbix` dans Git (optionnel mais pro pour BeCode)

## Étape 6 — Publier en ligne (optionnel)

1. **Accueil** → **Publier** → connecte ton compte Microsoft
2. Choisis un espace de travail (workspace)
3. Sur https://app.powerbi.com → ouvre le rapport → **Fichier** → **Intégrer le rapport** → **Site web ou portail**
4. Copie l’URL ou le code `<iframe>` et ajoute-le dans le README principal

## Comparaison Streamlit vs Power BI vs Tableau

| | Streamlit | Power BI | Tableau |
|---|-----------|----------|---------|
| **ML scores** | ✅ live | ✅ CSV export | ✅ CSV export |
| **Clustering** | ✅ | ✅ `ML_Cluster` | ✅ `ML_Cluster` |
| **Code** | Python | DAX + clic | Calculs + clic |
| **Déploiement** | Render | powerbi.com | Tableau Public |

Détails : [`bi/COMPARISON.md`](../bi/COMPARISON.md) · Tableau : [`tableau/README.md`](../tableau/README.md)
