
from collections import Counter

from careflow.simulator import generate_baseline_visits


def test_scenario_generator():
    event_log, visits, long_wait_transitions, injection_records = (
        generate_baseline_visits()
    )

    direct_visits = [
        visit for visit in visits.values()
        if visit["baseline_pathway"] == "direct"
    ]

    diagnostic_visits = [
        visit for visit in visits.values()
        if visit["baseline_pathway"] == "diagnostic"
    ]

    return_loop_visits = [
        visit for visit in diagnostic_visits
        if visit["baseline_has_return_loop"]
    ]

    scenario_counts = Counter(
        record["Scenario_Type"]
        for record in injection_records
    )

    assert len(visits) == 1000
    assert len(direct_visits) == 600
    assert len(diagnostic_visits) == 400

    expected_columns = {
        "Case_ID",
        "Activity_Name",
        "Start_Timestamp",
        "End_Timestamp",
    }
    assert all(set(event) == expected_columns for event in event_log)

    assert all(
        visit["is_incomplete"]
        == (visit["incomplete_end_activity"] != "")
        for visit in visits.values()
    )

    # Incomplete visits must end without Discharge.
    incomplete_ids = {
        case_id
        for case_id, visit in visits.items()
        if visit["is_incomplete"]
    }
    for case_id in incomplete_ids:
        activities = [
            event["Activity_Name"]
            for event in event_log
            if event["Case_ID"] == case_id
        ]
        assert activities[-1] != "Discharge"

    print(f"Generated visits: {len(visits)}")
    print(f"Generated events: {len(event_log)}")
    print(f"Direct visits: {len(direct_visits)}")
    print(f"Diagnostic visits: {len(diagnostic_visits)}")
    print(f"Diagnostic return loops: {len(return_loop_visits)}")
    print(f"Incomplete visits: {len(incomplete_ids)}")
    print(f"Long waits selected: {len(long_wait_transitions)}")
    print(f"Injection records: {len(injection_records)}")
    print(f"Scenario counts: {dict(scenario_counts)}")
    print("Scenario generator tests passed!")


if __name__ == "__main__":
    test_scenario_generator()
