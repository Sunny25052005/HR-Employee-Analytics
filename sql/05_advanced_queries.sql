-- =============================================================================
-- Script 05: Advanced SQL Analytics, Window Functions & CTEs
-- Project: HR Employee Analytics Dashboard
-- Database Engine: MySQL 8.0+
-- Description: Advanced analytical SQL featuring Window Functions (RANK, DENSE_RANK,
--              ROW_NUMBER, NTILE), Multi-table CTEs, Star-Schema Joins, and Subqueries.
-- =============================================================================

USE hr_analytics;

-- =============================================================================
-- QUERY 1: DEPARTMENTAL SALARY RANKING (DENSE_RANK)
-- Objective: Rank employees by salary within each department to identify top earners.
-- Window Function: DENSE_RANK() PARTITION BY Department ORDER BY MonthlyIncome DESC
-- =============================================================================
SELECT 
    EmployeeID,
    Department,
    JobRole,
    MonthlyIncome,
    DENSE_RANK() OVER (
        PARTITION BY Department 
        ORDER BY MonthlyIncome DESC
    ) AS dept_salary_rank
FROM employees
ORDER BY Department, dept_salary_rank
LIMIT 30;


-- =============================================================================
-- QUERY 2: JOB ROLE SALARY PEER RANKING (RANK vs DENSE_RANK)
-- Objective: Evaluate within-role compensation distribution and tie-handling.
-- =============================================================================
SELECT 
    EmployeeID,
    JobRole,
    TotalWorkingYears,
    MonthlyIncome,
    RANK() OVER (
        PARTITION BY JobRole 
        ORDER BY MonthlyIncome DESC
    ) AS role_salary_rank,
    DENSE_RANK() OVER (
        PARTITION BY JobRole 
        ORDER BY MonthlyIncome DESC
    ) AS role_dense_rank
FROM employees
WHERE JobRole IN ('Research Scientist', 'Sales Executive')
ORDER BY JobRole, role_salary_rank
LIMIT 20;


-- =============================================================================
-- QUERY 3: LONGEST TENURED EMPLOYEES PER DEPARTMENT (ROW_NUMBER)
-- Objective: Retrieve the top 3 longest-tenured veterans in each department.
-- Techniques: CTE + ROW_NUMBER() Window Function + Filter
-- =============================================================================
WITH DepartmentTenureCTE AS (
    SELECT 
        EmployeeID,
        Department,
        JobRole,
        YearsAtCompany,
        JoiningDate,
        MonthlyIncome,
        ROW_NUMBER() OVER (
            PARTITION BY Department 
            ORDER BY YearsAtCompany DESC, JoiningDate ASC
        ) AS tenure_rank
    FROM employees
    WHERE EmploymentStatus = 'Active'
)
SELECT 
    Department,
    tenure_rank,
    EmployeeID,
    JobRole,
    YearsAtCompany,
    JoiningDate,
    MonthlyIncome
FROM DepartmentTenureCTE
WHERE tenure_rank <= 3
ORDER BY Department, tenure_rank;


-- =============================================================================
-- QUERY 4: SALARY QUARTILE SEGMENTATION (NTILE)
-- Objective: Divide the entire workforce into 4 equal compensation tiers (Quartiles).
-- =============================================================================
WITH SalaryQuartileCTE AS (
    SELECT 
        EmployeeID,
        Department,
        JobRole,
        MonthlyIncome,
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


-- =============================================================================
-- QUERY 5: RUNNING TOTAL OF SALARY EXPENDITURE OVER TIME (RUNNING AGGREGATE)
-- Objective: Cumulative payroll commitment tracking based on employee joining sequence.
-- =============================================================================
SELECT 
    EmployeeID,
    Department,
    JoiningDate,
    MonthlyIncome,
    SUM(MonthlyIncome) OVER (
        PARTITION BY Department 
        ORDER BY JoiningDate 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_dept_payroll
FROM employees
ORDER BY Department, JoiningDate
LIMIT 25;


-- =============================================================================
-- QUERY 6: COMPARISON TO DEPARTMENTAL AVERAGE (WINDOW AVG + VARIANCE)
-- Objective: Identify employees earning significantly above or below their departmental mean.
-- =============================================================================
SELECT 
    EmployeeID,
    Department,
    JobRole,
    MonthlyIncome,
    ROUND(AVG(MonthlyIncome) OVER (PARTITION BY Department), 2) AS dept_avg_income,
    ROUND(MonthlyIncome - AVG(MonthlyIncome) OVER (PARTITION BY Department), 2) AS variance_from_dept_avg,
    ROUND(((MonthlyIncome - AVG(MonthlyIncome) OVER (PARTITION BY Department)) / 
           AVG(MonthlyIncome) OVER (PARTITION BY Department)) * 100, 2) AS pct_variance
FROM employees
ORDER BY pct_variance DESC
LIMIT 25;


-- =============================================================================
-- QUERY 7: MULTI-LEVEL ATTRITION RISK SCORE MODEL (COMPOSITE CTE)
-- Objective: Score active employees on an automated flight-risk scale (0 to 100).
-- High Flight Risk: Overtime = Yes, Low Satisfaction, Stagnant Promotion, Low WLB.
-- =============================================================================
WITH FlightRiskScoring AS (
    SELECT 
        EmployeeID,
        Department,
        JobRole,
        MonthlyIncome,
        YearsSinceLastPromotion,
        Overtime,
        JobSatisfaction,
        WorkLifeBalance,
        (
            (CASE WHEN Overtime = 'Yes' THEN 30 ELSE 0 END) +
            (CASE WHEN JobSatisfaction = 1 THEN 30 WHEN JobSatisfaction = 2 THEN 15 ELSE 0 END) +
            (CASE WHEN WorkLifeBalance = 1 THEN 20 WHEN WorkLifeBalance = 2 THEN 10 ELSE 0 END) +
            (CASE WHEN YearsSinceLastPromotion >= 5 THEN 20 ELSE 0 END)
        ) AS flight_risk_score
    FROM employees
    WHERE EmploymentStatus = 'Active'
)
SELECT 
    EmployeeID,
    Department,
    JobRole,
    MonthlyIncome,
    YearsSinceLastPromotion,
    Overtime,
    JobSatisfaction,
    flight_risk_score,
    CASE 
        WHEN flight_risk_score >= 70 THEN 'CRITICAL RISK'
        WHEN flight_risk_score >= 45 THEN 'HIGH RISK'
        WHEN flight_risk_score >= 20 THEN 'MODERATE RISK'
        ELSE 'LOW RISK'
    END AS risk_tier
FROM FlightRiskScoring
WHERE flight_risk_score >= 70
ORDER BY flight_risk_score DESC, MonthlyIncome ASC
LIMIT 30;


-- =============================================================================
-- QUERY 8: STAR SCHEMA JOIN - EMPLOYEES WITH DIM_EDUCATION
-- Objective: Enrich employee records with normalized educational degrees.
-- Relational Technique: INNER JOIN
-- =============================================================================
SELECT 
    e.EmployeeID,
    e.Age,
    e.Department,
    e.JobRole,
    d.EducationDegree,
    e.EducationField,
    e.MonthlyIncome
FROM employees e
INNER JOIN dim_education d 
    ON e.Education = d.EducationLevelID
WHERE e.MonthlyIncome > 12000
ORDER BY e.MonthlyIncome DESC
LIMIT 20;


-- =============================================================================
-- QUERY 9: STAR SCHEMA JOIN - COMPREHENSIVE MULTI-DIMENSIONAL AUDIT
-- Objective: Cross-analyze compensation relative to role standard floors.
-- Relational Technique: MULTI-TABLE INNER JOIN
-- =============================================================================
SELECT 
    e.EmployeeID,
    dept.DepartmentName,
    role.JobRoleName,
    e.MonthlyIncome,
    role.StandardSalaryFloor,
    ROUND(e.MonthlyIncome - role.StandardSalaryFloor, 2) AS compensation_premium
FROM employees e
INNER JOIN dim_department dept 
    ON e.Department = dept.DepartmentName
INNER JOIN dim_job_role role 
    ON e.JobRole = role.JobRoleName
ORDER BY compensation_premium DESC
LIMIT 20;


-- =============================================================================
-- QUERY 10: STAGNANT HIGH PERFORMERS AUDIT (SUBQUERY & CTE)
-- Objective: Detect star talent (Rating >= 3) waiting 4+ years for promotion.
-- =============================================================================
WITH HighPerformingStagnant AS (
    SELECT 
        EmployeeID,
        Department,
        JobRole,
        YearsAtCompany,
        YearsSinceLastPromotion,
        PerformanceRating,
        MonthlyIncome
    FROM employees
    WHERE EmploymentStatus = 'Active'
      AND PerformanceRating >= 3
      AND YearsSinceLastPromotion >= 4
)
SELECT 
    Department,
    COUNT(EmployeeID) AS stagnant_top_performers_count,
    ROUND(AVG(MonthlyIncome), 2) AS avg_salary,
    ROUND(AVG(YearsSinceLastPromotion), 1) AS avg_years_without_promo
FROM HighPerformingStagnant
GROUP BY Department
ORDER BY stagnant_top_performers_count DESC;


-- =============================================================================
-- QUERY 11: DEPARTMENT OUTLIERS VIA GROUP BY & HAVING
-- Objective: Identify departments with below-average satisfaction and high attrition.
-- =============================================================================
SELECT 
    Department,
    COUNT(EmployeeID) AS dept_headcount,
    ROUND(AVG(OverallSatisfaction), 2) AS avg_morale,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS attrition_rate
FROM employees
GROUP BY Department
HAVING avg_morale < 2.70 OR attrition_rate > 12.0
ORDER BY attrition_rate DESC;


-- =============================================================================
-- QUERY 12: CORRELATED SUBQUERY - ABOVE-AVERAGE EARNERS WITHIN ROLE
-- Objective: Flag employees whose compensation exceeds their specific peer group mean.
-- =============================================================================
SELECT 
    e.EmployeeID,
    e.JobRole,
    e.Department,
    e.MonthlyIncome
FROM employees e
WHERE e.MonthlyIncome > (
    SELECT AVG(inner_emp.MonthlyIncome)
    FROM employees inner_emp
    WHERE inner_emp.JobRole = e.JobRole
)
ORDER BY e.JobRole, e.MonthlyIncome DESC
LIMIT 25;


-- =============================================================================
-- QUERY 13: YEAR-OVER-YEAR HIRING GROWTH TREND (DATE AGGREGATION & CTE)
-- Objective: Annual intake velocity and active retention status.
-- =============================================================================
WITH YearlyCohortCTE AS (
    SELECT 
        YEAR(JoiningDate) AS hire_year,
        COUNT(EmployeeID) AS hires_count,
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_from_cohort
    FROM employees
    GROUP BY YEAR(JoiningDate)
)
SELECT 
    hire_year,
    hires_count,
    attrition_from_cohort,
    ROUND((attrition_from_cohort * 100.0 / hires_count), 2) AS cohort_attrition_rate
FROM YearlyCohortCTE
ORDER BY hire_year ASC;


-- =============================================================================
-- QUERY 14: EXECUTIVE SALARY BENCHMARKING (MIN, MAX, 25th, 75th PERCENTILES)
-- Objective: Enterprise salary distribution summary across departments.
-- =============================================================================
SELECT 
    Department,
    COUNT(*) AS total_staff,
    ROUND(MIN(MonthlyIncome), 2) AS min_salary,
    ROUND(AVG(MonthlyIncome), 2) AS mean_salary,
    ROUND(MAX(MonthlyIncome), 2) AS max_salary,
    ROUND(MAX(MonthlyIncome) - MIN(MonthlyIncome), 2) AS salary_spread
FROM employees
GROUP BY Department
ORDER BY mean_salary DESC;


-- =============================================================================
-- QUERY 15: COMPREHENSIVE WORKFORCE HEALTH SCORECARD (FINAL EXECUTIVE CTE)
-- Objective: Single comprehensive executive summary roll-up by business unit.
-- =============================================================================
WITH DeptMetrics AS (
    SELECT 
        Department,
        COUNT(EmployeeID) AS total_employees,
        SUM(CASE WHEN EmploymentStatus = 'Active' THEN 1 ELSE 0 END) AS active_headcount,
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS churned_headcount,
        AVG(MonthlyIncome) AS avg_payroll,
        AVG(Age) AS avg_age,
        AVG(YearsAtCompany) AS avg_tenure,
        AVG(OverallSatisfaction) AS avg_wellbeing
    FROM employees
    GROUP BY Department
)
SELECT 
    Department,
    total_employees,
    active_headcount,
    churned_headcount,
    ROUND((churned_headcount * 100.0 / total_employees), 2) AS attrition_rate_pct,
    ROUND(avg_payroll, 2) AS avg_monthly_income,
    ROUND(avg_age, 1) AS mean_age_years,
    ROUND(avg_tenure, 1) AS mean_tenure_years,
    ROUND(avg_wellbeing, 2) AS composite_morale_index
FROM DeptMetrics
ORDER BY total_employees DESC;
