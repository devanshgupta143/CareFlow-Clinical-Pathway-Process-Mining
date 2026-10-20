# Data Cleaning & Quality Control Rules

## Missing & Invalid Value Handling
- **Null Wait Times**: Replace missing or null `WaitTimeMinutes` values with 0.
- **Unmatched Departments**: Map unassigned or null departments to 'General Assessment'.
- **Duplicate Records**: Deduplicate events based on matching `Patient_ID` + `Activity_Name` + `Timestamp`.
- **Outlier Filtering**: Flag patient wait times exceeding 1,440 minutes (24 hours) as data anomalies for review.
