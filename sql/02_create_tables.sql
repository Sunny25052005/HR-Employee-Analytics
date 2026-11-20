-- =============================================================================
-- Script 02: Table Architecture & Constraint Specification
-- Project: HR Employee Analytics Dashboard
-- Database Engine: MySQL 8.0+
-- Description: Creates the core employee relation and normalized star-schema dimensions.
-- =============================================================================

USE hr_analytics;

-- -----------------------------------------------------------------------------
-- 1. MASTER EMPLOYEE TABLE (Staging & Central Analytic Relation)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    EmployeeID VARCHAR(20) NOT NULL,
    Age INT NOT NULL,
    Gender VARCHAR(20) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    JobRole VARCHAR(50) NOT NULL,
    Education INT NOT NULL,
    EducationField VARCHAR(50) NOT NULL,
    JoiningDate DATE NOT NULL,
    YearsAtCompany INT NOT NULL,
    MonthlyIncome DECIMAL(10, 2) NOT NULL,
    JobSatisfaction INT NOT NULL,
    EnvironmentSatisfaction INT NOT NULL,
    PerformanceRating INT NOT NULL,
    WorkLifeBalance INT NOT NULL,
    Overtime VARCHAR(5) NOT NULL,
    TrainingTimesLastYear INT NOT NULL,
    YearsSinceLastPromotion INT NOT NULL,
    TotalWorkingYears INT NOT NULL,
    BusinessTravel VARCHAR(30) NOT NULL,
    Attrition VARCHAR(5) NOT NULL,
    EmploymentStatus VARCHAR(20) NOT NULL,
    AgeGroup VARCHAR(20),
    TenureGroup VARCHAR(30),
    SalaryBand VARCHAR(30),
    OverallSatisfaction DECIMAL(3, 2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Primary Key Constraint
    CONSTRAINT pk_employees PRIMARY KEY (EmployeeID),
    
    -- Domain Validation Constraints (MySQL 8.0+ enforces CHECK constraints)
    CONSTRAINT chk_age CHECK (Age >= 18 AND Age <= 70),
    CONSTRAINT chk_salary CHECK (MonthlyIncome >= 2000.00),
    CONSTRAINT chk_satisfaction CHECK (JobSatisfaction BETWEEN 1 AND 4),
    CONSTRAINT chk_env_satisfaction CHECK (EnvironmentSatisfaction BETWEEN 1 AND 4),
    CONSTRAINT chk_work_life CHECK (WorkLifeBalance BETWEEN 1 AND 4),
    CONSTRAINT chk_perf_rating CHECK (PerformanceRating BETWEEN 1 AND 4),
    CONSTRAINT chk_education CHECK (Education BETWEEN 1 AND 5),
    CONSTRAINT chk_overtime CHECK (Overtime IN ('Yes', 'No')),
    CONSTRAINT chk_attrition CHECK (Attrition IN ('Yes', 'No')),
    CONSTRAINT chk_employment_status CHECK (EmploymentStatus IN ('Active', 'Terminated')),
    CONSTRAINT chk_tenure CHECK (YearsAtCompany <= TotalWorkingYears),
    CONSTRAINT chk_promo CHECK (YearsSinceLastPromotion <= YearsAtCompany)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 2. STAR SCHEMA DIMENSIONAL MODEL TABLES (For Advanced BI & Query Joins)
-- -----------------------------------------------------------------------------

-- Dimension: Education Lookup
DROP TABLE IF EXISTS dim_education;
CREATE TABLE dim_education (
    EducationLevelID INT PRIMARY KEY,
    EducationDegree VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dim_education (EducationLevelID, EducationDegree) VALUES
(1, 'High School / Below College'),
(2, 'Associate Degree / College'),
(3, 'Bachelor Degree'),
(4, 'Master Degree'),
(5, 'Doctorate / PhD');

-- Dimension: Department Lookup
DROP TABLE IF EXISTS dim_department;
CREATE TABLE dim_department (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(50) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Job Role Lookup
DROP TABLE IF EXISTS dim_job_role;
CREATE TABLE dim_job_role (
    JobRoleID INT AUTO_INCREMENT PRIMARY KEY,
    JobRoleName VARCHAR(50) UNIQUE NOT NULL,
    StandardSalaryFloor DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indices to accelerate analytical aggregations and filters
CREATE INDEX idx_emp_dept ON employees(Department);
CREATE INDEX idx_emp_role ON employees(JobRole);
CREATE INDEX idx_emp_attrition ON employees(Attrition);
CREATE INDEX idx_emp_status ON employees(EmploymentStatus);
CREATE INDEX idx_emp_overtime ON employees(Overtime);
CREATE INDEX idx_emp_income ON employees(MonthlyIncome);
