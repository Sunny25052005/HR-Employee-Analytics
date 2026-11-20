"""
generate_dataset.py
Generates a realistic synthetic HR Employee dataset with 5,000 records.
Uses a fixed random seed for 100% reproducibility.
Introduces controlled anomalies into the raw dataset to demonstrate
professional data cleaning and preprocessing pipelines.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_hr_dataset(num_records=5000, seed=42):
    np.random.seed(seed)

    # 1. Employee IDs
    emp_ids = [f"EMP{str(i).zfill(4)}" for i in range(1, num_records + 1)]

    # 2. Gender distribution (~52% Male, ~44% Female, ~4% Non-Binary)
    genders = np.random.choice(["Male", "Female", "Non-Binary"], size=num_records, p=[0.52, 0.44, 0.04])

    # 3. Department & Job Roles mapping
    dept_roles = {
        "Sales": [
            ("Sales Executive", 0.55),
            ("Sales Representative", 0.35),
            ("Manager", 0.10)
        ],
        "Research & Development": [
            ("Research Scientist", 0.35),
            ("Laboratory Technician", 0.30),
            ("Manufacturing Director", 0.15),
            ("Healthcare Representative", 0.10),
            ("Research Director", 0.05),
            ("Manager", 0.05)
        ],
        "Human Resources": [
            ("Human Resources", 0.80),
            ("Manager", 0.20)
        ]
    }

    # Department probabilities (~60% R&D, ~33% Sales, ~7% HR)
    dept_choices = ["Research & Development", "Sales", "Human Resources"]
    dept_probs = [0.60, 0.33, 0.07]
    departments = np.random.choice(dept_choices, size=num_records, p=dept_probs)

    job_roles = []
    for dept in departments:
        roles, probs = zip(*dept_roles[dept])
        job_roles.append(np.random.choice(roles, p=probs))

    # 4. Age distribution (Beta/Normal distributed between 20 and 60, mean ~37)
    ages = np.clip(np.random.normal(loc=37.2, scale=8.8, size=num_records).astype(int), 20, 60)

    # 5. Education level (1 to 5) and Field
    edu_levels = np.random.choice([1, 2, 3, 4, 5], size=num_records, p=[0.12, 0.20, 0.40, 0.24, 0.04])
    edu_fields_pool = ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"]
    
    edu_fields = []
    for dept in departments:
        if dept == "Sales":
            f = np.random.choice(edu_fields_pool, p=[0.20, 0.10, 0.45, 0.15, 0.02, 0.08])
        elif dept == "Research & Development":
            f = np.random.choice(edu_fields_pool, p=[0.45, 0.35, 0.02, 0.12, 0.01, 0.05])
        else:
            f = np.random.choice(edu_fields_pool, p=[0.05, 0.05, 0.05, 0.05, 0.70, 0.10])
        edu_fields.append(f)

    # 6. Experience calculations
    # TotalWorkingYears must be realistic based on age and education
    # Minimum starting age: ~18 for High school, ~22 for Bachelor's, ~24 for Master's, ~27 for PhD
    min_start_ages = {1: 18, 2: 20, 3: 22, 4: 24, 5: 27}
    
    total_working_years = []
    years_at_company = []
    years_since_promotion = []
    joining_dates = []

    reference_date = datetime(2024, 6, 30)

    for i in range(num_records):
        age = ages[i]
        edu = edu_levels[i]
        min_start = min_start_ages[edu]
        max_possible_work = max(0, age - min_start)
        
        twy = int(np.clip(np.random.normal(loc=max_possible_work * 0.75, scale=3), 0, max_possible_work))
        total_working_years.append(twy)

        # Years at company cannot exceed total working years
        max_yac = min(twy, 40)
        if max_yac == 0:
            yac = 0
        else:
            # Tenure tends to skew lower (exponential / beta)
            yac = int(np.clip(np.random.exponential(scale=5.0), 0, max_yac))
        years_at_company.append(yac)

        # Joining date derived from years at company
        days_at_company = int(yac * 365.25 + np.random.randint(0, 365))
        join_dt = reference_date - timedelta(days=days_at_company)
        joining_dates.append(join_dt.strftime("%Y-%m-%d"))

        # Years since last promotion <= years at company
        if yac == 0:
            ysp = 0
        else:
            ysp = int(np.random.uniform(0, yac))
        years_since_promotion.append(ysp)

    # 7. Salary calculation based on Role, Experience, and Education
    base_salaries = {
        "Sales Representative": 3200,
        "Laboratory Technician": 3500,
        "Human Resources": 4500,
        "Research Scientist": 5500,
        "Sales Executive": 6800,
        "Manufacturing Director": 9000,
        "Healthcare Representative": 8800,
        "Research Director": 14000,
        "Manager": 15000
    }

    monthly_incomes = []
    for i in range(num_records):
        role = job_roles[i]
        twy = total_working_years[i]
        edu = edu_levels[i]
        base = base_salaries[role]
        
        # Increments per year of experience and education level
        exp_multiplier = 1 + (twy * 0.04)
        edu_bonus = (edu - 1) * 300
        noise = np.random.normal(loc=0, scale=400)
        
        salary = int(base * exp_multiplier + edu_bonus + noise)
        salary = max(2200, round(salary, -1)) # minimum salary floor $2,200
        monthly_incomes.append(salary)

    # 8. Workplace factors
    job_satisfaction = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.15, 0.25, 0.35, 0.25])
    env_satisfaction = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.16, 0.24, 0.34, 0.26])
    work_life_balance = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.10, 0.30, 0.45, 0.15])
    performance_rating = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.05, 0.15, 0.65, 0.15])
    overtime = np.random.choice(["Yes", "No"], size=num_records, p=[0.28, 0.72])
    training_times = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=num_records, p=[0.05, 0.15, 0.35, 0.25, 0.12, 0.05, 0.03])
    business_travel = np.random.choice(["Travel_Rarely", "Travel_Frequently", "Non-Travel"], size=num_records, p=[0.70, 0.19, 0.11])

    # 9. Realistic Attrition Risk Modeling
    # Attrition is driven by: Overtime, Low Satisfaction, Low WorkLifeBalance, Low Income, High Travel, Long time without promotion
    attrition = []
    employment_status = []

    for i in range(num_records):
        score = 0.0
        if overtime[i] == "Yes":
            score += 0.30
        if job_satisfaction[i] == 1:
            score += 0.30
        elif job_satisfaction[i] == 2:
            score += 0.15
        if work_life_balance[i] == 1:
            score += 0.25
        if env_satisfaction[i] == 1:
            score += 0.15
        if business_travel[i] == "Travel_Frequently":
            score += 0.20
        if years_since_promotion[i] >= 5:
            score += 0.15
        if monthly_incomes[i] < 4500:
            score += 0.20
        if ages[i] < 30:
            score += 0.15
        if years_at_company[i] <= 2:
            score += 0.15

        # Base attrition probability ~ 4%, max ~ 45% based on risk score
        prob = 0.04 + (score * 0.22)
        prob = min(0.60, prob)
        
        is_attrition = np.random.rand() < prob
        if is_attrition:
            attrition.append("Yes")
            employment_status.append("Terminated")
        else:
            attrition.append("No")
            employment_status.append("Active")

    df = pd.DataFrame({
        "EmployeeID": emp_ids,
        "Age": ages,
        "Gender": genders,
        "Department": departments,
        "JobRole": job_roles,
        "Education": edu_levels,
        "EducationField": edu_fields,
        "JoiningDate": joining_dates,
        "YearsAtCompany": years_at_company,
        "MonthlyIncome": monthly_incomes,
        "JobSatisfaction": job_satisfaction,
        "EnvironmentSatisfaction": env_satisfaction,
        "PerformanceRating": performance_rating,
        "WorkLifeBalance": work_life_balance,
        "Overtime": overtime,
        "TrainingTimesLastYear": training_times,
        "YearsSinceLastPromotion": years_since_promotion,
        "TotalWorkingYears": total_working_years,
        "BusinessTravel": business_travel,
        "Attrition": attrition,
        "EmploymentStatus": employment_status
    })

    # To realistically simulate raw industry data that requires data cleaning:
    # 1. Add 10 duplicate rows at the end
    duplicates = df.iloc[np.random.choice(df.index, size=10)].copy()
    
    # 2. Inject a few missing values in selected columns (<0.5%)
    raw_df = pd.concat([df, duplicates], ignore_index=True)
    
    # Introduce controlled NaNs in raw dataset
    nan_indices_salary = np.random.choice(raw_df.index, size=12, replace=False)
    raw_df.loc[nan_indices_salary, "MonthlyIncome"] = np.nan
    
    nan_indices_edu = np.random.choice(raw_df.index, size=8, replace=False)
    raw_df.loc[nan_indices_edu, "EducationField"] = np.nan

    nan_indices_wlb = np.random.choice(raw_df.index, size=10, replace=False)
    raw_df.loc[nan_indices_wlb, "WorkLifeBalance"] = np.nan

    # Add a few inconsistent string whitespaces
    ws_indices = np.random.choice(raw_df.index, size=15, replace=False)
    raw_df.loc[ws_indices, "Department"] = raw_df.loc[ws_indices, "Department"].apply(lambda x: f"  {x}  ")

    return raw_df, df

if __name__ == "__main__":
    import os
    os.makedirs("dataset", exist_ok=True)
    raw_df, clean_truth = generate_hr_dataset(5000, seed=42)
    raw_path = os.path.join("dataset", "raw_employee_data.csv")
    raw_df.to_csv(raw_path, index=False)
    print(f"Dataset generated successfully at: {raw_path}")
    print(f"Total raw rows: {len(raw_df)}, Columns: {len(raw_df.columns)}")
    print(f"Sample data:\n{raw_df.head(3)}")
