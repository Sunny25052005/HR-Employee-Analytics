# Project Overview: HR Employee Analytics Dashboard

**Project Title:** End-to-End HR Employee Analytics & Business Intelligence Solution  
**Target Roles:** Data Analyst, Business Analyst, BI Developer, Data Engineer  
**Domain:** Human Resources / People Analytics / Workforce Intelligence  
**Author:** B.Tech Computer Science Student  

---

## 1. Executive Summary
The **HR Employee Analytics Dashboard** is a comprehensive, production-grade business intelligence and analytics solution engineered to empower Chief Human Resources Officers (CHROs), People Operations, and Department Leaders to make data-backed human capital decisions.

By synthesizing **5,000 verified employee records**, this project tackles core enterprise HR dilemmas:
- **Voluntary Attrition & Flight Risk:** Why do employees leave, which roles are at greatest risk, and what early warning signals (overtime, promotion stagnation, low satisfaction) precede resignation?
- **Compensation Equity & Payroll Optimization:** How does compensation scale with experience, education, and job title? Are there wage disparities or compression issues across departments?
- **Workforce Demographics & DEI:** What is the organizational footprint across departments, age cohorts, and gender diversity?
- **Employee Morale & Performance:** What is the relationship between work-life balance, job satisfaction, environment rating, and annual appraisal performance?

---

## 2. Technology Stack & Architecture

```
+-----------------------------------------------------------------------------------+
|                              END-TO-END DATA ARCHITECTURE                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Raw Data Simulation ]                                                          |
|         │  (5,010 synthetic records with realistic anomalies, seed=42)          |
|         ▼                                                                         |
|  [ Python Data Pipeline ] ───► python/data_cleaning.py                            |
|         │                      ├── Deduplication & whitespace trimming            |
|         │                      ├── Context-aware missing value imputation         |
|         │                      ├── Chronology validation & domain constraints     |
|         │                      └── Feature Engineering (AgeGroup, SalaryBand)     |
|         ▼                                                                         |
|  [ Cleaned Data Tier ] ──────► dataset/cleaned_employee_data.csv (5,000 records)  |
|         │                                                                         |
|         ├───────────────────────────────┬────────────────────────────────┐        |
|         ▼                               ▼                                ▼        |
|  [ Python EDA & Viz ]          [ Relational SQL Tier ]         [ Power BI Tier ]  |
|  python/eda_analysis.py        sql/01_create_database.sql      powerbi/           |
|  python/data_visualization.py  sql/02_create_tables.sql        4 Interactive      |
|  14 High-Res Charts            sql/03_import_data.sql          Executive Pages    |
|  Jupyter Notebook              sql/04_business_analysis.sql    21 Custom DAX      |
|  Statistical Summaries         sql/05_advanced_queries.sql     Explicit Measures  |
|                                30 Production SQL Queries       Star Schema Model  |
+-----------------------------------------------------------------------------------+
```

### Core Technologies
- **Python 3.12+:** Core data processing, simulation, cleaning, and statistical validation.
- **Pandas & NumPy:** In-memory tabular transformations, grouping, aggregations, and IQR outlier detection.
- **Matplotlib & Seaborn:** Publication-quality corporate data visualizations with accessible palettes.
- **MySQL 8.0+ / SQL:** Relational schema design, domain constraints, window functions, and multi-table CTE analytics.
- **Microsoft Power BI Desktop:** Interactive executive dashboards, KPI tiles, cross-filtering, and star-schema modeling.
- **DAX (Data Analysis Expressions):** 21 customized measures with dynamic filter context evaluation.
- **Pytest:** Automated test-driven verification suite validating 100% of data integrity constraints.
- **Git & GitHub:** Version control, professional repository architecture, and recruiter-focused portfolio assets.

---

## 3. High-Level Project Deliverables
1. **Curated Datasets:**
   - `dataset/raw_employee_data.csv`: 5,010 raw synthetic records with controlled anomalies.
   - `dataset/cleaned_employee_data.csv`: 5,000 validated production records.
2. **Modular Python Scripts:**
   - `python/generate_dataset.py`: Reproducible synthetic data generation with seed=42.
   - `python/data_cleaning.py`: Complete cleaning, imputation, and validation sequence.
   - `python/eda_analysis.py`: Exploratory statistical profiling and summary export.
   - `python/data_visualization.py`: Generates 14 corporate visual artifacts.
   - `python/notebooks/HR_Analytics_EDA.ipynb`: Interactive Jupyter analysis workflow.
3. **Database & SQL Suite:**
   - 5 dedicated SQL files providing schema definitions, star-schema dimension tables, indices, and 30 business queries answering 15 specific executive questions.
4. **Power BI & Business Intelligence:**
   - `powerbi/DAX_Measures.md`: 21 comprehensive DAX formulas with mathematical explanations.
   - `powerbi/Dashboard_Design_Guide.md`: 4 full dashboard page blueprints and visual placement grids.
5. **Quality Assurance & Verification:**
   - `tests/test_data.py`: Automated Pytest suite verifying row counts, uniqueness, and domain bounds.
