
import random
from datetime import datetime

from careflow.simulator import generate_visit_timeline


def test_direct_visit_with_long_wait():
    rng = random.Random(42)

    case_id = "CF0001"

    pathway = [
        "Registration",
        "Triage",
        "Doctor_Consultation",
        "Discharge",
    ]

    arrival_time = datetime(2026, 1, 5, 9, 0, 0)

    # Force a long wait between Registration and Triage.
    long_wait_transitions = {
        ("CF0001", "Registration", "Triage")
    }

    events = generate_visit_timeline(
        case_id,
        pathway,
        arrival_time,
        rng,
        long_wait_transitions=long_wait_transitions,
    )

    # Display the generated events.
    for event in events:
        print(event)

    # Check that the correct activities were generated.
    assert [event["Activity_Name"] for event in events] == pathway

    # Calculate the wait between Registration and Triage.
    registration_end = events[0]["End_Timestamp"]
    triage_start = events[1]["Start_Timestamp"]

    waiting_minutes = int(
        (triage_start - registration_end).total_seconds() / 60
    )

    print(f"\nRegistration to Triage wait: {waiting_minutes} minutes")

    # A selected long wait must be between 30 and 90 minutes.
    assert 30 <= waiting_minutes <= 90, (
        f"Expected a long wait between 30 and 90 minutes, "
        f"but got {waiting_minutes} minutes."
    )

    # Check that activities remain chronological and do not overlap.
    for index in range(len(events) - 1):
        assert (
            events[index]["End_Timestamp"]
            <= events[index + 1]["Start_Timestamp"]
        )

    print("Direct visit long-wait test passed!")


if __name__ == "__main__":
    test_direct_visit_with_long_wait()
