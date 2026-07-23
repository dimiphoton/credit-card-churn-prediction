"""Generate README screenshot assets from project data."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "docs" / "images"
DATA_PATH = PROJECT_ROOT / "data" / "raw_data" / "bank_data.csv"

sns.set_theme(style="whitegrid", palette="Set2")


def save_churn_overview(df: pd.DataFrame) -> None:
    """Bar chart: Existing vs Attrited customers."""
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = df["Attrition_Flag"].value_counts()
    sns.barplot(x=counts.index, y=counts.values, ax=ax, hue=counts.index, legend=False)
    ax.set_title("Customer attrition split", fontsize=14, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Number of customers")
    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=3)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "churn_overview.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_churn_by_card(df: pd.DataFrame) -> None:
    """Churn rate by card category."""
    rate = (
        df.groupby("Card_Category")["Attrition_Flag"]
        .apply(lambda s: (s == "Attrited Customer").mean() * 100)
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=rate.index, y=rate.values, ax=ax, color="steelblue")
    ax.set_title("Churn rate by card category", fontsize=14, fontweight="bold")
    ax.set_xlabel("Card category")
    ax.set_ylabel("Churn rate (%)")
    for i, value in enumerate(rate.values):
        ax.text(i, value + 0.3, f"{value:.1f}%", ha="center")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "churn_by_card.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_correlation_heatmap(df: pd.DataFrame) -> None:
    """Heatmap of numeric features vs churn."""
    numeric_cols = [
        "Customer_Age",
        "Credit_Limit",
        "Total_Trans_Amt",
        "Total_Trans_Ct",
        "Months_Inactive_12_mon",
        "Contacts_Count_12_mon",
    ]
    plot_df = df.copy()
    plot_df["is_churn"] = (plot_df["Attrition_Flag"] == "Attrited Customer").astype(int)
    corr = plot_df[numeric_cols + ["is_churn"]].corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Feature correlation matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_kpi_summary(df: pd.DataFrame) -> None:
    """Simple KPI cards-style summary image."""
    churn_rate = (df["Attrition_Flag"] == "Attrited Customer").mean() * 100
    attrited = (df["Attrition_Flag"] == "Attrited Customer").sum()
    avg_limit = df["Credit_Limit"].mean()

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    fig.suptitle("Dashboard KPIs", fontsize=16, fontweight="bold", y=1.02)

    kpis = [
        ("Total customers", f"{len(df):,}"),
        ("Churn rate", f"{churn_rate:.1f}%"),
        ("Avg credit limit", f"${avg_limit:,.0f}"),
    ]
    colors = ["#4C78A8", "#F58518", "#54A24B"]

    for ax, (label, value), color in zip(axes, kpis, colors):
        ax.axis("off")
        ax.text(0.5, 0.65, value, ha="center", va="center", fontsize=28, fontweight="bold", color=color)
        ax.text(0.5, 0.25, label, ha="center", va="center", fontsize=12, color="#333333")
        ax.set_facecolor("#F8F9FA")

    fig.patch.set_facecolor("white")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dashboard_kpis.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_cluster_churn() -> None:
    """Cluster churn rates from saved training artifacts."""
    import json

    profiles_path = PROJECT_ROOT / "models" / "cluster_profiles.json"
    if not profiles_path.exists():
        return

    profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
    df = pd.DataFrame(profiles["cluster_profiles"])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["cluster_id"].astype(str), df["churn_rate"] * 100, color=["#4C78A8", "#F58518"])
    ax.set_title("Churn rate by customer segment", fontsize=14, fontweight="bold")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Churn rate (%)")
    for i, value in enumerate(df["churn_rate"] * 100):
        ax.text(i, value + 0.3, f"{value:.1f}%", ha="center")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "cluster_churn.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_model_metrics() -> None:
    """Model performance chart from saved metrics."""
    import json

    metrics_path = PROJECT_ROOT / "models" / "metrics.json"
    if not metrics_path.exists():
        return

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    best = metrics["best_model"]
    model_metrics = metrics["models"][best]

    fig, ax = plt.subplots(figsize=(8, 5))
    names = ["Recall", "F1", "ROC-AUC"]
    values = [model_metrics["recall"], model_metrics["f1"], model_metrics["roc_auc"]]
    bars = ax.bar(names, values, color=["#54A24B", "#4C78A8", "#E45756"])
    ax.set_ylim(0, 1)
    ax.set_title(f"Model performance — {best.replace('_', ' ').title()}", fontsize=14, fontweight="bold")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.3f}", ha="center")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "model_metrics.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    save_churn_overview(df)
    save_churn_by_card(df)
    save_correlation_heatmap(df)
    save_kpi_summary(df)
    save_cluster_churn()
    save_model_metrics()
    print(f"Saved images to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
