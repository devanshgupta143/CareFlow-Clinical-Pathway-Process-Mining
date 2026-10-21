# Fact and Dimension Table Mapping

## Relationship Specifications
- **Fact_Hospital_Events to Dim_Patient**: Many-to-One (* to 1) via `Patient_ID`.
- **Fact_Hospital_Events to Dim_Department**: Many-to-One (* to 1) via `Department_ID`.
- **Fact_Hospital_Events to Dim_Calendar**: Many-to-One (* to 1) via `Event_Date`.
- **Cross-Filtering Direction**: Single-direction filtering from dimensions to the fact table to maximize performance.
