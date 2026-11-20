# Power BI Executive Dashboard User & Implementation Guide

**Project:** HR Employee Analytics Dashboard  
**Technology:** Microsoft Power BI Desktop & Service  
**Target Audience:** Business Intelligence Analysts, HR Leadership, Data Analytics Recruiters  

---

## 1. Executive Summary & Dashboard Architecture
The **HR Employee Analytics Power BI Dashboard** provides a 360-degree interactive diagnostic view of organizational workforce dynamics. Engineered across **4 dedicated report pages**, the solution empowers HR executives and operational managers to drill down from high-level enterprise health metrics into departmental flight risks, compensation structures, and employee engagement scores.

```
+------------------------------------------------------------------------------------+
|                         POWER BI REPORT PAGE ARCHITECTURE                          |
+------------------------------------------------------------------------------------+
|                                                                                    |
|  PAGE 1: HR EXECUTIVE OVERVIEW                                                    |
|  └── High-level macro KPIs (Headcount, Active Staff, Attrition Rate, Avg Salary)   |
|  └── Divisional distributions, gender diversity donut, hiring trends               |
|                                                                                    |
|  PAGE 2: ATTRITION ANALYSIS                                                        |
|  └── Deep-dive into turnover drivers: Overtime, Age Cohorts, Tenure, Job Roles     |
|  └── Benchmark comparisons against organizational averages                         |
|                                                                                    |
|  PAGE 3: SALARY AND WORKFORCE ANALYSIS                                             |
|  └── Compensation benchmarks by title, experience vs salary scatter regression     |
|  └── Educational specialization matrix and salary quartile distribution            |
|                                                                                    |
|  PAGE 4: PERFORMANCE AND SATISFACTION                                              |
|  └── Employee morale scores (Job Sat, Work-Life Balance, Environment)              |
|  └── Appraisal ratings, promotion stagnation flight-risk audit, training ROI       |
+------------------------------------------------------------------------------------+
```

---

## 2. In-Depth Report Page Breakdown

### Page 1: HR Executive Overview
- **Core KPI Cards:**
  - **Total Employees:** `5,000` (Cumulative historical headcount)
  - **Active Employees:** `4,348` (87.0% current workforce)
  - **Attrition Count:** `652` (Total voluntary & involuntary separations)
  - **Attrition Rate:** `13.0%` (Turnover benchmark)
  - **Average Monthly Income:** `$10,017`
  - **Average Age:** `37.0 Years`
- **Key Visuals:**
  - *Headcount by Department:* Clustered Column Chart illustrating workforce concentration (R&D: 62.2%, Sales: 30.9%, HR: 7.0%).
  - *Gender Diversity:* Donut Chart reflecting 52% Male, 44% Female, 4% Non-Binary representation.
  - *Intake Velocity:* Area Chart displaying historical annual hiring volume.
  - *Employment Status by Division:* Stacked bar chart showing active vs separated proportions.

### Page 2: Attrition Analysis
- **Top Metrics Strip:** Overall Attrition (`13.0%`) vs Overtime Attrition (`19.7%`) vs Early Tenure Attrition (`14.8%`).
- **Key Visuals:**
  - *Attrition by Department:* Highlights divisional variation with visual benchmark line.
  - *Attrition by Job Role:* Horizontal bar chart ranking roles from highest turnover (Sales Representative: 15.5%) to lowest (Research Director: 7.4%).
  - *Overtime Impact:* 100% Stacked Bar demonstrating nearly 2x churn among overtime staff.
  - *Age Group Breakdown:* Visualizes vulnerability of junior workers (`<25`).
  - *Tenure Attrition Curve:* Shows that over 38% of exits occur within the first 24 months.

### Page 3: Salary and Workforce Analysis
- **Top Metrics Strip:** Mean Salary (`$10,017`), Median Salary (`$8,655`), Gender Pay Parity Ratio (`0.99`).
- **Key Visuals:**
  - *Departmental Salary Comparison:* Average vs Median compensation.
  - *Compensation by Job Role:* Box plot showing wage quartiles from Manager ($15k-$22k) down to Sales Rep ($3k-$5k).
  - *Experience vs Salary Scatter Plot:* Demonstrates strong positive correlation between Total Working Years and Monthly Income.
  - *Education Discipline Matrix:* Visualizes talent distribution across technical and life sciences degrees.

### Page 4: Performance and Satisfaction
- **Top Metrics Strip:** Average Job Satisfaction (`2.71/4.0`), Average Work-Life Balance (`2.65/4.0`), Stagnant Top Performers (`382`).
- **Key Visuals:**
  - *Work-Life Balance vs Attrition:* Monotonic decline in churn as WLB rating improves from 1 to 4.
  - *Performance Appraisals by Department:* 100% Stacked Bar showing consistent appraisal distributions across units.
  - *Promotion Stagnation Curve:* Line chart proving that attrition accelerates when employees wait 4+ years for promotion.
  - *Training Sessions vs Performance:* Identifies optimal training frequency (2-3 sessions/year).

---

## 3. Data Modeling & Dimensional Architecture

```
+--------------------+            +------------------------+            +--------------------+
|   dim_department   |            |       employees        |            |   dim_education    |
+--------------------+            +------------------------+            +--------------------+
| DepartmentID (PK)  | 1        * | EmployeeID (PK)        | *        1 | EducationID (PK)   |
| DepartmentName     |───────────►| Department (FK)        |◄───────────| EducationDegree    |
+--------------------+            | JobRole (FK)           |            +--------------------+
                                  | Education (FK)         |
+--------------------+            | Age, MonthlyIncome...  |
|    dim_job_role    | 1        * | Attrition, Tenure...   |
+--------------------+───────────►+------------------------+
| JobRoleID (PK)     |
| JobRoleName        |
| StandardSalaryFloor|
+--------------------+
```

### Model Settings:
- **Storage Mode:** Import Mode (optimal in-memory VertiPaq compression).
- **Cross-Filter Direction:** Single (Dimension to Fact table).
- **Date Dimension:** Ingested `JoiningDate` configured with date hierarchy (Year, Quarter, Month).

---

## 4. Advanced Power BI Features Implemented

### 4.1 Custom Dynamic Tooltips
- Created a specialized tooltip page (`Tooltip_EmployeeProfile`) displaying tenure, performance rating, and overtime status when hovering over any department or role bar chart.

### 4.2 Slicer Synchronisation
- Slicers configured in the **Sync Slicers Pane** across all 4 pages so an executive selecting "Sales" on Page 1 retains the filter on Pages 2, 3, and 4.

### 4.3 Row-Level Security (RLS) Setup
Configured RLS roles for corporate governance:
```dax
-- Role: Sales_Director
[Department] = "Sales"

-- Role: R&D_Director
[Department] = "Research & Development"

-- Role: HR_Executive
-- No filter (Full Access)
```

---

## 5. Step-by-Step Power BI Desktop Build Instructions
1. **Download & Open:** Open Microsoft Power BI Desktop.
2. **Import Cleaned CSV:**
   - Click **Get Data > Text/CSV** and select `dataset/cleaned_employee_data.csv`.
   - In Power Query, click **Transform Data**, verify data types, and click **Close & Apply**.
3. **Add DAX Calculation Table:**
   - Click **Enter Data**, name the table `_Measures`.
   - Right-click `_Measures` and add the 21 DAX measures documented in `powerbi/DAX_Measures.md`.
4. **Build Layout:** Follow the visual placement grids detailed in `powerbi/Dashboard_Design_Guide.md`.
5. **Save Report:** Save as `HR_Employee_Analytics_Dashboard.pbix`.
