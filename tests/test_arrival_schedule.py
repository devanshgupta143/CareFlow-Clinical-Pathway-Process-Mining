
import random

from careflow.simulator import (
    get_operating_dates,
    allocate_daily_visits,
    generate_arrival_time,
)
from careflow.config import TOTAL_VISITS


def test_arrival_schedule():
    rng = random.Random(42)

    dates = get_operating_dates()
    daily_counts = allocate_daily_visits(
        dates,
        TOTAL_VISITS,
        rng,
    )

    assert len(dates) == 26
    assert sum(daily_counts.values()) == 1000
    assert all(count > 0 for count in daily_counts.values())

    for date in dates:
        for _ in range(daily_counts[date]):
            arrival = generate_arrival_time(date, rng)

            assert arrival.date() == date
            assert 9 <= arrival.hour < 17

    print(f"Operating dates: {len(dates)}")
    print(f"Total allocated visits: {sum(daily_counts.values())}")
    print(f"Minimum daily visits: {min(daily_counts.values())}")
    print(f"Maximum daily visits: {max(daily_counts.values())}")
    print("Arrival schedule tests passed!")


if __name__ == "__main__":
    test_arrival_schedule()
