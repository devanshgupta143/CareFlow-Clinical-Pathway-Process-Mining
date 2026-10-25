
import random

from careflow.config import LONG_WAIT_PROPORTION
from careflow.simulator import select_long_wait_transitions


def test_exact_long_wait_selection():
    pathways = {
        f"CF{i:04d}": [
            "Registration",
            "Triage",
            "Doctor_Consultation",
            "Discharge",
        ]
        for i in range(1, 101)
    }

    rng = random.Random(42)

    selected = select_long_wait_transitions(pathways, rng)

    total_transitions = sum(
        len(pathway) - 1 for pathway in pathways.values()
    )
    expected_count = round(total_transitions * LONG_WAIT_PROPORTION)

    assert len(selected) == expected_count
    assert len(selected) == len(set(selected))

    print(f"Eligible transitions: {total_transitions}")
    print(f"Required long waits: {expected_count}")
    print(f"Selected long waits: {len(selected)}")
    print("Long-wait selection tests passed!")


if __name__ == "__main__":
    test_exact_long_wait_selection()
