# Analytics Methodology & Technical Architecture

**Project:** HR Employee Analytics Dashboard  
**Author:** Senior Data Analyst & Project Lead  
**Scope:** Engineering, Statistical, and BI Methodologies  

---

## 1. Project Lifecycle & Data Engineering Architecture

The project adheres to the standard **CRISP-DM (Cross-Industry Standard Process for Data Mining)** and modern analytics engineering frameworks.

```
[ Raw Data Ingestion ] ──► [ Automated Cleaning & Validation ] ──► [ Feature Engineering ]
                                                                             │
       ┌─────────────────────────────────────────────────────────────────────┘
       ▼
[ Relational Warehousing (MySQL) ] ──► [ Exploratory Profiling (EDA) ] ──► [ Executive BI (Power BI) ]
```

### 1.1 Data Ingestion & Synthetic Generation Pipeline
- **Reproducibility Guarantee:** All synthetic data generation scripts (`python/generate_dataset.py`) execute under an immutable pseudorandom seed (`np.random.seed(42)`).
- **Domain Realism Modeling:**
  - Age generated using a normal distribution bounded between 20 and 60 years ($\mu = 37.2, \sigma = 8.8$).
  - Total working experience and company tenure generated conditionally:
    $$\text{TotalWorkingYears} \le \text{Age} - 18$$
    $$\text{YearsAtCompany} \le \text{TotalWorkingYears}$$
    $$\text{YearsSinceLastPromotion} \le \text{YearsAtCompany}$$
  - Monthly compensation is anchored to role baselines with non-linear multipliers for experience and education.
  - Attrition risk is modeled probabilistically based on combined risk weights (Overtime, Low Satisfaction, Low Work-Life Balance, Low Income, Promotion Stagnation).

---

## 2. Enterprise Data Cleaning & Imputation Protocol

The data cleaning pipeline (`python/data_cleaning.py`) implements a multi-stage validation sequence:

### 2.1 Deduplication
- Primary key uniqueness constraint enforced on `EmployeeID`.
- Duplicates identified via `df.duplicated(subset=['EmployeeID'])` and eliminated, preserving first recorded instance.

### 2.2 Context-Aware Imputation Strategy
- **Continuous Variables (`MonthlyIncome`):** Imputed using the **median** grouped by `JobRole` to avoid distorting role-specific salary benchmarks.
- **Categorical Variables (`EducationField`):** Imputed using the **mode** within the employee's respective `Department`.
- **Ordinal Survey Ratings (`WorkLifeBalance`):** Imputed using the global mode.

### 2.3 Chronological & Boundary Verification
- Standardized all dates to ISO `YYYY-MM-DD`.
- Enforced hard chronological constraints:
  - If `YearsAtCompany > TotalWorkingYears`, `TotalWorkingYears` is adjusted to equal `YearsAtCompany`.
  - If `YearsSinceLastPromotion > YearsAtCompany`, promotion years is capped at company tenure.
  - Enforced minimum legal working age (`Age >= TotalWorkingYears + 16`).

### 2.4 Outlier Analysis via Interquartile Range (IQR)
Outliers are evaluated using Tukey's method:
$$\text{IQR} = Q_3 - Q_1$$
$$\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR}$$
$$\text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}$$
Outliers identified in `MonthlyIncome` were retained because they represent legitimate executive leadership compensation rather than instrumentation errors.

---

## 3. Relational Database & Star Schema Modeling

### 3.1 Schema Design
To support analytical agility and enterprise BI ingestion, the data model supports both:
1. **Flat Reporting Master Table (`employees`):** High-speed tabular queries without expensive join overhead.
2. **Normalized Star Schema (`dim_department`, `dim_job_role`, `dim_education`):** Dimensional model for enterprise data warehousing standards.

### 3.2 Indexing Strategy
Indices created on high-cardinality filtering and join attributes:
- `idx_emp_dept` on `Department`
- `idx_emp_role` on `JobRole`
- `idx_emp_attrition` on `Attrition`
- `idx_emp_status` on `EmploymentStatus`
- `idx_emp_income` on `MonthlyIncome`

---

## 4. Business Intelligence & DAX Modeling Methodology

### 4.1 Filter Context vs Row Context
- All metrics are calculated as **Explicit DAX Measures** to preserve dynamic filter context.
- Measures using `CALCULATE` modify the filter context dynamically based on visual slices and report filters.
- Zero-safe division handled via `DIVIDE(Numerator, Denominator, 0)`.

### 4.2 Dashboard Visual Hierarchy & UX Principles
- **Top-to-Bottom, Left-to-Right:** Key Performance Indicator (KPI) cards are prioritized at the top, leading into macro distributions, followed by granular analytical cross-tabs.
- **Color Consistency:**
  - Navy (`#1E3A8A`): Primary volume and corporate baseline.
  - Crimson (`#DC2626`): Strictly reserved for attrition, terminations, and critical risk flags.
  - Teal (`#0D9488`): Active workforce and positive benchmarks.
- **Slicer Centralization:** Persistent left-hand filter navigation panel ensuring unified interactivity across all pages.

---

## 5. Automated Testing & Verification Framework
- Implemented with **Pytest** in `tests/test_data.py`.
- Automated test suites validate:
  1. Record count equals expected threshold (5,000 records).
  2. 100% uniqueness of `EmployeeID`.
  3. Absolute zero missing/null values across all columns.
  4. Validity of chronological constraints (`YearsAtCompany <= TotalWorkingYears`).
  5. Value bounds on categorical attributes and survey ratings (1 to 4 scale).
  6. Financial bounds (No negative or below-minimum wages).
