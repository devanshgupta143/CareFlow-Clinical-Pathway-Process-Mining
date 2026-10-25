
import random

from careflow.config import (
    ORDINARY_WAIT_MIN,
    ORDINARY_WAIT_MAX,
    LONG_WAIT_MIN,
    LONG_WAIT_MAX,
)
from careflow.simulator import generate_waiting_time


def test_waiting_times_stay_within_configured_ranges():
    rng = random.Random(42)

    for _ in range(500):
        ordinary_wait = generate_waiting_time(rng)
        long_wait = generate_waiting_time(rng, is_long_wait=True)

        assert ORDINARY_WAIT_MIN <= ordinary_wait <= ORDINARY_WAIT_MAX
        assert LONG_WAIT_MIN <= long_wait <= LONG_WAIT_MAX


if __name__ == "__main__":
    test_waiting_times_stay_within_configured_ranges()
    print("All waiting-time tests passed!")
