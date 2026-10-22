# Data Model Integrity & Verification Rules

## Integrity Constraints
1. **Primary Key Uniqueness**:
   - `Dim_Patient[Patient_ID]` must contain zero duplicate keys.
   - `Dim_Department[Department_ID]` must contain unique ward identifiers.

2. **Referential Integrity**:
   - Every `Patient_ID` in `Fact_Hospital_Events` must resolve to a valid record in `Dim_Patient`. Unmatched keys must be assigned to 'UNKNOWN_PATIENT'.

3. **Relationship Cardinality & Cross-Filtering**:
   - `Dim_Patient` (1) to `Fact_Hospital_Events` (*) | Single Direction
   - `Dim_Department` (1) to `Fact_Hospital_Events` (*) | Single Direction
   - `Dim_Calendar` (1) to `Fact_Hospital_Events` (*) | Single Direction
