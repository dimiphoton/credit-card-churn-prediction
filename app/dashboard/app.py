"""Dashboard Streamlit — KPIs, EDA et résultats modèle."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from churn.config import (  # noqa: E402
    CHURN_POSITIVE_LABEL,
    CLASSIFIER_MODEL_PATH,
    TARGET_COLUMN,
)
from churn.ingest import load_raw_csv  # noqa: E402
from churn.predict import load_cluster_profiles, load_metrics, predict_churn  # noqa: E402

st.set_page_config(page_title="Churn Dashboard", layout="wide", page_icon="💳")

st.title("Credit Card Churn — Dashboard Marketing")
st.caption("KPIs, exploration et résultats du modèle ML")


@st.cache_data
def load_data() -> pd.DataFrame:
    """Charge le dataset (cache Streamlit)."""
    return load_raw_csv()


df = load_data()
churn_rate = (df[TARGET_COLUMN] == CHURN_POSITIVE_LABEL).mean() * 100

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Clients total", f"{len(df):,}")
col2.metric("Taux de churn", f"{churn_rate:.1f} %")
col3.metric("Clients attrited", f"{(df[TARGET_COLUMN] == CHURN_POSITIVE_LABEL).sum():,}")
col4.metric("Credit limit moyenne", f"${df['Credit_Limit'].mean():,.0f}")

st.divider()

# --- Onglets ---
tab_eda, tab_model, tab_clusters, tab_predict = st.tabs(
    ["Exploration", "Modèle ML", "Segments clients", "Prédiction"]
)

with tab_eda:
    st.subheader("Répartition du churn")
    st.bar_chart(df[TARGET_COLUMN].value_counts())

    st.subheader("Churn par catégorie de carte")
    card_churn = (
        df.groupby("Card_Category")[TARGET_COLUMN]
        .apply(lambda s: (s == CHURN_POSITIVE_LABEL).mean() * 100)
        .sort_values(ascending=False)
    )
    st.bar_chart(card_churn)

    st.subheader("Variables numériques clés")
    st.dataframe(
        df[["Customer_Age", "Credit_Limit", "Total_Trans_Amt", "Months_Inactive_12_mon"]].describe().T
    )

with tab_model:
    st.subheader("Performance du modèle")
    if CLASSIFIER_MODEL_PATH.exists():
        metrics = load_metrics()
        best = metrics["best_model"]
        st.success(f"Meilleur modèle : **{best}**")

        model_metrics = metrics["models"][best]
        m1, m2, m3 = st.columns(3)
        m1.metric("Recall", f"{model_metrics['recall']:.3f}")
        m2.metric("F1-score", f"{model_metrics['f1']:.3f}")
        m3.metric("ROC-AUC", f"{model_metrics['roc_auc']:.3f}")

        with st.expander("Rapport de classification"):
            st.code(metrics.get("classification_report", "N/A"))

        st.subheader("Limitations")
        st.markdown(
            """
            - Modèle entraîné sur données historiques (biais temporel possible).
            - Recall priorisé : plus de faux positifs acceptables pour ne pas rater un churner.
            - Label encoding des variables catégorielles (ordre arbitraire).
            - Pas de variables externes (macro-économie, concurrence).
            """
        )
    else:
        st.warning("Modèle non entraîné. Lancer `python scripts/run_training.py`.")

with tab_clusters:
    st.subheader("Segmentation clients (KMeans)")
    if CLASSIFIER_MODEL_PATH.exists():
        cluster_data = load_cluster_profiles()
        st.write(f"Nombre optimal de clusters : **{cluster_data['best_k']}**")

        profiles = pd.DataFrame(cluster_data["cluster_profiles"])
        st.dataframe(profiles, use_container_width=True)

        st.bar_chart(profiles.set_index("cluster_id")["churn_rate"] * 100)

        st.subheader("Profils types")
        for _, row in profiles.iterrows():
            st.markdown(
                f"**Cluster {int(row['cluster_id'])}** — "
                f"{int(row['size'])} clients, churn {row['churn_rate']*100:.1f} %, "
                f"âge moyen {row['avg_customer_age']:.0f} ans, "
                f"transactions moy. ${row['avg_total_trans_amt']:,.0f}"
            )
    else:
        st.warning("Clustering non disponible.")

with tab_predict:
    st.subheader("Prédire le churn d'un client")
    if not CLASSIFIER_MODEL_PATH.exists():
        st.warning("Entraîner le modèle d'abord.")
    else:
        sample = df.drop(columns=["Unnamed: 0", "Attrition_Flag", "CLIENTNUM"], errors="ignore").iloc[0]
        with st.form("predict_form"):
            st.write("Remplir les informations client :")
            inputs = {}
            cols = st.columns(3)
            fields = list(sample.index)
            for i, field in enumerate(fields):
                with cols[i % 3]:
                    if pd.api.types.is_numeric_dtype(sample[field]):
                        inputs[field] = st.number_input(field, value=float(sample[field]))
                    else:
                        inputs[field] = st.text_input(field, value=str(sample[field]))

            submitted = st.form_submit_button("Prédire")
            if submitted:
                # Cast numeric fields
                for field in fields:
                    if pd.api.types.is_numeric_dtype(sample[field]):
                        inputs[field] = type(sample[field])(inputs[field])
                result = predict_churn(inputs)
                st.json(result)
