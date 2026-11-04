# Star Schema Data Model Architecture

## Model Overview

- **Architecture Type**: Star schema with a case-grain hub and event/transition facts.
- **Facts**: `Cases` (one row per encounter), `Events`, `Transitions`,
  `StageMetrics`, `Bottlenecks`, `VariantFrequency`, and `VariantFlows`.
- **Dimensions**: `DimDate`, `DimActivity`, `DimDepartment`, `DimDiagnosis`,
  `DimResource`, and `DimVariant`.

## Generated Power BI model

The PM4Py exporter now defines the concrete `Cases`, `Events`, `Transitions`,
stage/bottleneck, variant-flow and dimension table schemas. See
[docs/power_bi_integration.md](docs/power_bi_integration.md) for field-level
definitions, relationship cardinalities, DAX measures, and PBIP import steps.
