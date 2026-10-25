
from collections import Counter, defaultdict

from careflow.config import (
    TOTAL_VISITS,
    DIRECT_VISITS,
    DIAGNOSTIC_VISITS,
    SIMULATION_START,
    SIMULATION_END,
    ACTIVITY_DURATIONS,
    CLOSING_HOUR,
    DIRECT_PATHWAY,
    DIAGNOSTIC_PATHWAY,
)


EXPECTED_EVENT_COLUMNS = {
    "Case_ID",
    "Activity_Name",
    "Start_Timestamp",
    "End_Timestamp",
}

ALLOWED_SCENARIOS = {
    "Extended_Duration",
    "Rework",
    "Pathway_Deviation",
    "Incomplete_Visit",
    "Long_Wait",
}


def validate_dataset(
    event_log,
    visits,
    long_wait_transitions,
    injection_records,
):
    """Validate CareFlow's generated dataset; raise on invalid data."""

    errors = []

    # 1. Check total visits and baseline pathway counts.
    if len(visits) != TOTAL_VISITS:
        errors.append(
            f"Expected {TOTAL_VISITS} visits; found {len(visits)}."
        )

    baseline_counts = Counter(
        visit["baseline_pathway"]
        for visit in visits.values()
    )

    if baseline_counts["direct"] != DIRECT_VISITS:
        errors.append(
            f"Expected {DIRECT_VISITS} direct visits; "
            f"found {baseline_counts['direct']}."
        )

    if baseline_counts["diagnostic"] != DIAGNOSTIC_VISITS:
        errors.append(
            f"Expected {DIAGNOSTIC_VISITS} diagnostic visits; "
            f"found {baseline_counts['diagnostic']}."
        )

    # 2. Check the raw event-log schema and group events by visit.
    events_by_case = defaultdict(list)
    known_case_ids = set(visits)

    for row_number, event in enumerate(event_log, start=1):
        if set(event.keys()) != EXPECTED_EVENT_COLUMNS:
            errors.append(
                f"Event row {row_number} does not have exactly "
                "the four required columns."
            )
            continue

        case_id = event["Case_ID"]
        activity = event["Activity_Name"]
        start = event["Start_Timestamp"]
        end = event["End_Timestamp"]

        if case_id not in known_case_ids:
            errors.append(
                f"Event row {row_number} refers to unknown case {case_id}."
            )
            continue

        if activity not in ACTIVITY_DURATIONS:
            errors.append(
                f"Unknown activity {activity!r} in case {case_id}."
            )

        if not hasattr(start, "strftime") or not hasattr(end, "strftime"):
            errors.append(
                f"Invalid timestamp type in case {case_id}."
            )
            continue

        if start > end:
            errors.append(
                f"Activity starts after it ends in case {case_id}."
            )

        if start < SIMULATION_START or start >= SIMULATION_END:
            errors.append(
                f"Activity start is outside the simulation window "
                f"in case {case_id}: {start}."
            )

        if end < SIMULATION_START or end >= SIMULATION_END:
            errors.append(
                f"Activity end is outside the simulation window "
                f"in case {case_id}: {end}."
            )

        if start.weekday() == 6 or end.weekday() == 6:
            errors.append(
                f"Activity occurs on Sunday in case {case_id}: "
                f"{activity}."
            )

        if end.hour > CLOSING_HOUR or (
            end.hour == CLOSING_HOUR
            and (end.minute > 0 or end.second > 0)
        ):
            errors.append(
                f"Activity ends after operating hours in case {case_id}: "
                f"{end}."
            )

        events_by_case[case_id].append(event)

    # 3. Every visit must have at least one event.
    missing_cases = known_case_ids - set(events_by_case)

    for case_id in sorted(missing_cases):
        errors.append(f"Visit {case_id} has no event records.")

    # 4. Check chronology and non-overlapping activity intervals.
    for case_id, events in events_by_case.items():
        events.sort(key=lambda row: row["Start_Timestamp"])

        for previous, current in zip(events, events[1:]):
            if current["Start_Timestamp"] < previous["End_Timestamp"]:
                errors.append(
                    f"Overlapping activities in case {case_id}: "
                    f"{previous['Activity_Name']} and "
                    f"{current['Activity_Name']}."
                )

    # 5. Check incomplete-visit metadata against the event log.
    for case_id, visit in visits.items():
        case_events = events_by_case.get(case_id, [])

        if not case_events:
            continue

        case_events.sort(key=lambda row: row["Start_Timestamp"])
        final_activity = case_events[-1]["Activity_Name"]

        if visit["is_incomplete"]:
            if final_activity == "Discharge":
                errors.append(
                    f"Incomplete visit {case_id} contains Discharge."
                )

            if final_activity != visit["incomplete_end_activity"]:
                errors.append(
                    f"Incomplete endpoint mismatch for {case_id}: "
                    f"metadata says {visit['incomplete_end_activity']!r}, "
                    f"event log ends with {final_activity!r}."
                )
        else:
            if visit["incomplete_end_activity"] != "":
                errors.append(
                    f"Complete visit {case_id} has an incomplete endpoint."
                )

    # 6. Check scenario records.
    injection_ids = set()

    for record in injection_records:
        case_id = record.get("Case_ID")
        scenario_type = record.get("Scenario_Type")
        injection_id = record.get("Injection_ID")

        if case_id not in known_case_ids:
            errors.append(
                f"Injection refers to unknown case {case_id!r}."
            )

        if scenario_type not in ALLOWED_SCENARIOS:
            errors.append(
                f"Unknown scenario type {scenario_type!r}."
            )

        if not injection_id:
            errors.append("An injection record has no Injection_ID.")
        elif injection_id in injection_ids:
            errors.append(f"Duplicate Injection_ID: {injection_id}.")
        else:
            injection_ids.add(injection_id)

    # 7. Confirm long-wait records and selection counts agree.
    recorded_long_waits = [
        record for record in injection_records
        if record.get("Scenario_Type") == "Long_Wait"
    ]

    if len(recorded_long_waits) != len(long_wait_transitions):
        errors.append(
            "Long-wait record count does not match selected "
            f"transitions: {len(recorded_long_waits)} records versus "
            f"{len(long_wait_transitions)} selected transitions."
        )

    if errors:
        preview = "\n".join(f"- {error}" for error in errors[:25])
        remaining = len(errors) - 25

        if remaining > 0:
            preview += f"\n- ...and {remaining} more errors."

        raise ValueError(
            f"CareFlow validation failed with {len(errors)} error(s):\n"
            f"{preview}"
        )

    return {
        "visits": len(visits),
        "events": len(event_log),
        "direct_visits": baseline_counts["direct"],
        "diagnostic_visits": baseline_counts["diagnostic"],
        "injection_records": len(injection_records),
        "selected_long_waits": len(long_wait_transitions),
        "status": "PASS",
    }
