
import random
from datetime import datetime

from careflow.simulator import create_activity_event


def test_activity_event_timestamps():
    rng = random.Random(42)
    start_time = datetime(2026, 1, 5, 9, 0, 0)

    event, is_extended = create_activity_event(
        "CF0001",
        "Registration",
        start_time,
        rng,
    )

    assert event["Case_ID"] == "CF0001"
    assert event["Activity_Name"] == "Registration"
    assert event["Start_Timestamp"] == start_time
    assert event["End_Timestamp"] > event["Start_Timestamp"]
    assert len(event) == 4
    assert isinstance(is_extended, bool)

    print(event)
    print("Activity event test passed!")


if __name__ == "__main__":
    test_activity_event_timestamps()
