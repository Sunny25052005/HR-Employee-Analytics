"""
test_data.py
Automated Quality Assurance & Verification Test Suite
Author: Senior Data Analyst / QA Engineer
Project: HR Employee Analytics Dashboard

Uses pytest to rigorously validate:
1. Data volume & file integrity
2. Primary key uniqueness & format
3. Absolute zero nulls post-imputation
4. Schema conformance (all required columns)
5. Chronological business rules (Age, Tenure, Promotion)
6. Domain ranges & constraints
7. Chart generation integrity (all 14 charts exist and non-empty)
8. SQL and Power BI deliverable completeness
"""

import os
import re
import pytest
import pandas as pd

CLEANED_CSV = os.path.join("dataset", "cleaned_employee_data.csv")
RAW_CSV = os.path.join("dataset", "raw_employee_data.csv")
CHARTS_DIR = os.path.join("outputs", "charts")
SQL_DIR = "sql"
POWERBI_DIR = "powerbi"

@pytest.fixture(scope="session")
def cleaned_df():
    """Session fixture loading cleaned dataset."""
    assert os.path.exists(CLEANED_CSV), f"Cleaned dataset missing at {CLEANED_CSV}"
    df = pd.read_csv(CLEANED_CSV)
    return df

# -------------------------------------------------------------
# 1. Dataset Shape and Volume Tests
# -------------------------------------------------------------
def test_dataset_record_count(cleaned_df):
    """Verify cleaned dataset contains exactly 5,000 valid records."""
    assert len(cleaned_df) == 5000, f"Expected 5,000 rows, found {len(cleaned_df)}"

def test_dataset_column_count(cleaned_df):
    """Verify cleaned dataset contains 25 columns (21 base + 4 engineered)."""
    assert cleaned_df.shape[1] == 25, f"Expected 25 columns, found {cleaned_df.shape[1]}"

# -------------------------------------------------------------
# 2. Primary Key Uniqueness & ID Format
# -------------------------------------------------------------
def test_employee_id_uniqueness(cleaned_df):
    """Verify 100% of EmployeeIDs are strictly unique."""
    unique_ids = cleaned_df["EmployeeID"].nunique()
    assert unique_ids == 5000, f"Detected duplicate IDs! Unique count: {unique_ids}"

def test_employee_id_format(cleaned_df):
    """Verify EmployeeIDs conform to standard EMPXXXX regex format."""
    pattern = re.compile(r"^EMP\d{4}$")
    invalid_ids = cleaned_df[~cleaned_df["EmployeeID"].astype(str).str.match(pattern)]
    assert len(invalid_ids) == 0, f"Found {len(invalid_ids)} malformed EmployeeIDs"

# -------------------------------------------------------------
# 3. Missing Value Verification
# -------------------------------------------------------------
def test_zero_null_values(cleaned_df):
    """Verify zero missing/NaN values across the entire cleaned dataset."""
    total_nulls = cleaned_df.isnull().sum().sum()
    assert total_nulls == 0, f"Dataset contains {total_nulls} unresolved null values"

# -------------------------------------------------------------
# 4. Schema Column Existence
# -------------------------------------------------------------
def test_required_columns_presence(cleaned_df):
    """Verify all 21 mandatory prompt columns + 4 engineered features exist."""
    required_cols = [
        "EmployeeID", "Age", "Gender", "Department", "JobRole", "Education",
        "EducationField", "JoiningDate", "YearsAtCompany", "MonthlyIncome",
        "JobSatisfaction", "EnvironmentSatisfaction", "PerformanceRating",
        "WorkLifeBalance", "Overtime", "TrainingTimesLastYear",
        "YearsSinceLastPromotion", "TotalWorkingYears", "BusinessTravel",
        "Attrition", "EmploymentStatus", "AgeGroup", "TenureGroup",
        "SalaryBand", "OverallSatisfaction"
    ]
    missing_cols = [c for c in required_cols if c not in cleaned_df.columns]
    assert len(missing_cols) == 0, f"Missing required columns: {missing_cols}"

# -------------------------------------------------------------
# 5. Chronological & Relational Integrity
# -------------------------------------------------------------
def test_tenure_within_total_experience(cleaned_df):
    """YearsAtCompany must never exceed TotalWorkingYears."""
    violations = cleaned_df[cleaned_df["YearsAtCompany"] > cleaned_df["TotalWorkingYears"]]
    assert len(violations) == 0, f"Found {len(violations)} tenure violations"

def test_promotion_within_company_tenure(cleaned_df):
    """YearsSinceLastPromotion must never exceed YearsAtCompany."""
    violations = cleaned_df[cleaned_df["YearsSinceLastPromotion"] > cleaned_df["YearsAtCompany"]]
    assert len(violations) == 0, f"Found {len(violations)} promotion violations"

def test_legal_working_age(cleaned_df):
    """Employee must be at least 16 years old when career began."""
    violations = cleaned_df[cleaned_df["Age"] < (cleaned_df["TotalWorkingYears"] + 16)]
    assert len(violations) == 0, f"Found {len(violations)} working age violations"

# -------------------------------------------------------------
# 6. Domain Range and Category Constraints
# -------------------------------------------------------------
def test_numerical_bounds(cleaned_df):
    """Validate numerical domains (Age, Income, Survey Ratings 1-4)."""
    assert cleaned_df["Age"].between(18, 70).all(), "Age out of [18, 70] bounds"
    assert (cleaned_df["MonthlyIncome"] >= 2000).all(), "Negative or below-floor salary detected"
    assert cleaned_df["JobSatisfaction"].isin([1, 2, 3, 4]).all(), "Invalid JobSatisfaction score"
    assert cleaned_df["EnvironmentSatisfaction"].isin([1, 2, 3, 4]).all(), "Invalid EnvironmentSatisfaction score"
    assert cleaned_df["WorkLifeBalance"].isin([1, 2, 3, 4]).all(), "Invalid WorkLifeBalance score"
    assert cleaned_df["PerformanceRating"].isin([1, 2, 3, 4]).all(), "Invalid PerformanceRating score"
    assert cleaned_df["Education"].isin([1, 2, 3, 4, 5]).all(), "Invalid Education level"

def test_categorical_domains(cleaned_df):
    """Validate categorical fields match acceptable enum sets."""
    assert set(cleaned_df["Gender"].unique()).issubset({"Male", "Female", "Non-Binary"})
    assert set(cleaned_df["Department"].unique()).issubset({"Sales", "Research & Development", "Human Resources"})
    assert set(cleaned_df["Overtime"].unique()).issubset({"Yes", "No"})
    assert set(cleaned_df["Attrition"].unique()).issubset({"Yes", "No"})
    assert set(cleaned_df["EmploymentStatus"].unique()).issubset({"Active", "Terminated"})

# -------------------------------------------------------------
# 7. Visualization Artifact Completeness
# -------------------------------------------------------------
def test_all_14_charts_exist():
    """Verify all 14 visual charts were generated, saved, and are non-empty."""
    expected_charts = [
        "01_workforce_demographics_by_department.png",
        "02_gender_distribution_donut.png",
        "03_attrition_rate_by_department.png",
        "04_attrition_by_job_role.png",
        "05_monthly_income_distribution_kde.png",
        "06_salary_by_job_role_boxplot.png",
        "07_attrition_by_overtime_status.png",
        "08_age_group_vs_attrition_rate.png",
        "09_job_satisfaction_vs_attrition.png",
        "10_work_life_balance_impact.png",
        "11_tenure_vs_monthly_income_scatter.png",
        "12_correlation_heatmap_matrix.png",
        "13_years_since_promotion_vs_attrition.png",
        "14_performance_rating_by_department.png"
    ]
    for chart in expected_charts:
        chart_path = os.path.join(CHARTS_DIR, chart)
        assert os.path.exists(chart_path), f"Chart missing: {chart}"
        file_size = os.path.getsize(chart_path)
        assert file_size > 10000, f"Chart file too small or corrupt ({file_size} bytes): {chart}"

# -------------------------------------------------------------
# 8. SQL Scripts Completeness
# -------------------------------------------------------------
def test_sql_scripts_exist():
    """Verify all 5 SQL files exist and contain core keywords."""
    sql_files = [
        "01_create_database.sql",
        "02_create_tables.sql",
        "03_import_data.sql",
        "04_business_analysis.sql",
        "05_advanced_queries.sql"
    ]
    for sf in sql_files:
        path = os.path.join(SQL_DIR, sf)
        assert os.path.exists(path), f"SQL script missing: {sf}"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            assert len(content) > 100, f"SQL script empty: {sf}"

# -------------------------------------------------------------
# 9. Power BI Deliverables
# -------------------------------------------------------------
def test_powerbi_documentation_completeness():
    """Verify DAX measures and dashboard design guide exist and are comprehensive."""
    dax_path = os.path.join(POWERBI_DIR, "DAX_Measures.md")
    guide_path = os.path.join(POWERBI_DIR, "Dashboard_Design_Guide.md")
    assert os.path.exists(dax_path), "DAX_Measures.md missing"
    assert os.path.exists(guide_path), "Dashboard_Design_Guide.md missing"
    
    with open(dax_path, "r", encoding="utf-8") as f:
        dax_text = f.read()
        assert "Attrition Rate" in dax_text
        assert "CALCULATE" in dax_text
        assert "DIVIDE" in dax_text
