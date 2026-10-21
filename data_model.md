# Star Schema Data Model Architecture

## Model Overview
- **Architecture Type**: Star Schema optimized for Power BI Process Mining.
- **Fact Table**: `Fact_Hospital_Events` (containing event logs, timestamps, wait times).
- **Dimension Tables**: 
  - `Dim_Patient` (Patient demographics, risk groups)
  - `Dim_Department` (Hospital wards, facility IDs)
  - `Dim_Calendar` (Date, month, quarter, day of week)
