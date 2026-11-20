-- =============================================================================
-- Script 04: Core Business Analysis SQL Queries
-- Project: HR Employee Analytics Dashboard
-- Database Engine: MySQL 8.0+
-- Description: Answers the 15 core business questions requested by HR Leadership.
-- =============================================================================

USE hr_analytics;

-- =============================================================================
-- QUESTION 1: What is the total employee count?
-- Purpose: Informs executive leadership of total organizational workforce scale.
-- =============================================================================
SELECT 
    COUNT(EmployeeID) AS total_employee_count,
    COUNT(DISTINCT EmployeeID) AS unique_employee_count
FROM employees;


-- =============================================================================
-- QUESTION 2: Which department has the most employees?
-- Purpose: Identifies organizational headcount concentration across divisions.
-- =============================================================================
SELECT 
    Department,
    COUNT(EmployeeID) AS employee_count,
    ROUND((COUNT(EmployeeID) * 100.0 / (SELECT COUNT(*) FROM employees)), 2) AS percentage_of_workforce
FROM employees
GROUP BY Department
ORDER BY employee_count DESC;


-- =============================================================================
-- QUESTION 3: What is the overall attrition rate?
-- Purpose: Baseline KPI measuring the percentage of the workforce that has left.
-- =============================================================================
SELECT 
    COUNT(EmployeeID) AS total_records,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS total_attrition_count,
    SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) AS active_headcount,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS overall_attrition_rate_pct
FROM employees;


-- =============================================================================
-- QUESTION 4: Which department has the highest attrition?
-- Purpose: Pinpoints high-risk operational areas experiencing abnormal turnover.
-- =============================================================================
SELECT 
    Department,
    COUNT(EmployeeID) AS department_headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS department_attrition_count,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS department_attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY department_attrition_rate_pct DESC;


-- =============================================================================
-- QUESTION 5: Which job role has the highest average salary?
-- Purpose: Benchmark market competitiveness and compensation hierarchies.
-- =============================================================================
SELECT 
    JobRole,
    Department,
    COUNT(EmployeeID) AS employee_count,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_salary,
    ROUND(MIN(MonthlyIncome), 2) AS min_monthly_salary,
    ROUND(MAX(MonthlyIncome), 2) AS max_monthly_salary
FROM employees
GROUP BY JobRole, Department
ORDER BY avg_monthly_salary DESC;


-- =============================================================================
-- QUESTION 6: What is the average monthly salary across the company?
-- Purpose: General workforce compensation baseline for budget planning.
-- =============================================================================
SELECT 
    ROUND(AVG(MonthlyIncome), 2) AS overall_avg_monthly_salary,
    ROUND(MIN(MonthlyIncome), 2) AS overall_min_salary,
    ROUND(MAX(MonthlyIncome), 2) AS overall_max_salary,
    ROUND(STDDEV(MonthlyIncome), 2) AS salary_standard_deviation
FROM employees;


-- =============================================================================
-- QUESTION 7: What is the average employee tenure?
-- Purpose: Gauges organizational longevity, loyalty, and career lifecycle.
-- =============================================================================
SELECT 
    ROUND(AVG(YearsAtCompany), 2) AS avg_years_at_company,
    ROUND(AVG(TotalWorkingYears), 2) AS avg_total_working_years,
    ROUND(AVG(YearsSinceLastPromotion), 2) AS avg_years_since_promotion
FROM employees;


-- =============================================================================
-- QUESTION 8: Which age group has the highest attrition?
-- Purpose: Uncovers generational vulnerability and early-career turnover risks.
-- =============================================================================
SELECT 
    AgeGroup,
    COUNT(EmployeeID) AS total_in_age_group,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS attrition_rate_pct
FROM employees
GROUP BY AgeGroup
ORDER BY attrition_rate_pct DESC;


-- =============================================================================
-- QUESTION 9: Does overtime correlate with attrition?
-- Purpose: Evaluates employee burnout and work-intensity impact on retention.
-- =============================================================================
SELECT 
    Overtime,
    COUNT(EmployeeID) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS attrition_rate_pct,
    ROUND(AVG(MonthlyIncome), 2) AS avg_salary
FROM employees
GROUP BY Overtime
ORDER BY attrition_rate_pct DESC;


-- =============================================================================
-- QUESTION 10: Which employees have not received a promotion for a long time?
-- Purpose: Identifies active high-tenure employees at risk due to career stagnation (>= 5 years).
-- =============================================================================
SELECT 
    EmployeeID,
    Age,
    Department,
    JobRole,
    YearsAtCompany,
    YearsSinceLastPromotion,
    MonthlyIncome,
    PerformanceRating
FROM employees
WHERE EmploymentStatus = 'Active' 
  AND YearsSinceLastPromotion >= 5
ORDER BY YearsSinceLastPromotion DESC, YearsAtCompany DESC
LIMIT 20;


-- =============================================================================
-- QUESTION 11: Which department has the highest job satisfaction?
-- Purpose: Evaluates employee morale and cultural engagement across divisions.
-- =============================================================================
SELECT 
    Department,
    COUNT(EmployeeID) AS total_employees,
    ROUND(AVG(JobSatisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(EnvironmentSatisfaction), 2) AS avg_env_satisfaction,
    ROUND(AVG(WorkLifeBalance), 2) AS avg_work_life_balance,
    ROUND(AVG(OverallSatisfaction), 2) AS composite_morale_score
FROM employees
GROUP BY Department
ORDER BY composite_morale_score DESC;


-- =============================================================================
-- QUESTION 12: What is the gender distribution across the organization?
-- Purpose: Analyzes Diversity, Equity, and Inclusion (DEI) workforce metrics.
-- =============================================================================
SELECT 
    Gender,
    COUNT(EmployeeID) AS headcount,
    ROUND((COUNT(EmployeeID) * 100.0 / (SELECT COUNT(*) FROM employees)), 2) AS pct_of_total_workforce,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_salary
FROM employees
GROUP BY Gender
ORDER BY headcount DESC;


-- =============================================================================
-- QUESTION 13: Which employees have the highest salaries?
-- Purpose: Compensation audits and executive payroll transparency (Top 10 Earners).
-- =============================================================================
SELECT 
    EmployeeID,
    Age,
    Department,
    JobRole,
    EducationField,
    TotalWorkingYears,
    MonthlyIncome
FROM employees
ORDER BY MonthlyIncome DESC
LIMIT 10;


-- =============================================================================
-- QUESTION 14: What is the department-wise performance distribution?
-- Purpose: Cross-tabulates employee appraisal distribution across divisions.
-- =============================================================================
SELECT 
    Department,
    COUNT(EmployeeID) AS department_headcount,
    SUM(CASE WHEN PerformanceRating = 1 THEN 1 ELSE 0 END) AS rating_1_low,
    SUM(CASE WHEN PerformanceRating = 2 THEN 1 ELSE 0 END) AS rating_2_good,
    SUM(CASE WHEN PerformanceRating = 3 THEN 1 ELSE 0 END) AS rating_3_excellent,
    SUM(CASE WHEN PerformanceRating = 4 THEN 1 ELSE 0 END) AS rating_4_outstanding,
    ROUND(AVG(PerformanceRating), 2) AS avg_dept_rating
FROM employees
GROUP BY Department
ORDER BY avg_dept_rating DESC;


-- =============================================================================
-- QUESTION 15: What is the employee retention rate?
-- Purpose: Measures overall organizational stability and personnel continuity.
-- =============================================================================
SELECT 
    COUNT(EmployeeID) AS total_headcount,
    SUM(CASE WHEN EmploymentStatus = 'Active' THEN 1 ELSE 0 END) AS active_headcount,
    ROUND((SUM(CASE WHEN EmploymentStatus = 'Active' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS retention_rate_pct,
    ROUND((SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(EmployeeID)), 2) AS attrition_rate_pct
FROM employees;
