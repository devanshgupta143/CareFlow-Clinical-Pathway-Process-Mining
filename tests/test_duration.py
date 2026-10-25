
import random

from careflow.config import ACTIVITY_DURATIONS
from careflow.simulator import generate_activity_duration


def test_all_activities_return_valid_durations():
    rng = random.Random(42)

    for activity_name, ranges in ACTIVITY_DURATIONS.items():
        ordinary_min, _, ordinary_max, extended_min, extended_max = ranges

        for _ in range(100):
            duration, is_extended = generate_activity_duration(
                activity_name, rng
            )

            assert isinstance(duration, int)
            assert isinstance(is_extended, bool)

            if is_extended:
                assert extended_min <= duration <= extended_max
            else:
                assert ordinary_min <= duration <= ordinary_max


if __name__ == "__main__":
    test_all_activities_return_valid_durations()
    print("All activity-duration tests passed!")
