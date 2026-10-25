
from careflow.config import (
    TOTAL_VISITS,
    DIRECT_VISITS,
    DIAGNOSTIC_VISITS,
    ACTIVITY_DURATIONS,
    DIRECT_PATHWAY,
    DIAGNOSTIC_PATHWAY,
)

print("CareFlow configuration loaded successfully!")
print(f"Total visits: {TOTAL_VISITS}")
print(f"Direct visits: {DIRECT_VISITS}")
print(f"Diagnostic visits: {DIAGNOSTIC_VISITS}")
print(f"Activity types: {len(ACTIVITY_DURATIONS)}")
print(f"Direct pathway: {' -> '.join(DIRECT_PATHWAY)}")
print(f"Diagnostic pathway: {' -> '.join(DIAGNOSTIC_PATHWAY)}")

assert TOTAL_VISITS == DIRECT_VISITS + DIAGNOSTIC_VISITS
assert len(ACTIVITY_DURATIONS) == 6

print("All configuration checks passed!")
