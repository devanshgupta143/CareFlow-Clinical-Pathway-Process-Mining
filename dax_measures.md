# Power BI DAX Measures Specification

## Key Metrics
- Total Patients = COUNTROWS('HospitalLogs')
- Avg Wait Time (Mins) = AVERAGE('HospitalLogs'[WaitTimeMinutes])
- Bottleneck Cases = CALCULATE(COUNTROWS('HospitalLogs'), 'HospitalLogs'[WaitTimeMinutes] > 60)
- Readmission Rate = DIVIDE([Readmissions], [Total Patients], 0)
