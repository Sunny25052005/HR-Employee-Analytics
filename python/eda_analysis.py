"""
eda_analysis.py
Exploratory Data Analysis (EDA) Module
Author: Senior Data Analyst
Project: HR Employee Analytics Dashboard

Performs in-depth statistical profiling across:
1. Workforce Demographics & Headcount Distribution
2. Attrition Dynamics (Overall, Department, Role, Overtime, Tenure)
3. Compensation & Salary Structure Analysis
4. Employee Experience & Career Progression
5. Workplace Wellbeing & Satisfaction Ratings
6. Performance & Promotion Distribution
Outputs a structured statistical report to outputs/reports/eda_summary_report.txt
"""

import os
import pandas as pd
import numpy as np

def run_eda(csv_path: str, report_out_path: str):
    print("=" * 65)
    print("STARTING EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 65)
    
    df = pd.read_csv(csv_path)
    total_records = len(df)
    
    # 1. Demographics & Overview
    total_active = (df["EmploymentStatus"] == "Active").sum()
    total_attrition = (df["Attrition"] == "Yes").sum()
    overall_attrition_rate = (total_attrition / total_records) * 100
    retention_rate = 100 - overall_attrition_rate
    
    avg_age = df["Age"].mean()
    median_age = df["Age"].median()
    avg_salary = df["MonthlyIncome"].mean()
    median_salary = df["MonthlyIncome"].median()
    avg_tenure = df["YearsAtCompany"].mean()
    avg_total_exp = df["TotalWorkingYears"].mean()
    
    # Gender Distribution
    gender_counts = df["Gender"].value_counts()
    gender_pcts = df["Gender"].value_counts(normalize=True) * 100
    
    # Department Distribution
    dept_counts = df["Department"].value_counts()
    dept_pcts = df["Department"].value_counts(normalize=True) * 100
    
    # 2. Attrition Breakdown by Department
    dept_attr = df.groupby("Department")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100).round(2)
    dept_headcount = df.groupby("Department")["EmployeeID"].count()
    dept_attr_count = df[df["Attrition"] == "Yes"].groupby("Department")["EmployeeID"].count()
    
    dept_summary = pd.DataFrame({
        "Total Employees": dept_headcount,
        "Attrition Count": dept_attr_count,
        "Attrition Rate (%)": dept_attr
    }).sort_values(by="Attrition Rate (%)", ascending=False)
    
    # 3. Job Role Attrition & Compensation Breakdown
    role_summary = df.groupby("JobRole").agg(
        Total_Employees=("EmployeeID", "count"),
        Attrition_Count=("Attrition", lambda x: (x == "Yes").sum()),
        Attrition_Rate=("Attrition", lambda x: round((x == "Yes").mean() * 100, 2)),
        Avg_Monthly_Salary=("MonthlyIncome", lambda x: round(x.mean(), 2)),
        Median_Salary=("MonthlyIncome", "median"),
        Avg_Tenure_Years=("YearsAtCompany", lambda x: round(x.mean(), 2))
    ).sort_values(by="Attrition_Rate", ascending=False)
    
    # 4. Overtime Impact
    ot_summary = df.groupby("Overtime").agg(
        Total_Headcount=("EmployeeID", "count"),
        Attrition_Count=("Attrition", lambda x: (x == "Yes").sum()),
        Attrition_Rate=("Attrition", lambda x: round((x == "Yes").mean() * 100, 2)),
        Avg_Salary=("MonthlyIncome", lambda x: round(x.mean(), 2))
    )
    
    # 5. Age Group Impact
    age_summary = df.groupby("AgeGroup", observed=False).agg(
        Total_Employees=("EmployeeID", "count"),
        Attrition_Count=("Attrition", lambda x: (x == "Yes").sum()),
        Attrition_Rate=("Attrition", lambda x: round((x == "Yes").mean() * 100, 2)),
        Avg_Salary=("MonthlyIncome", lambda x: round(x.mean(), 2))
    )
    
    # 6. Tenure Cohort Impact
    tenure_summary = df.groupby("TenureGroup", observed=False).agg(
        Total_Employees=("EmployeeID", "count"),
        Attrition_Count=("Attrition", lambda x: (x == "Yes").sum()),
        Attrition_Rate=("Attrition", lambda x: round((x == "Yes").mean() * 100, 2)),
        Avg_Salary=("MonthlyIncome", lambda x: round(x.mean(), 2))
    )
    
    # 7. Satisfaction Levels & Attrition Correlation
    sat_summary = df.groupby("JobSatisfaction").agg(
        Total_Employees=("EmployeeID", "count"),
        Attrition_Count=("Attrition", lambda x: (x == "Yes").sum()),
        Attrition_Rate=("Attrition", lambda x: round((x == "Yes").mean() * 100, 2))
    )
    
    wlb_summary = df.groupby("WorkLifeBalance").agg(
        Total_Employees=("EmployeeID", "count"),
        Attrition_Count=("Attrition", lambda x: (x == "Yes").sum()),
        Attrition_Rate=("Attrition", lambda x: round((x == "Yes").mean() * 100, 2))
    )
    
    # 8. Performance & Promotions
    perf_summary = df.groupby("PerformanceRating").agg(
        Total_Employees=("EmployeeID", "count"),
        Avg_Salary=("MonthlyIncome", lambda x: round(x.mean(), 2)),
        Attrition_Rate=("Attrition", lambda x: round((x == "Yes").mean() * 100, 2))
    )
    
    stagnant_promo_count = ((df["YearsSinceLastPromotion"] >= 5) & (df["EmploymentStatus"] == "Active")).sum()
    
    # Print highlights to stdout
    print(f"Total Headcount Analyzed   : {total_records:,}")
    print(f"Active Employees           : {total_active:,} ({total_active/total_records*100:.1f}%)")
    print(f"Attrition Count            : {total_attrition:,} ({overall_attrition_rate:.2f}%)")
    print(f"Employee Retention Rate    : {retention_rate:.2f}%")
    print(f"Average Monthly Salary     : ${avg_salary:,.2f} (Median: ${median_salary:,.2f})")
    print(f"Average Age / Tenure       : {avg_age:.1f} yrs / {avg_tenure:.1f} yrs")
    print(f"Highest Attrition Dept     : {dept_summary.index[0]} ({dept_summary['Attrition Rate (%)'].iloc[0]}%)")
    print(f"Highest Attrition Role     : {role_summary.index[0]} ({role_summary['Attrition_Rate'].iloc[0]}%)")
    print(f"Overtime Attrition Impact  : Overtime Yes = {ot_summary.loc['Yes', 'Attrition_Rate']}% vs No = {ot_summary.loc['No', 'Attrition_Rate']}%")
    print(f"Active Stagnant Promotions : {stagnant_promo_count:,} employees (>=5 years without promotion)\n")
    
    # Save structured summary report
    os.makedirs(os.path.dirname(report_out_path), exist_ok=True)
    with open(report_out_path, "w", encoding="utf-8") as f:
        f.write("=" * 75 + "\n")
        f.write("HR EMPLOYEE ANALYTICS - COMPREHENSIVE EDA SUMMARY REPORT\n")
        f.write("=" * 75 + "\n\n")
        
        f.write("SECTION 1: KEY PERFORMANCE INDICATORS (ORGANIZATIONAL METRICS)\n")
        f.write(f"  - Total Employee Count      : {total_records:,}\n")
        f.write(f"  - Current Active Headcount  : {total_active:,} ({total_active/total_records*100:.2f}%)\n")
        f.write(f"  - Total Attrition Count     : {total_attrition:,} ({overall_attrition_rate:.2f}%)\n")
        f.write(f"  - Workforce Retention Rate  : {retention_rate:.2f}%\n")
        f.write(f"  - Mean Monthly Income       : ${avg_salary:,.2f}\n")
        f.write(f"  - Median Monthly Income     : ${median_salary:,.2f}\n")
        f.write(f"  - Mean Employee Age         : {avg_age:.2f} Years\n")
        f.write(f"  - Mean Company Tenure       : {avg_tenure:.2f} Years\n")
        f.write(f"  - Mean Total Experience     : {avg_total_exp:.2f} Years\n\n")
        
        f.write("SECTION 2: WORKFORCE DEMOGRAPHIC DISTRIBUTION\n")
        f.write("GENDER DISTRIBUTION:\n")
        for g in gender_counts.index:
            f.write(f"  - {g:12}: {gender_counts[g]:,d} ({gender_pcts[g]:.2f}%)\n")
        f.write("\nDEPARTMENT DISTRIBUTION:\n")
        for d in dept_counts.index:
            f.write(f"  - {d:25}: {dept_counts[d]:,d} ({dept_pcts[d]:.2f}%)\n")
        f.write("\n")
        
        f.write("SECTION 3: ATTRITION ANALYSIS BY DEPARTMENT\n")
        f.write(dept_summary.to_string() + "\n\n")
        
        f.write("SECTION 4: JOB ROLE PROFILE & COMPENSATION BENCHMARKS\n")
        f.write(role_summary.to_string() + "\n\n")
        
        f.write("SECTION 5: OVERTIME WORK ANALYSIS\n")
        f.write(ot_summary.to_string() + "\n\n")
        
        f.write("SECTION 6: AGE GROUP ANALYSIS\n")
        f.write(age_summary.to_string() + "\n\n")
        
        f.write("SECTION 7: TENURE COHORT ATTRITION PATTERNS\n")
        f.write(tenure_summary.to_string() + "\n\n")
        
        f.write("SECTION 8: JOB SATISFACTION VS ATTRITION\n")
        f.write(sat_summary.to_string() + "\n\n")
        
        f.write("SECTION 9: WORK-LIFE BALANCE IMPACT\n")
        f.write(wlb_summary.to_string() + "\n\n")
        
        f.write("SECTION 10: PERFORMANCE AND CAREER PROGRESSION\n")
        f.write(perf_summary.to_string() + "\n")
        f.write(f"Active employees with >= 5 years without promotion: {stagnant_promo_count:,}\n\n")
        f.write("=" * 75 + "\n")
        f.write("END OF EDA SUMMARY REPORT\n")
        f.write("=" * 75 + "\n")
        
    print(f"EDA Summary successfully written to: {report_out_path}")
    return df

if __name__ == "__main__":
    csv_file = os.path.join("dataset", "cleaned_employee_data.csv")
    report_file = os.path.join("outputs", "reports", "eda_summary_report.txt")
    run_eda(csv_file, report_file)
