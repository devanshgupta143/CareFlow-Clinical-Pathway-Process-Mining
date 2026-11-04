# Power BI Dashboard Architecture & Wireframe

## Executive Summary (1920 x 1080)

- **Canvas:** pale slate background, navy headings, deep-teal chart accents,
  soft-gray/white cards, and slate body text.
- **Top bar (y=16-152):** report title and model-refresh timestamp, followed by
  date-range and department slicers. An activity slicer is included because the
  loaded event log has no clinical service-line field.
- **KPI row (y=170-300):** total patient cases, average pathway duration in
  fractional days, average wait between consecutive events in hours, and
  repeated-activity rework rate.
- **Analysis row (y=340-780):** bottleneck chart by activity on the left and
  pathway-variant case frequency on the right, sorted from most frequent.
- **Detail row (y=800-1060):** department/activity wait-time matrix.

## Additional Report Page

Clinical Pathway Rework & Loop Analysis shows rework cases by department and an
activity-repeat matrix, using the same 1920 x 1080 canvas and visual theme.

## Data Readiness Notes

The loaded event table currently contains only `Case_ID`, `Activity_Name`,
`Timestamp`, and `Department`. The provided baseline metadata does not join to
the loaded event IDs, and no `IsStandardPath` or clinical service-line field
exists in the model. Consequently, adherence-to-guideline and service-line
filtering are intentionally not displayed until those inputs are reconciled.
