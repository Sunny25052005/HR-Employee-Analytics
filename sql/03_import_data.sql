-- =============================================================================
-- Script 03: Data Ingestion & Dimensional Population
-- Project: HR Employee Analytics Dashboard
-- Database Engine: MySQL 8.0+
-- Description: Ingests the cleaned CSV dataset and populates relational dimension tables.
-- =============================================================================

USE hr_analytics;

-- -----------------------------------------------------------------------------
-- METHOD 1: INGESTION VIA MySQL LOAD DATA LOCAL INFILE
-- Note: Replace file path with absolute path on your system.
-- In MySQL Client / Workbench, ensure local_infile is enabled:
-- SET GLOBAL local_infile = 1;
-- -----------------------------------------------------------------------------

/*
LOAD DATA LOCAL INFILE 'C:/Users/DELL/OneDrive/Desktop/HR EMPL/dataset/cleaned_employee_data.csv'
INTO TABLE employees
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n' -- Use '\n' for Linux / macOS environments
IGNORE 1 ROWS
(
    EmployeeID, Age, Gender, Department, JobRole, Education, EducationField, 
    JoiningDate, YearsAtCompany, MonthlyIncome, JobSatisfaction, 
    EnvironmentSatisfaction, PerformanceRating, WorkLifeBalance, Overtime, 
    TrainingTimesLastYear, YearsSinceLastPromotion, TotalWorkingYears, 
    BusinessTravel, Attrition, EmploymentStatus, AgeGroup, TenureGroup, 
    SalaryBand, OverallSatisfaction
);
*/

-- -----------------------------------------------------------------------------
-- METHOD 2: POPULATE DIMENSIONAL TABLES FROM MASTER INGESTION
-- Run after data is loaded into `employees` table:
-- -----------------------------------------------------------------------------

-- 1. Populate dim_department
INSERT IGNORE INTO dim_department (DepartmentName)
SELECT DISTINCT Department FROM employees ORDER BY Department;

-- 2. Populate dim_job_role with calculated salary floors
INSERT IGNORE INTO dim_job_role (JobRoleName, StandardSalaryFloor)
SELECT JobRole, MIN(MonthlyIncome) 
FROM employees 
GROUP BY JobRole 
ORDER BY JobRole;

-- -----------------------------------------------------------------------------
-- POST-IMPORT VERIFICATION AND SANITY AUDIT QUERIES
-- -----------------------------------------------------------------------------

-- Verification 1: Verify total row count equals 5,000
SELECT COUNT(*) AS total_imported_records FROM employees;

-- Verification 2: Check for any unexpected NULL values
SELECT 
    SUM(CASE WHEN EmployeeID IS NULL THEN 1 ELSE 0 END) AS null_emp_ids,
    SUM(CASE WHEN MonthlyIncome IS NULL THEN 1 ELSE 0 END) AS null_income,
    SUM(CASE WHEN Department IS NULL THEN 1 ELSE 0 END) AS null_dept,
    SUM(CASE WHEN Attrition IS NULL THEN 1 ELSE 0 END) AS null_attrition
FROM employees;

-- Verification 3: Inspect sample rows
SELECT 
    EmployeeID, Age, Gender, Department, JobRole, MonthlyIncome, 
    YearsAtCompany, Attrition, EmploymentStatus
FROM employees
LIMIT 5;
