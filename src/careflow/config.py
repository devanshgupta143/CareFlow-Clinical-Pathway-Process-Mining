
from datetime import datetime

# Simulation identity
PROJECT_NAME = "CareFlow"
RANDOM_SEED = 42

# Simulation window: January 2026
SIMULATION_START = datetime(2026, 1, 1, 0, 0, 0)
SIMULATION_END = datetime(2026, 1, 31, 0, 0, 0)

# Number of simulated outpatient visits
TOTAL_VISITS = 1_000

# Outpatient department operating hours
OPENING_HOUR = 9
CLOSING_HOUR = 17
OPERATING_DAYS = 6  # Monday to Saturday

# Baseline pathway allocation
DIRECT_VISITS = 600
DIAGNOSTIC_VISITS = 400

# Scenario probabilities
EXTENDED_ACTIVITY_PROBABILITY = 0.08
REWORK_PROBABILITY = 0.10
PATHWAY_DEVIATION_PROBABILITY = 0.05
INCOMPLETE_VISIT_PROBABILITY = 0.03

# Waiting-time injection
LONG_WAIT_PROPORTION = 0.15
BOTTLENECK_WEIGHT = 3

# Arrival-period weights
ARRIVAL_PERIOD_WEIGHTS = {
    "morning": 0.40,
    "midday": 0.15,
    "afternoon": 0.35,
    "late": 0.10,
}

# Activity durations in whole minutes:
# (ordinary minimum, ordinary mode, ordinary maximum,
#  extended minimum, extended maximum)
ACTIVITY_DURATIONS = {
    "Registration": (5, 10, 15, 16, 30),
    "Triage": (5, 10, 15, 16, 30),
    "Doctor_Consultation": (10, 20, 30, 31, 60),
    "Diagnostic_Test": (10, 20, 30, 31, 60),
    "Review_Results": (5, 10, 15, 16, 30),
    "Discharge": (5, 7.5, 10, 11, 20),
}

# Reference pathway templates
DIRECT_PATHWAY = [
    "Registration",
    "Triage",
    "Doctor_Consultation",
    "Discharge",
]

DIAGNOSTIC_PATHWAY = [
    "Registration",
    "Triage",
    "Doctor_Consultation",
    "Diagnostic_Test",
    "Review_Results",
    "Discharge",
]

# Primary bottleneck transitions
BOTTLENECK_TRANSITIONS = {
    ("Triage", "Doctor_Consultation"),
    ("Doctor_Consultation", "Diagnostic_Test"),
    ("Diagnostic_Test", "Review_Results"),
}


# Waiting-time distributions, measured in whole minutes
ORDINARY_WAIT_MIN = 5
ORDINARY_WAIT_MODE = 10
ORDINARY_WAIT_MAX = 20

LONG_WAIT_MIN = 30
LONG_WAIT_MODE = 45
LONG_WAIT_MAX = 90

