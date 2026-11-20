"""
data_visualization.py
Enterprise Data Visualization Suite
Author: Senior Data Analyst / BI Developer
Project: HR Employee Analytics Dashboard

Generates 14 publication-grade, corporate-themed data visualizations:
 1. 01_workforce_demographics_by_department.png
 2. 02_gender_distribution_donut.png
 3. 03_attrition_rate_by_department.png
 4. 04_attrition_by_job_role.png
 5. 05_monthly_income_distribution_kde.png
 6. 06_salary_by_job_role_boxplot.png
 7. 07_attrition_by_overtime_status.png
 8. 08_age_group_vs_attrition_rate.png
 9. 09_job_satisfaction_vs_attrition.png
10. 10_work_life_balance_impact.png
11. 11_tenure_vs_monthly_income_scatter.png
12. 12_correlation_heatmap_matrix.png
13. 13_years_since_promotion_vs_attrition.png
14. 14_performance_rating_by_department.png
"""

import os
import tempfile
os.environ["MPLCONFIGDIR"] = tempfile.mkdtemp()
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set corporate theme standards
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
PRIMARY_COLOR = "#1E3A8A"     # Deep Corporate Navy
SECONDARY_COLOR = "#0D9488"   # Slate Teal
ACCENT_RED = "#DC2626"        # Alert / Attrition Crimson
ACCENT_GREEN = "#16A34A"      # Active / Retention Green
NEUTRAL_GRAY = "#64748B"      # Cool Gray
BG_LIGHT = "#F8FAFC"          # Slate White

def setup_figure(title: str, subtitle: str = None, figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor(BG_LIGHT)
    if subtitle:
        fig.suptitle(title, fontsize=15, fontweight="bold", color="#0F172A", y=0.98)
        ax.set_title(subtitle, fontsize=10, color="#475569", pad=12)
    else:
        ax.set_title(title, fontsize=14, fontweight="bold", color="#0F172A", pad=12)
    return fig, ax

def generate_all_visualizations(csv_path: str, output_dir: str):
    print("=" * 65)
    print("STARTING DATA VISUALIZATION GENERATION")
    print("=" * 65)
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    # -------------------------------------------------------------
    # CHART 1: Workforce Demographics by Department
    # -------------------------------------------------------------
    fig, ax = setup_figure("Workforce Headcount Distribution by Department", "Total number of employees actively recorded across core functional divisions")
    dept_counts = df["Department"].value_counts()
    bars = ax.bar(dept_counts.index, dept_counts.values, color=PRIMARY_COLOR, edgecolor="#0F172A", width=0.55)
    ax.set_ylabel("Employee Headcount", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_xlabel("Department", fontsize=11, fontweight="semibold", color="#334155")
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:,} ({height/len(df)*100:.1f}%)",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, max(dept_counts.values) * 1.15)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "01_workforce_demographics_by_department.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 1: 01_workforce_demographics_by_department.png")

    # -------------------------------------------------------------
    # CHART 2: Gender Distribution Donut Chart
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    fig.patch.set_facecolor("white")
    gender_counts = df["Gender"].value_counts()
    colors = [PRIMARY_COLOR, SECONDARY_COLOR, "#F59E0B"]
    wedges, texts, autotexts = ax.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        pctdistance=0.75
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
        at.set_fontsize(11)
    for t in texts:
        t.set_fontsize(11)
        t.set_fontweight("semibold")
        t.set_color("#1E293B")
    ax.set_title("Workforce Gender Diversity & Composition", fontsize=14, fontweight="bold", color="#0F172A", pad=14)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "02_gender_distribution_donut.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 2: 02_gender_distribution_donut.png")

    # -------------------------------------------------------------
    # CHART 3: Department-Wise Attrition Rate
    # -------------------------------------------------------------
    fig, ax = setup_figure("Department Attrition Rate Comparison", "Percentage of departed employees across business divisions")
    dept_attr = df.groupby("Department")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100).sort_values(ascending=False)
    bars = ax.bar(dept_attr.index, dept_attr.values, color=ACCENT_RED, edgecolor="#991B1B", width=0.55)
    ax.axhline(df["Attrition"].apply(lambda x: x == "Yes").mean() * 100, color="#1E293B", linestyle="--", linewidth=1.5, label=f"Company Average ({(df['Attrition']=='Yes').mean()*100:.1f}%)")
    ax.set_ylabel("Attrition Rate (%)", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_xlabel("Department", fontsize=11, fontweight="semibold", color="#334155")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.2f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color="#991B1B")
    ax.set_ylim(0, max(dept_attr.values) * 1.25)
    ax.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "03_attrition_rate_by_department.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 3: 03_attrition_rate_by_department.png")

    # -------------------------------------------------------------
    # CHART 4: Attrition by Job Role (Horizontal Bar)
    # -------------------------------------------------------------
    fig, ax = setup_figure("Attrition Rate by Job Role", "Comparative attrition percentages across all organizational titles", figsize=(11, 7))
    role_attr = df.groupby("JobRole")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100).sort_values(ascending=True)
    norm_colors = [ACCENT_RED if val >= 13.0 else SECONDARY_COLOR for val in role_attr.values]
    bars = ax.barh(role_attr.index, role_attr.values, color=norm_colors, edgecolor="#334155", height=0.6)
    ax.axvline((df["Attrition"] == "Yes").mean() * 100, color="#0F172A", linestyle="--", linewidth=1.5, label="Overall Benchmark")
    ax.set_xlabel("Attrition Rate (%)", fontsize=11, fontweight="semibold", color="#334155")
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f" {w:.1f}%",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9.5, fontweight="bold", color="#1E293B")
    ax.set_xlim(0, max(role_attr.values) * 1.18)
    ax.legend(loc="lower right")
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "04_attrition_by_job_role.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 4: 04_attrition_by_job_role.png")

    # -------------------------------------------------------------
    # CHART 5: Monthly Income Distribution (Histogram + KDE)
    # -------------------------------------------------------------
    fig, ax = setup_figure("Monthly Income Distribution & Skewness", "Probability density and histogram of workforce compensation levels")
    sns.histplot(df["MonthlyIncome"], kde=True, ax=ax, color=PRIMARY_COLOR, bins=35, edgecolor="white", alpha=0.65)
    mean_val = df["MonthlyIncome"].mean()
    med_val = df["MonthlyIncome"].median()
    ax.axvline(mean_val, color=ACCENT_RED, linestyle="--", linewidth=2, label=f"Mean: ${mean_val:,.0f}")
    ax.axvline(med_val, color=ACCENT_GREEN, linestyle="-", linewidth=2, label=f"Median: ${med_val:,.0f}")
    ax.set_xlabel("Monthly Income ($)", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_ylabel("Employee Count", fontsize=11, fontweight="semibold", color="#334155")
    ax.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, "05_monthly_income_distribution_kde.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 5: 05_monthly_income_distribution_kde.png")

    # -------------------------------------------------------------
    # CHART 6: Salary by Job Role Boxplot
    # -------------------------------------------------------------
    fig, ax = setup_figure("Compensation Structure by Job Role", "Salary distribution quartiles, medians, and executive outliers", figsize=(12, 7))
    order = df.groupby("JobRole")["MonthlyIncome"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="MonthlyIncome", y="JobRole", hue="JobRole", order=order, ax=ax, palette="Blues_r", boxprops=dict(alpha=0.85), legend=False)
    ax.set_xlabel("Monthly Income ($)", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_ylabel("Job Role", fontsize=11, fontweight="semibold", color="#334155")
    plt.tight_layout()
    chart6_path = os.path.join(output_dir, "06_salary_by_job_role_boxplot.png")
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 6: 06_salary_by_job_role_boxplot.png")

    # -------------------------------------------------------------
    # CHART 7: Attrition by Overtime Status
    # -------------------------------------------------------------
    fig, ax = setup_figure("Impact of Overtime on Employee Attrition", "Comparison of attrition rate between overtime workers and non-overtime workers")
    ot_df = df.groupby(["Overtime", "Attrition"]).size().unstack()
    ot_rates = (ot_df["Yes"] / ot_df.sum(axis=1) * 100).round(2)
    x = np.arange(len(ot_rates))
    bars = ax.bar(x, ot_rates.values, color=[SECONDARY_COLOR, ACCENT_RED], width=0.45, edgecolor="#0F172A")
    ax.set_xticks(x)
    ax.set_xticklabels([f"No Overtime\n(n={ot_df.loc['No'].sum():,})", f"Overtime Active\n(n={ot_df.loc['Yes'].sum():,})"], fontsize=11, fontweight="semibold")
    ax.set_ylabel("Attrition Rate (%)", fontsize=11, fontweight="semibold", color="#334155")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}% Attrition",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 5), textcoords="offset points",
                    ha="center", va="bottom", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, max(ot_rates.values) * 1.3)
    plt.tight_layout()
    chart7_path = os.path.join(output_dir, "07_attrition_by_overtime_status.png")
    plt.savefig(chart7_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 7: 07_attrition_by_overtime_status.png")

    # -------------------------------------------------------------
    # CHART 8: Age Group vs Attrition Rate
    # -------------------------------------------------------------
    fig, ax = setup_figure("Attrition Vulnerability across Age Cohorts", "Younger talent under 25 and early-career cohorts exhibit heightened turnover risk")
    age_attr = df.groupby("AgeGroup", observed=False)["Attrition"].apply(lambda x: (x == "Yes").mean() * 100)
    bars = ax.bar(age_attr.index.astype(str), age_attr.values, color=PRIMARY_COLOR, edgecolor="#0F172A", width=0.5)
    ax.set_ylabel("Attrition Rate (%)", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_xlabel("Age Bracket (Years)", fontsize=11, fontweight="semibold", color="#334155")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, max(age_attr.values) * 1.25)
    plt.tight_layout()
    chart8_path = os.path.join(output_dir, "08_age_group_vs_attrition_rate.png")
    plt.savefig(chart8_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 8: 08_age_group_vs_attrition_rate.png")

    # -------------------------------------------------------------
    # CHART 9: Job Satisfaction vs Attrition
    # -------------------------------------------------------------
    fig, ax = setup_figure("Job Satisfaction Level vs. Attrition Rate", "Turnover rate plunges dramatically as employee job satisfaction increases")
    sat_map = {1: "1 - Low", 2: "2 - Medium", 3: "3 - High", 4: "4 - Very High"}
    sat_attr = df.groupby("JobSatisfaction")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100)
    sat_labels = [sat_map[k] for k in sat_attr.index]
    palette = [ACCENT_RED, "#EA580C", "#0284C7", ACCENT_GREEN]
    bars = ax.bar(sat_labels, sat_attr.values, color=palette, edgecolor="#0F172A", width=0.5)
    ax.set_ylabel("Attrition Rate (%)", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_xlabel("Job Satisfaction Rating", fontsize=11, fontweight="semibold", color="#334155")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, max(sat_attr.values) * 1.25)
    plt.tight_layout()
    chart9_path = os.path.join(output_dir, "09_job_satisfaction_vs_attrition.png")
    plt.savefig(chart9_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 9: 09_job_satisfaction_vs_attrition.png")

    # -------------------------------------------------------------
    # CHART 10: Work-Life Balance Impact
    # -------------------------------------------------------------
    fig, ax = setup_figure("Work-Life Balance Influence on Turnover", "Attrition rates categorized by perceived employee work-life equilibrium")
    wlb_map = {1: "1 - Bad", 2: "2 - Good", 3: "3 - Better", 4: "4 - Best"}
    wlb_attr = df.groupby("WorkLifeBalance")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100)
    wlb_labels = [wlb_map[k] for k in wlb_attr.index]
    bars = ax.bar(wlb_labels, wlb_attr.values, color=[ACCENT_RED, "#F59E0B", SECONDARY_COLOR, ACCENT_GREEN], width=0.5, edgecolor="#0F172A")
    ax.set_ylabel("Attrition Rate (%)", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_xlabel("Work-Life Balance Rating", fontsize=11, fontweight="semibold", color="#334155")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, max(wlb_attr.values) * 1.25)
    plt.tight_layout()
    chart10_path = os.path.join(output_dir, "10_work_life_balance_impact.png")
    plt.savefig(chart10_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 10: 10_work_life_balance_impact.png")

    # -------------------------------------------------------------
    # CHART 11: Company Tenure vs Monthly Income (Scatter + Trend)
    # -------------------------------------------------------------
    fig, ax = setup_figure("Tenure Progression vs Monthly Compensation", "Relationship between organizational service years and salary advancement", figsize=(11, 6))
    sample_df = df.sample(n=min(1200, len(df)), random_state=42)
    sns.scatterplot(
        data=sample_df,
        x="YearsAtCompany",
        y="MonthlyIncome",
        hue="Attrition",
        palette={"No": SECONDARY_COLOR, "Yes": ACCENT_RED},
        alpha=0.6,
        s=45,
        ax=ax
    )
    sns.regplot(
        data=df,
        x="YearsAtCompany",
        y="MonthlyIncome",
        scatter=False,
        ax=ax,
        color="#0F172A",
        line_kws={"linewidth": 2, "linestyle": "--", "label": "Career Trendline"}
    )
    ax.set_xlabel("Years at Company", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_ylabel("Monthly Income ($)", fontsize=11, fontweight="semibold", color="#334155")
    ax.legend(title="Employee Attrition", loc="upper left")
    plt.tight_layout()
    chart11_path = os.path.join(output_dir, "11_tenure_vs_monthly_income_scatter.png")
    plt.savefig(chart11_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 11: 11_tenure_vs_monthly_income_scatter.png")

    # -------------------------------------------------------------
    # CHART 12: Correlation Heatmap Matrix
    # -------------------------------------------------------------
    fig, ax = setup_figure("Correlation Heatmap: Key HR Quantitative Metrics", "Pearson correlation coefficients across organizational performance indicators", figsize=(10, 8))
    numeric_cols = [
        "Age", "MonthlyIncome", "YearsAtCompany", "TotalWorkingYears",
        "YearsSinceLastPromotion", "JobSatisfaction", "EnvironmentSatisfaction",
        "WorkLifeBalance", "PerformanceRating"
    ]
    corr = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        vmin=-0.2,
        vmax=1.0,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    plt.xticks(rotation=45, ha="right", fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)
    plt.tight_layout()
    chart12_path = os.path.join(output_dir, "12_correlation_heatmap_matrix.png")
    plt.savefig(chart12_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 12: 12_correlation_heatmap_matrix.png")

    # -------------------------------------------------------------
    # CHART 13: Years Since Last Promotion vs Attrition
    # -------------------------------------------------------------
    fig, ax = setup_figure("Attrition Propensity by Promotion Stagnation", "Turnover risk escalates when employee promotion intervals exceed 4-5 years")
    promo_attr = df.groupby("YearsSinceLastPromotion")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100)
    promo_attr = promo_attr.loc[promo_attr.index <= 10]  # Focus on key 0-10 year window
    ax.plot(promo_attr.index, promo_attr.values, marker="o", color=ACCENT_RED, linewidth=2.5, markersize=7)
    ax.fill_between(promo_attr.index, promo_attr.values, alpha=0.15, color=ACCENT_RED)
    ax.set_xlabel("Years Since Last Promotion", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_ylabel("Attrition Rate (%)", fontsize=11, fontweight="semibold", color="#334155")
    for x_val, y_val in zip(promo_attr.index, promo_attr.values):
        ax.annotate(f"{y_val:.1f}%", (x_val, y_val), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(promo_attr.values) * 1.3)
    plt.tight_layout()
    chart13_path = os.path.join(output_dir, "13_years_since_promotion_vs_attrition.png")
    plt.savefig(chart13_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 13: 13_years_since_promotion_vs_attrition.png")

    # -------------------------------------------------------------
    # CHART 14: Performance Rating Distribution by Department
    # -------------------------------------------------------------
    fig, ax = setup_figure("Performance Appraisal Ratings across Departments", "Proportional breakdown of employee annual appraisal ratings (1=Low, 4=Outstanding)")
    perf_dept = pd.crosstab(df["Department"], df["PerformanceRating"], normalize="index") * 100
    perf_dept.plot(kind="bar", stacked=True, ax=ax, colormap="Blues", edgecolor="#0F172A", width=0.55)
    ax.set_ylabel("Percentage of Department (%)", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_xlabel("Department", fontsize=11, fontweight="semibold", color="#334155")
    ax.set_xticklabels(perf_dept.index, rotation=0, fontsize=10, fontweight="semibold")
    ax.legend(title="Performance Rating", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    chart14_path = os.path.join(output_dir, "14_performance_rating_by_department.png")
    plt.savefig(chart14_path, dpi=300)
    plt.close()
    print("  ✓ Saved Chart 14: 14_performance_rating_by_department.png")

    print("=" * 65)
    print(f"ALL 14 VISUALIZATIONS GENERATED SUCCESSFULLY IN: {output_dir}")
    print("=" * 65)

if __name__ == "__main__":
    csv_file = os.path.join("dataset", "cleaned_employee_data.csv")
    out_dir = os.path.join("outputs", "charts")
    generate_all_visualizations(csv_file, out_dir)
