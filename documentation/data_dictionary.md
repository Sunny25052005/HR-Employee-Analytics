# Comprehensive Data Dictionary & Schema Documentation

**Project:** HR Employee Analytics Dashboard  
**Dataset Reference:** `dataset/cleaned_employee_data.csv` (and `dataset/raw_employee_data.csv`)  
**Scope:** 5,000 Verified Employee Records  
**Schema Standard:** 3NF / Dimensional Star Schema  

---

## 1. Master Employee Table Schema (`employees`)

| Column Name | SQL Type | Python Dtype | Nullable | Description & Domain / Values | Sample Values | Business Significance |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **`EmployeeID`** | `VARCHAR(20)` | `string` | **No** | Unique alphanumeric employee identifier. Constraint: `PK, Unique` | `EMP0001`, `EMP0452` | Primary entity key for workforce identity tracking. |
| **`Age`** | `INT` | `int64` | **No** | Chronological employee age. Domain: `18 <= Age <= 70` | `28`, `42`, `55` | Generational cohort segmentation and retirement forecasting. |
| **`Gender`** | `VARCHAR(20)` | `string` | **No** | Gender identity. Domain: `['Male', 'Female', 'Non-Binary']` | `Male`, `Female` | Diversity, Equity, and Inclusion (DEI) monitoring. |
| **`Department`** | `VARCHAR(50)` | `string` | **No** | Primary operational division. Domain: `['Research & Development', 'Sales', 'Human Resources']` | `Research & Development` | Divisional headcount and organizational budgeting. |
| **`JobRole`** | `VARCHAR(50)` | `string` | **No** | Functional title. 9 Distinct titles across divisions. | `Research Scientist`, `Sales Executive` | Granular role-based compensation and turnover analysis. |
| **`Education`** | `INT` | `int64` | **No** | Formal education level code. Domain: `1 to 5` (1: High School, 2: College, 3: Bachelor, 4: Master, 5: PhD) | `3`, `4` | Human capital qualification mapping. |
| **`EducationField`** | `VARCHAR(50)` | `string` | **No** | Major degree specialization. Domain: `['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other']` | `Life Sciences`, `Medical` | Talent recruitment alignment with academic discipline. |
| **`JoiningDate`** | `DATE` | `object (date)` | **No** | Official date of organizational onboarding. Format: `YYYY-MM-DD` | `2018-04-12` | Historical hiring velocity and cohort retention tracking. |
| **`YearsAtCompany`** | `INT` | `int64` | **No** | Total completed years of tenure with the organization. Constraint: `<= TotalWorkingYears` | `2`, `5`, `12` | Employee loyalty, institutional retention, and vesting. |
| **`MonthlyIncome`** | `DECIMAL(10,2)` | `float64` | **No** | Gross monthly compensation in USD. Domain: `$2,200 to $25,000+` | `6450.00`, `14200.00` | Payroll analytics, wage equity, and cost-of-turnover modeling. |
| **`JobSatisfaction`** | `INT` | `int64` | **No** | Employee self-reported job fulfillment. Domain: `1 (Low) to 4 (Very High)` | `1`, `2`, `3`, `4` | Key emotional leading indicator for flight risk. |
| **`EnvironmentSatisfaction`** | `INT` | `int64` | **No** | Rating of workplace culture and facilities. Domain: `1 (Low) to 4 (Very High)` | `2`, `3` | Physical and managerial workplace climate health. |
| **`PerformanceRating`** | `INT` | `int64` | **No** | Annual performance appraisal score. Domain: `1 (Low), 2 (Good), 3 (Excellent), 4 (Outstanding)` | `3`, `4` | Talent management, merit compensation, and promotion calibration. |
| **`WorkLifeBalance`** | `INT` | `int64` | **No** | Perceived equilibrium between work and personal life. Domain: `1 (Bad) to 4 (Best)` | `1`, `2`, `3`, `4` | Critical burnout metric and schedule sustainability. |
| **`Overtime`** | `VARCHAR(5)` | `string` | **No** | Whether the employee regularly works overtime. Domain: `['Yes', 'No']` | `Yes`, `No` | Workload intensity; strong statistical predictor of voluntary churn. |
| **`TrainingTimesLastYear`** | `INT` | `int64` | **No** | Count of formal training programs attended in the preceding 12 months. Domain: `0 to 6` | `2`, `3` | Employee upskilling and learning investment ROI. |
| **`YearsSinceLastPromotion`** | `INT` | `int64` | **No** | Years elapsed since the employee's last promotion. Constraint: `<= YearsAtCompany` | `1`, `4`, `7` | Career progression velocity and promotion stagnation audit. |
| **`TotalWorkingYears`** | `INT` | `int64` | **No** | Lifetime cumulative working experience across all employers. Constraint: `>= YearsAtCompany` | `6`, `15` | Total industry seniority and experience profiling. |
| **`BusinessTravel`** | `VARCHAR(30)` | `string` | **No** | Frequency of job-related travel. Domain: `['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']` | `Travel_Rarely` | Travel fatigue and role mobility demands. |
| **`Attrition`** | `VARCHAR(5)` | `string` | **No** | Whether the employee has separated from the organization. Domain: `['Yes', 'No']` | `Yes`, `No` | Primary target dependent variable for turnover analytics. |
| **`EmploymentStatus`** | `VARCHAR(20)` | `string` | **No** | Current operational status. Domain: `['Active', 'Terminated']` | `Active`, `Terminated` | Filter attribute separating current staff from historical exits. |

---

## 2. Engineered Analytical Cohorts (Derived Features)

| Feature Name | Dtype | Derivation Logic | Category Labels / Output Range | Business Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`AgeGroup`** | `Categorical` | Binned from `Age` | `['<25', '25-34', '35-44', '45-54', '55+']` | Segmenting workforce by generational life stages. |
| **`TenureGroup`** | `Categorical` | Binned from `YearsAtCompany` | `['0-2 Years', '3-5 Years', '6-10 Years', '10+ Years']` | Diagnosing early-career vs mid-tenure vs veteran turnover. |
| **`SalaryBand`** | `Categorical` | Binned from `MonthlyIncome` | `['Entry (<$5K)', 'Mid ($5K-$10K)', 'Senior ($10K-$15K)', 'Executive (>$15K)']` | Compensation tier grouping for Power BI filtering. |
| **`OverallSatisfaction`**| `Float` | `(JobSat + EnvSat + WLB) / 3.0` | `1.00 to 4.00` | Composite metric summarizing total employee morale. |

---

## 3. Dimensional Lookup Tables (Star Schema)

### Table: `dim_education`
- **`EducationLevelID`** (`INT`, PK): Values `1, 2, 3, 4, 5`.
- **`EducationDegree`** (`VARCHAR(50)`): Descriptive qualification title (`High School / Below College`, `Associate Degree / College`, `Bachelor Degree`, `Master Degree`, `Doctorate / PhD`).

### Table: `dim_department`
- **`DepartmentID`** (`INT`, PK, Auto-increment).
- **`DepartmentName`** (`VARCHAR(50)`, Unique): Values `Research & Development`, `Sales`, `Human Resources`.

### Table: `dim_job_role`
- **`JobRoleID`** (`INT`, PK, Auto-increment).
- **`JobRoleName`** (`VARCHAR(50)`, Unique): 9 Distinct role titles.
- **`StandardSalaryFloor`** (`DECIMAL(10,2)`): Role-specific base compensation threshold.
