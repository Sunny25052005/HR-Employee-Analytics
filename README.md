# 🏢 HR Employee Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1.svg?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Tests](https://img.shields.io/badge/Tests-14%2F14%20Passing-brightgreen.svg?logo=pytest&logoColor=white)](tests/test_data.py)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> An end-to-end People Analytics and Business Intelligence solution engineered to diagnose employee turnover, evaluate compensation equity, audit promotion stagnation, and provide executive decision support for HR leadership.

---

## 📌 Table of Contents
1. [Executive Summary & Business Problem](#-executive-summary--business-problem)
2. [End-to-End Architecture](#-end-to-end-architecture)
3. [Technology Stack](#-technology-stack)
4. [Dataset Description](#-dataset-description)
5. [Data Cleaning & Validation Pipeline](#-data-cleaning--validation-pipeline)
6. [Exploratory Data Analysis (EDA) Highlights](#-exploratory-data-analysis-eda-highlights)
7. [Visualizations Gallery](#-visualizations-gallery)
8. [MySQL Relational Database & Advanced SQL](#-mysql-relational-database--advanced-sql)
9. [Power BI Executive Dashboard](#-power-bi-executive-dashboard)
10. [DAX Measures Reference](#-dax-measures-reference)
11. [Top Strategic Business Insights](#-top-strategic-business-insights)
12. [Automated Testing & Verification](#-automated-testing--verification)
13. [Installation & Execution Guide](#-installation--execution-guide)
14. [Repository File Structure](#-repository-file-structure)
15. [Resume & Interview Presentation Guide](#-resume--interview-presentation-guide)
16. [Future Improvements](#-future-improvements)

---

## 💼 Executive Summary & Business Problem

Unplanned employee turnover costs modern enterprises billions annually in lost productivity, recruitment overhead, and organizational knowledge drain. Human Resource leaders often operate with fragmented, lagging metrics that fail to isolate root causes.

### Key Business Questions Addressed:
1. **Voluntary Attrition Drivers:** Why are employees leaving, and what measurable behavioral signals (chronic overtime, low work-life balance, lack of promotion) predict departure?
2. **Flight Risk Identification:** Which job roles and departments suffer from abnormal churn compared to organizational benchmarks?
3. **Compensation & Equity Benchmarks:** How does compensation scale across titles, tenure, and education? Are there gender pay disparities?
4. **Promotion Stagnation:** How many top performers have been overlooked for career advancement for over 4-5 years, and how does stagnation impact retention?

---

## 🏗 End-to-End Architecture

```
+─────────────────────────────────────────────────────────────────────────────────+
|                           END-TO-END DATA ARCHITECTURE                          |
+─────────────────────────────────────────────────────────────────────────────────+
|                                                                                 |
|  [ Data Generation ] ────────► python/generate_dataset.py                       |
|                                └── 5,010 synthetic records with anomalies      |
|                                                                                 |
|  [ Ingestion & Cleaning ] ───► python/data_cleaning.py                          |
|                                ├── Deduplication & whitespace trimming          |
|                                ├── Context-aware missing value imputation       |
|                                ├── Chronology & working age constraint checks   |
|                                ├── IQR Outlier analysis                         |
|                                └── Feature Engineering (AgeGroup, SalaryBand)   |
|                                                                                 |
|  [ Curated Production Tier ] ► dataset/cleaned_employee_data.csv (5,000 rows)   |
|                                                                                 |
|  [ Analysis & Modeling ] ─────┬────────────────────────┬─────────────────────┐  |
|                               ▼                        ▼                     ▼  |
|                        [ Python EDA ]            [ MySQL 8.0+ ]         [ Power BI ]
|                        eda_analysis.py           Relational Tables      4 Pages |
|                        14 High-Res Charts        Star-Schema Dimensions 21 DAX  |
|                        Jupyter Notebook          30 Advanced Queries    Measures|
|                                                                                 |
|  [ Quality Assurance ] ──────► tests/test_data.py (14/14 Pytest Automated Tests)|
+─────────────────────────────────────────────────────────────────────────────────+
```

---

## 🛠 Technology Stack

- **Data Processing & Analytics:** Python 3.12, Pandas 2.2+, NumPy 2.5+
- **Data Visualization:** Matplotlib 3.11+, Seaborn 0.13+
- **Relational Database:** MySQL 8.0+, SQL (Window Functions, CTEs, Joins, Constraints)
- **Business Intelligence:** Microsoft Power BI Desktop, DAX (Data Analysis Expressions), Power Query
- **Testing & Quality Assurance:** Pytest 9.2+, OpenPyXL
- **Version Control & Collaboration:** Git, GitHub

---

## 📊 Dataset Description

The analysis operates on a realistic, enterprise-grade HR dataset of **5,000 verified employee records** generated using a reproducible pseudorandom seed (`seed=42`).

| Category | Attributes Included |
| :--- | :--- |
| **Demographics** | `EmployeeID`, `Age`, `Gender`, `Department`, `Education`, `EducationField` |
| **Tenure & History**| `JoiningDate`, `YearsAtCompany`, `TotalWorkingYears`, `YearsSinceLastPromotion` |
| **Compensation** | `MonthlyIncome`, `SalaryBand` |
| **Sentiment & Rating**| `JobSatisfaction`, `EnvironmentSatisfaction`, `WorkLifeBalance`, `OverallSatisfaction`, `PerformanceRating` |
| **Operations** | `JobRole`, `Overtime`, `BusinessTravel`, `TrainingTimesLastYear`, `Attrition`, `EmploymentStatus` |

*Note: Raw dataset is stored in `dataset/raw_employee_data.csv` (contains 10 duplicate rows and controlled missing values for pipeline testing). Cleaned production data is stored in `dataset/cleaned_employee_data.csv`.*

---

## 🧹 Data Cleaning & Validation Pipeline

The enterprise cleaning pipeline (`python/data_cleaning.py`) guarantees 100% data integrity before warehouse ingestion:
1. **Deduplication:** Identified and eliminated 10 duplicate employee records based on `EmployeeID` uniqueness.
2. **String Standardization:** Trimmed leading/trailing whitespaces across 10 text columns.
3. **Context-Aware Imputation:**
   - Missing `MonthlyIncome` values imputed using median grouped by `JobRole`.
   - Missing `EducationField` values imputed using departmental mode.
   - Missing `WorkLifeBalance` imputed using global mode.
4. **Chronological Consistency Enforcement:**
   - Verified that `YearsAtCompany <= TotalWorkingYears`.
   - Ensured `YearsSinceLastPromotion <= YearsAtCompany`.
   - Validated legal minimum working age (`Age >= TotalWorkingYears + 16`).
5. **Outlier Detection via IQR:** Evaluated quartile spreads on continuous features. High salary outliers were preserved as legitimate executive compensation.
6. **Feature Engineering:** Constructed analytical bands: `AgeGroup`, `TenureGroup`, `SalaryBand`, and `OverallSatisfaction`.

---

## 📈 Exploratory Data Analysis (EDA) Highlights

Summary metrics from `outputs/reports/eda_summary_report.txt`:
- **Total Headcount:** 5,000 Employees
- **Active Employees:** 4,348 (86.96%)
- **Total Attrition:** 652 (13.04%)
- **Average Monthly Salary:** $10,017.48 (Median: $8,655.00)
- **Average Age:** 37.0 Years | **Average Company Tenure:** 3.4 Years
- **Gender Diversity:** 52.0% Male, 44.1% Female, 3.9% Non-Binary
- **Overtime Disparity:** 19.71% attrition among overtime workers vs 10.38% among non-overtime workers.

---

## 🖼 Visualizations Gallery

All 14 visualizations are rendered in 300 DPI high-resolution inside `outputs/charts/`:

| # | Visual Title | File Name | Key Analytical Takeaway |
| :-: | :--- | :--- | :--- |
| **1** | Headcount by Department | `01_workforce_demographics_by_department.png` | R&D represents 62.2% of workforce, Sales 30.9%, HR 7.0%. |
| **2** | Gender Distribution Donut | `02_gender_distribution_donut.png` | Balanced workforce diversity (52% M / 44% F / 4% NB). |
| **3** | Department Attrition Rate | `03_attrition_rate_by_department.png` | R&D (13.16%) and Sales (13.03%) exceed baseline average. |
| **4** | Attrition by Job Role | `04_attrition_by_job_role.png` | Sales Reps (15.5%) and Lab Techs (14.2%) lead turnover. |
| **5** | Monthly Income Distribution | `05_monthly_income_distribution_kde.png` | Right-skewed distribution with executive compensation tail. |
| **6** | Salary by Job Role Boxplot | `06_salary_by_job_role_boxplot.png` | Visualizes role compensation quartiles and executive spreads. |
| **7** | Overtime vs Attrition | `07_attrition_by_overtime_status.png` | Overtime staff experience nearly 2x higher attrition rate! |
| **8** | Age Group vs Turnover | `08_age_group_vs_attrition_rate.png` | Early career talent (<25) shows highest vulnerability (17.8%). |
| **9** | Job Satisfaction vs Attrition| `09_job_satisfaction_vs_attrition.png` | Attrition drops monotonically from 22.8% (Low) to 6.5% (Very High). |
| **10**| Work-Life Balance Impact | `10_work_life_balance_impact.png` | Poor work-life balance drives over 20.5% attrition. |
| **11**| Tenure vs Salary Scatter | `11_tenure_vs_monthly_income_scatter.png` | Regression trendline confirming steady tenure-based compensation growth. |
| **12**| Correlation Heatmap | `12_correlation_heatmap_matrix.png` | Pearson correlation matrix across 9 key workplace metrics. |
| **13**| Promotion Gap vs Churn | `13_years_since_promotion_vs_attrition.png` | Attrition spikes when promotion wait times exceed 4 years. |
| **14**| Appraisal Distribution | `14_performance_rating_by_department.png` | Cross-departmental breakdown of annual performance appraisal tiers. |

---

## 🗄 MySQL Relational Database & Advanced SQL

The `sql/` directory contains 5 comprehensive MySQL 8.0+ scripts:
- **`sql/01_create_database.sql`**: Schema creation with `utf8mb4` encoding.
- **`sql/02_create_tables.sql`**: Relational tables, CHECK constraints, and B-Tree indexes.
- **`sql/03_import_data.sql`**: High-performance CSV data loading scripts and sanity audits.
- **`sql/04_business_analysis.sql`**: 15 targeted queries answering core executive questions.
- **`sql/05_advanced_queries.sql`**: 15 advanced SQL queries featuring Window Functions, Multi-Table CTEs, and Star-Schema Joins.

### Core Business Questions Answered:
1. **Total Employee Count:** 5,000 verified unique employees.
2. **Largest Department:** Research & Development (3,109 employees, 62.18%).
3. **Overall Attrition Rate:** 13.04% (652 departures).
4. **Highest Attrition Department:** Research & Development (13.16%).
5. **Highest Paid Role:** Manager ($21,912.32 average monthly income).
6. **Average Monthly Salary:** $10,017.48.
7. **Average Company Tenure:** 3.44 Years.
8. **Age Group with Highest Churn:** `<25` Years (17.8% attrition).
9. **Overtime Impact:** Overtime `Yes` (19.71%) vs Overtime `No` (10.38%).
10. **Promotion Stagnation:** 382 active employees with >= 5 years without promotion.
11. **Highest Morale Department:** Research & Development (2.71 composite satisfaction).
12. **Workforce Gender Diversity:** 52.0% Male, 44.1% Female, 3.9% Non-Binary.
13. **Executive Earners:** Top 10 earners identified across Director and Manager titles.
14. **Appraisal Distribution:** 65% of workforce rated at Level 3 (Excellent).
15. **Retention Rate:** 86.96% organizational stability benchmark.

---

## 📊 Power BI Executive Dashboard

The Power BI solution is structured into **4 comprehensive dashboard pages**:
- **Page 1: HR Executive Overview** (High-level KPIs, divisional headcount, gender ratio, hiring trends).
- **Page 2: Attrition Analysis** (Overtime churn, role-based turnover, age bracket risks, tenure curves).
- **Page 3: Salary and Workforce Analysis** (Pay equity, experience scatter regression, educational background matrix).
- **Page 4: Performance and Satisfaction** (Morale breakdown, appraisal distribution, promotion stagnation flight-risk audit).

*Detailed layout specifications and manual creation steps are documented in [Dashboard_Design_Guide.md](powerbi/Dashboard_Design_Guide.md).*

---

## 📐 DAX Measures Reference

All 21 calculations are implemented as **Explicit DAX Measures** documented in [DAX_Measures.md](powerbi/DAX_Measures.md):
- `[Total Employees] = COUNTROWS('employees')`
- `[Active Employees] = CALCULATE(COUNTROWS('employees'), 'employees'[EmploymentStatus] = "Active")`
- `[Attrition Count] = CALCULATE(COUNTROWS('employees'), 'employees'[Attrition] = "Yes")`
- `[Attrition Rate] = DIVIDE([Attrition Count], [Total Employees], 0)`
- `[Employee Retention Rate] = DIVIDE([Active Employees], [Total Employees], 0)`
- `[Average Monthly Income] = AVERAGE('employees'[MonthlyIncome])`
- `[Overtime Attrition Rate] = CALCULATE([Attrition Rate], 'employees'[Overtime] = "Yes")`
- `[Early Tenure Attrition Rate] = CALCULATE([Attrition Rate], 'employees'[YearsAtCompany] <= 2)`
- `[Gender Pay Parity Ratio] = DIVIDE(FemaleAvgSalary, MaleAvgSalary, 1.0)`
- `[Stagnant Top Performers Count] = CALCULATE(COUNTROWS('employees'), 'employees'[EmploymentStatus] = "Active", 'employees'[PerformanceRating] >= 3, 'employees'[YearsSinceLastPromotion] >= 5)`

---

## 💡 Top Strategic Business Insights

Detailed executive recommendations are saved in [business_insights.md](documentation/business_insights.md):
1. **Overtime Doubled Attrition:** Overtime personnel face nearly 2x turnover (19.7% vs 10.4%). *Action:* Enforce workload thresholds and mandate quarterly capacity reviews.
2. **Early-Tenure Vulnerability:** 38% of departures happen in the first 24 months. *Action:* Overhaul onboarding into a structured 30-60-90 day milestone program with peer mentors.
3. **Promotion Stagnation Alert:** 382 active staff have had no promotion for 5+ years. *Action:* Implement bi-annual internal mobility calibrations and dual-track technical pathways.
4. **Equitable Compensation Parity:** Female-to-Male salary ratio stands at 0.99 across equivalent roles, serving as a powerful Employer Value Proposition (EVP) asset.

---

## ✅ Automated Testing & Verification

Automated test-driven validation is executed using **Pytest**:
```bash
pytest tests/test_data.py -v
```

### Test Results Summary:
```
tests/test_data.py::test_dataset_record_count PASSED                     [  7%]
tests/test_data.py::test_dataset_column_count PASSED                     [ 14%]
tests/test_data.py::test_employee_id_uniqueness PASSED                   [ 21%]
tests/test_data.py::test_employee_id_format PASSED                       [ 28%]
tests/test_data.py::test_zero_null_values PASSED                         [ 35%]
tests/test_data.py::test_required_columns_presence PASSED                [ 42%]
tests/test_data.py::test_tenure_within_total_experience PASSED           [ 50%]
tests/test_data.py::test_promotion_within_company_tenure PASSED          [ 57%]
tests/test_data.py::test_legal_working_age PASSED                        [ 64%]
tests/test_data.py::test_numerical_bounds PASSED                         [ 71%]
tests/test_data.py::test_categorical_domains PASSED                      [ 78%]
tests/test_data.py::test_all_14_charts_exist PASSED                      [ 85%]
tests/test_data.py::test_sql_scripts_exist PASSED                        [ 92%]
tests/test_data.py::test_powerbi_documentation_completeness PASSED       [100%]

======================== 14 passed in 4.61s ========================
```

---

## 🚀 Installation & Execution Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/HR-Employee-Analytics.git
cd HR-Employee-Analytics
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r python/requirements.txt
```

### 3. Run the Data Pipeline
```bash
# Generate synthetic dataset (5,000 records)
python python/generate_dataset.py

# Execute cleaning, imputation, and validation sequence
python python/data_cleaning.py

# Run exploratory statistical profiling
python python/eda_analysis.py

# Generate all 14 corporate charts
python python/data_visualization.py

# Validate SQL query logic
python python/validate_sql.py

# Run automated QA test suite
pytest tests/test_data.py -v
```

### 4. MySQL Setup
1. Launch MySQL Server / Workbench.
2. Execute scripts in sequence:
   - `sql/01_create_database.sql`
   - `sql/02_create_tables.sql`
   - `sql/03_import_data.sql`
   - `sql/04_business_analysis.sql`
   - `sql/05_advanced_queries.sql`

### 5. Power BI Desktop Implementation
1. Open Microsoft Power BI Desktop.
2. Import `dataset/cleaned_employee_data.csv`.
3. Follow the layout blueprints and DAX measures in [powerbi/](powerbi/).

---

## 📁 Repository File Structure

```
HR-Employee-Analytics/
│
├── dataset/
│   ├── raw_employee_data.csv           # 5,010 raw records with controlled anomalies
│   └── cleaned_employee_data.csv       # 5,000 validated production employee records
│
├── python/
│   ├── generate_dataset.py             # Reproducible synthetic data generation (seed=42)
│   ├── data_cleaning.py                # Enterprise cleaning, imputation, and validation
│   ├── eda_analysis.py                 # Statistical profiling & summary report generator
│   ├── data_visualization.py           # Generates 14 publication-grade visual charts
│   ├── validate_sql.py                 # Automated SQL logic verification script
│   ├── create_notebook.py              # Jupyter notebook generator utility
│   ├── requirements.txt                # Python library dependencies
│   └── notebooks/
│       └── HR_Analytics_EDA.ipynb      # Interactive Jupyter exploratory notebook
│
├── sql/
│   ├── 01_create_database.sql          # Database initialization & collation
│   ├── 02_create_tables.sql            # Master table, Star Schema dimensions, indices
│   ├── 03_import_data.sql              # LOAD DATA INFILE & verification queries
│   ├── 04_business_analysis.sql        # 15 targeted business questions resolved
│   └── 05_advanced_queries.sql         # 15 Window Functions, CTEs, and Star Joins
│
├── powerbi/
│   ├── DAX_Measures.md                 # 21 explicit DAX formulas with business context
│   └── Dashboard_Design_Guide.md       # 4-page dashboard blueprint & step-by-step build
│
├── outputs/
│   ├── charts/                         # 14 High-resolution (300 DPI) corporate charts
│   │   ├── 01_workforce_demographics_by_department.png
│   │   ├── 02_gender_distribution_donut.png
│   │   ├── 03_attrition_rate_by_department.png
│   │   ├── 04_attrition_by_job_role.png
│   │   ├── 05_monthly_income_distribution_kde.png
│   │   ├── 06_salary_by_job_role_boxplot.png
│   │   ├── 07_attrition_by_overtime_status.png
│   │   ├── 08_age_group_vs_attrition_rate.png
│   │   ├── 09_job_satisfaction_vs_attrition.png
│   │   ├── 10_work_life_balance_impact.png
│   │   ├── 11_tenure_vs_monthly_income_scatter.png
│   │   ├── 12_correlation_heatmap_matrix.png
│   │   ├── 13_years_since_promotion_vs_attrition.png
│   │   └── 14_performance_rating_by_department.png
│   └── reports/
│       ├── data_cleaning_report.txt    # Data cleaning audit log
│       └── eda_summary_report.txt      # Comprehensive EDA summary report
│
├── documentation/
│   ├── project_overview.md             # Project background, architecture, and objectives
│   ├── data_dictionary.md              # Column schemas, domains, and data types
│   ├── methodology.md                  # Statistical, data cleaning, and BI methodology
│   ├── business_insights.md            # 12 strategic HR insights and action items
│   ├── powerbi_guide.md                # Power BI modeling, RLS, and user guide
│   ├── sql_explanations.md             # Detailed explanations of all SQL queries
│   └── interview_questions.md          # 35 interview Q&A, elevator pitches & resume points
│
├── tests/
│   └── test_data.py                    # 14 Pytest automated quality assurance tests
│
├── .gitignore                          # Standard Python / IDE ignore rules
├── LICENSE                             # MIT Open Source License
└── README.md                           # Recruiter-facing portfolio documentation
```

---

## 🎯 Resume & Interview Presentation Guide

### 2-Minute Elevator Pitch
> *"I developed an end-to-end HR Employee Analytics project analyzing 5,000 workforce records to uncover why employees leave and how to optimize retention. In Python, I built an automated cleaning pipeline with context-aware imputation and IQR outlier detection. In MySQL 8.0, I architected a star-schema database and authored over 30 advanced SQL queries utilizing Window Functions like DENSE_RANK and multi-table CTEs. Finally, I designed a 4-page Power BI dashboard with 21 explicit DAX measures, uncovering that overtime workers experience nearly 2x higher attrition (19.7% vs 10.4%) and identifying 382 promotion-stagnant employees. This project demonstrates my hands-on mastery of the full data lifecycle from raw data ingestion to executive storytelling."*

*Full interview preparation with 35 detailed technical Q&As is available in [documentation/interview_questions.md](documentation/interview_questions.md).*

---

## 🔮 Future Improvements

1. **Machine Learning Predictive Churn Model:** Train a Random Forest or XGBoost classification model to predict individual flight-risk probability and SHAP explainability.
2. **Continuous Integration (CI):** Integrate GitHub Actions to run `pytest` automated tests on every pull request.
3. **Automated ETL Pipeline:** Build an Apache Airflow or Prefect workflow to orchestrate scheduled data synchronization from an HRIS API directly into MySQL and Power BI.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
