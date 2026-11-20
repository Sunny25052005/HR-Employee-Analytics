# Enterprise DAX Measures Reference Guide

**Project:** HR Employee Analytics Dashboard  
**Technology:** Microsoft Power BI / DAX (Data Analysis Expressions)  
**Author:** Senior BI Developer / Data Analyst  
**Target Table:** `employees` (or Dedicated `_Measures` Calculation Table)

---

## 1. Overview of DAX Architecture & Best Practices
In corporate Power BI solutions, all calculations must be created as **Explicit DAX Measures** rather than relying on implicit aggregations. This ensures:
1. Predictable filter context evaluation across visual slices and cross-filtering.
2. Dynamic responsiveness to slicers (Department, Gender, Job Role, Tenure).
3. Consistent corporate formatting (percentages, currency, integers).
4. Centralization inside a dedicated `_Measures` table.

---

## 2. Core Workforce Health Measures

### 1. Total Employees
- **Business Purpose:** Calculates the total cumulative employee records in the organization.
- **DAX Formula:**
  ```dax
  Total Employees = 
  COUNTROWS('employees')
  ```
- **Explanation:** Uses `COUNTROWS` for optimal tabular engine performance. Returns the total count of rows within the active filter context.
- **Format:** Whole Number (`#,##0`)

---

### 2. Active Employees
- **Business Purpose:** Calculates current headcount actively working at the company.
- **DAX Formula:**
  ```dax
  Active Employees = 
  CALCULATE(
      COUNTROWS('employees'),
      'employees'[EmploymentStatus] = "Active"
  )
  ```
- **Explanation:** Evaluates total rows while injecting a filter condition where `EmploymentStatus` is `"Active"`.
- **Format:** Whole Number (`#,##0`)

---

### 3. Attrition Count
- **Business Purpose:** Quantifies the total number of employees who have voluntarily or involuntarily departed.
- **DAX Formula:**
  ```dax
  Attrition Count = 
  CALCULATE(
      COUNTROWS('employees'),
      'employees'[Attrition] = "Yes"
  )
  ```
- **Explanation:** Modifies filter context using `CALCULATE` to count rows where `Attrition` is `"Yes"`.
- **Format:** Whole Number (`#,##0`)

---

### 4. Attrition Rate (%)
- **Business Purpose:** Core organizational turnover benchmark. Identifies the proportion of personnel lost relative to total workforce.
- **DAX Formula:**
  ```dax
  Attrition Rate = 
  DIVIDE(
      [Attrition Count],
      [Total Employees],
      0
  )
  ```
- **Explanation:** Uses `DIVIDE` rather than the slash `/` operator to handle division-by-zero gracefully, defaulting to `0`. Evaluates dynamically under any department, role, or demographic filter.
- **Format:** Percentage (`0.0%` or `0.00%`)

---

### 5. Employee Retention Rate (%)
- **Business Purpose:** Informs executives of workforce stability and loyalty.
- **DAX Formula:**
  ```dax
  Employee Retention Rate = 
  DIVIDE(
      [Active Employees],
      [Total Employees],
      0
  )
  ```
- **Alternative:** `1 - [Attrition Rate]`
- **Explanation:** Measures the percentage of staff retained over the monitored period.
- **Format:** Percentage (`0.0%`)

---

## 3. Compensation & Demographic Measures

### 6. Average Monthly Income
- **Business Purpose:** Primary payroll metric for compensation benchmarking.
- **DAX Formula:**
  ```dax
  Average Monthly Income = 
  AVERAGE('employees'[MonthlyIncome])
  ```
- **Explanation:** Calculates the arithmetic mean of `MonthlyIncome` across the current filtered employee cohort.
- **Format:** Currency (`$#,##0`)

---

### 7. Median Monthly Income
- **Business Purpose:** Non-skewed compensation benchmark resisting executive salary outlier distortion.
- **DAX Formula:**
  ```dax
  Median Monthly Income = 
  MEDIAN('employees'[MonthlyIncome])
  ```
- **Explanation:** Sorts values in current context and returns the 50th percentile.
- **Format:** Currency (`$#,##0`)

---

### 8. Total Monthly Payroll Commitment
- **Business Purpose:** Monthly organizational payroll expenditure.
- **DAX Formula:**
  ```dax
  Total Monthly Payroll = 
  SUM('employees'[MonthlyIncome])
  ```
- **Explanation:** Sums monthly compensation across all selected employees.
- **Format:** Currency (`$#,##0`)

---

### 9. Average Employee Age
- **Business Purpose:** Monitors workforce generational distribution and succession planning.
- **DAX Formula:**
  ```dax
  Average Age = 
  ROUND(AVERAGE('employees'[Age]), 1)
  ```
- **Explanation:** Computes average age in years rounded to one decimal place.
- **Format:** Decimal (`0.0`)

---

### 10. Average Company Tenure
- **Business Purpose:** Measures average duration of organizational service.
- **DAX Formula:**
  ```dax
  Average Tenure = 
  ROUND(AVERAGE('employees'[YearsAtCompany]), 1)
  ```
- **Explanation:** Arithmetic mean of `YearsAtCompany` for the active filter context.
- **Format:** Decimal (`0.0`) "Years"

---

### 11. Average Total Working Experience
- **Business Purpose:** Assesses overall seniority and industry experience.
- **DAX Formula:**
  ```dax
  Average Total Experience = 
  ROUND(AVERAGE('employees'[TotalWorkingYears]), 1)
  ```
- **Explanation:** Evaluates cumulative lifetime working years across all prior and current roles.
- **Format:** Decimal (`0.0`) "Years"

---

## 4. Organizational & Cultural Sentiment Measures

### 12. Total Departments
- **Business Purpose:** Cardinality count of business operating divisions.
- **DAX Formula:**
  ```dax
  Total Departments = 
  DISTINCTCOUNT('employees'[Department])
  ```
- **Explanation:** Counts distinct department entities in the filtered scope.
- **Format:** Whole Number (`#`)

---

### 13. Average Job Satisfaction
- **Business Purpose:** Gauge of job fulfillment on a 1 (Low) to 4 (Very High) scale.
- **DAX Formula:**
  ```dax
  Average Job Satisfaction = 
  ROUND(AVERAGE('employees'[JobSatisfaction]), 2)
  ```
- **Explanation:** Aggregates employee sentiment scores.
- **Format:** Decimal (`0.00`)

---

### 14. Average Environment Satisfaction
- **Business Purpose:** Gauge of physical/workplace climate on a 1 to 4 scale.
- **DAX Formula:**
  ```dax
  Average Environment Satisfaction = 
  ROUND(AVERAGE('employees'[EnvironmentSatisfaction]), 2)
  ```
- **Format:** Decimal (`0.00`)

---

### 15. Average Work-Life Balance
- **Business Purpose:** Measures equilibrium between work duties and personal life (1 to 4 scale).
- **DAX Formula:**
  ```dax
  Average Work-Life Balance = 
  ROUND(AVERAGE('employees'[WorkLifeBalance]), 2)
  ```
- **Format:** Decimal (`0.00`)

---

### 16. Average Performance Rating
- **Business Purpose:** Annual appraisal benchmark score (1 to 4 scale).
- **DAX Formula:**
  ```dax
  Average Performance Rating = 
  ROUND(AVERAGE('employees'[PerformanceRating]), 2)
  ```
- **Format:** Decimal (`0.00`)

---

## 5. Advanced Strategic & Behavioral DAX Measures

### 17. Overtime Attrition Rate
- **Business Purpose:** Isolates turnover rate among employees working overtime hours.
- **DAX Formula:**
  ```dax
  Overtime Attrition Rate = 
  CALCULATE(
      [Attrition Rate],
      'employees'[Overtime] = "Yes"
  )
  ```
- **Explanation:** Re-evaluates `[Attrition Rate]` overriding the context for Overtime workers.
- **Format:** Percentage (`0.0%`)

---

### 18. Non-Overtime Attrition Rate
- **Business Purpose:** Benchmark comparison against non-overtime personnel.
- **DAX Formula:**
  ```dax
  Non-Overtime Attrition Rate = 
  CALCULATE(
      [Attrition Rate],
      'employees'[Overtime] = "No"
  )
  ```
- **Format:** Percentage (`0.0%`)

---

### 19. Early-Tenure Attrition Rate (<= 2 Years)
- **Business Purpose:** Monitors onboarding success and first-two-years turnover vulnerability.
- **DAX Formula:**
  ```dax
  Early Tenure Attrition Rate = 
  CALCULATE(
      [Attrition Rate],
      'employees'[YearsAtCompany] <= 2
  )
  ```
- **Format:** Percentage (`0.0%`)

---

### 20. Stagnant Top Performers (Flight Risk)
- **Business Purpose:** Identifies active high-performers (Rating >= 3) stuck without promotion for 5+ years.
- **DAX Formula:**
  ```dax
  Stagnant Top Performers Count = 
  CALCULATE(
      COUNTROWS('employees'),
      'employees'[EmploymentStatus] = "Active",
      'employees'[PerformanceRating] >= 3,
      'employees'[YearsSinceLastPromotion] >= 5
  )
  ```
- **Format:** Whole Number (`#,##0`)

---

### 21. Gender Pay Parity Ratio
- **Business Purpose:** Assesses gender compensation equity.
- **DAX Formula:**
  ```dax
  Gender Pay Parity Ratio = 
  VAR FemaleAvgSalary = 
      CALCULATE([Average Monthly Income], 'employees'[Gender] = "Female")
  VAR MaleAvgSalary = 
      CALCULATE([Average Monthly Income], 'employees'[Gender] = "Male")
  RETURN
      DIVIDE(FemaleAvgSalary, MaleAvgSalary, 1.0)
  ```
- **Explanation:** Calculates ratio of female average salary to male average salary. A value of 1.0 indicates perfect parity.
- **Format:** Decimal (`0.00`)

---

## 6. How to Deploy DAX Measures in Power BI Desktop
1. Click **Home > Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Right-click `_Measures` in the Fields pane and select **New Measure**.
4. Paste each formula above and set the formatting in the **Measure Tools** ribbon.
5. Hide the blank dummy column in `_Measures` to move the table to the top with a calculator icon.
