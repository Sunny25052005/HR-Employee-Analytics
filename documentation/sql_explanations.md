# Relational Database Architecture & SQL Analytical Explanations

**Project:** HR Employee Analytics Dashboard  
**Database System:** MySQL 8.0+  
**Schema:** `hr_analytics`  
**Author:** Senior SQL Developer & Data Analyst  

---

## 1. Relational Database Overview & File Architecture
The SQL suite comprises 5 production scripts designed to establish an enterprise-grade relational database and execute advanced workforce analytics.

| Script File | Purpose & Architectural Scope |
| :--- | :--- |
| **`sql/01_create_database.sql`** | Initializes the `hr_analytics` database with `utf8mb4` encoding and collation. |
| **`sql/02_create_tables.sql`** | Defines master `employees` table, 3 dimension tables (`dim_department`, `dim_job_role`, `dim_education`), CHECK constraints, and B-Tree indices. |
| **`sql/03_import_data.sql`** | Provides high-speed `LOAD DATA LOCAL INFILE` scripts, dimension population queries, and post-ingestion verification audits. |
| **`sql/04_business_analysis.sql`** | Contains 15 targeted analytical queries resolving core executive business questions. |
| **`sql/05_advanced_queries.sql`** | Contains 15 advanced SQL queries utilizing Window Functions, Multi-Table CTEs, and Star-Schema Joins. |

---

## 2. In-Depth Explanations of Core Business Queries (`04_business_analysis.sql`)

### Query 1: Total & Unique Employee Count
```sql
SELECT 
    COUNT(EmployeeID) AS total_employee_count,
    COUNT(DISTINCT EmployeeID) AS unique_employee_count
FROM employees;
```
- **Technical Explanation:** Performs a primary entity scan. Comparing `COUNT(EmployeeID)` to `COUNT(DISTINCT EmployeeID)` guarantees zero primary key duplication.
- **Business Result:** 5,000 total verified employee records with 100% uniqueness.

---

### Query 3: Overall Attrition & Retention Rate
```sql
SELECT 
    COUNT(EmployeeID) AS total_records,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS total_attrition_count,
    SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) AS active_headcount,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS overall_attrition_rate_pct
FROM employees;
```
- **Technical Explanation:** Employs conditional aggregation via `CASE WHEN` inside `SUM()` to calculate both active and separated cohorts in a single pass without subqueries.
- **Business Result:** Attrition count = 652 (**13.04%**), Active workforce = 4,348 (**86.96%**).

---

### Query 4: Department-Wise Attrition Comparison
```sql
SELECT 
    Department,
    COUNT(EmployeeID) AS department_headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS department_attrition_count,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS department_attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY department_attrition_rate_pct DESC;
```
- **Technical Explanation:** Groups data by operational division and calculates individual divisional churn rates to uncover high-risk departments.
- **Business Result:** Research & Development (13.16%), Sales (13.03%), and Human Resources (11.78%).

---

### Query 9: Correlation Between Overtime and Turnover
```sql
SELECT 
    Overtime,
    COUNT(EmployeeID) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS attrition_rate_pct,
    ROUND(AVG(MonthlyIncome), 2) AS avg_salary
FROM employees
GROUP BY Overtime
ORDER BY attrition_rate_pct DESC;
```
- **Technical Explanation:** Groups by the binary `Overtime` indicator to isolate workload intensity effects.
- **Business Result:** Overtime `Yes` attrition is **19.71%** vs Overtime `No` attrition of **10.38%** (nearly 2x churn).

---

### Query 10: Promotion Stagnation Audit (>= 5 Years)
```sql
SELECT 
    EmployeeID, Age, Department, JobRole, YearsAtCompany, 
    YearsSinceLastPromotion, MonthlyIncome, PerformanceRating
FROM employees
WHERE EmploymentStatus = 'Active' 
  AND YearsSinceLastPromotion >= 5
ORDER BY YearsSinceLastPromotion DESC, YearsAtCompany DESC
LIMIT 20;
```
- **Technical Explanation:** Multi-predicate filtering (`WHERE EmploymentStatus = 'Active' AND YearsSinceLastPromotion >= 5`) isolating active staff suffering from promotion stagnation.
- **Business Result:** 382 active employees identified with 5+ years without promotion, representing an immediate flight risk for talent retention.

---

## 3. Advanced Window Functions & Analytical Techniques (`05_advanced_queries.sql`)

### 1. Departmental Salary Ranking via `DENSE_RANK()`
```sql
SELECT 
    EmployeeID, Department, JobRole, MonthlyIncome,
    DENSE_RANK() OVER (
        PARTITION BY Department 
        ORDER BY MonthlyIncome DESC
    ) AS dept_salary_rank
FROM employees
ORDER BY Department, dept_salary_rank;
```
- **Why `DENSE_RANK`?** Unlike `RANK()` which skips rank values after ties (e.g. 1, 2, 2, 4), `DENSE_RANK()` guarantees contiguous sequence numbering (1, 2, 2, 3), ensuring accurate pay band tiers within each division.

---

### 2. Identifying Longest-Tenured Staff via `ROW_NUMBER()` and CTEs
```sql
WITH DepartmentTenureCTE AS (
    SELECT 
        EmployeeID, Department, JobRole, YearsAtCompany, JoiningDate, MonthlyIncome,
        ROW_NUMBER() OVER (
            PARTITION BY Department 
            ORDER BY YearsAtCompany DESC, JoiningDate ASC
        ) AS tenure_rank
    FROM employees
    WHERE EmploymentStatus = 'Active'
)
SELECT * FROM DepartmentTenureCTE WHERE tenure_rank <= 3;
```
- **Technical Explanation:** Uses `ROW_NUMBER()` to generate a deterministic sequential index partitioned by department, and leverages a Common Table Expression (CTE) to filter the outer result set to the top 3 veterans per department.

---

### 3. Salary Quartile Segmentation via `NTILE(4)`
```sql
WITH SalaryQuartileCTE AS (
    SELECT 
        EmployeeID, Department, JobRole, MonthlyIncome,
        NTILE(4) OVER (ORDER BY MonthlyIncome) AS salary_quartile
    FROM employees
)
SELECT 
    salary_quartile,
    COUNT(EmployeeID) AS headcount,
    ROUND(MIN(MonthlyIncome), 2) AS min_salary_in_tier,
    ROUND(MAX(MonthlyIncome), 2) AS max_salary_in_tier,
    ROUND(AVG(MonthlyIncome), 2) AS avg_salary_in_tier
FROM SalaryQuartileCTE
GROUP BY salary_quartile
ORDER BY salary_quartile;
```
- **Technical Explanation:** Dynamically segments 5,000 employees into 4 equal quartiles (1,250 rows each), computing min, max, and average earnings per quartile to inform compensation equity reviews.

---

### 4. Automated Flight Risk Composite Model (Multi-Factor CTE)
```sql
WITH FlightRiskScoring AS (
    SELECT 
        EmployeeID, Department, JobRole, MonthlyIncome, YearsSinceLastPromotion,
        Overtime, JobSatisfaction, WorkLifeBalance,
        (
            (CASE WHEN Overtime = 'Yes' THEN 30 ELSE 0 END) +
            (CASE WHEN JobSatisfaction = 1 THEN 30 WHEN JobSatisfaction = 2 THEN 15 ELSE 0 END) +
            (CASE WHEN WorkLifeBalance = 1 THEN 20 WHEN WorkLifeBalance = 2 THEN 10 ELSE 0 END) +
            (CASE WHEN YearsSinceLastPromotion >= 5 THEN 20 ELSE 0 END)
        ) AS flight_risk_score
    FROM employees
    WHERE EmploymentStatus = 'Active'
)
SELECT *,
    CASE 
        WHEN flight_risk_score >= 70 THEN 'CRITICAL RISK'
        WHEN flight_risk_score >= 45 THEN 'HIGH RISK'
        WHEN flight_risk_score >= 20 THEN 'MODERATE RISK'
        ELSE 'LOW RISK'
    END AS risk_tier
FROM FlightRiskScoring
WHERE flight_risk_score >= 70;
```
- **Technical Explanation:** Assigns additive risk penalty weights across behavioral metrics to surface employees exhibiting multiple churn indicators.

---

## 4. Query Performance Optimization & Indexing Strategies
1. **B-Tree Indices:** Created indices on `Department`, `JobRole`, `Attrition`, and `MonthlyIncome`. Queries filtering or grouping by these columns execute via index scans rather than full table scans.
2. **Cardinality & Cost-Based Optimizer (CBO):** Indexed `Department` and `JobRole` columns allow MySQL's CBO to construct optimal hash joins and sort-merge joins when connecting dimensional tables.
3. **Partitioning by Date (Scale Consideration):** In production warehouses exceeding millions of rows, range-partitioning by `YEAR(JoiningDate)` enables partition pruning on historical trend queries.
