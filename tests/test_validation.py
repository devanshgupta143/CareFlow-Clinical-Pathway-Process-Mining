
from careflow.simulator import generate_baseline_visits
from careflow.validation import validate_dataset


def test_full_dataset_validation():
    (
        event_log,
        visits,
        long_wait_transitions,
        injection_records,
    ) = generate_baseline_visits()

    report = validate_dataset(
        event_log,
        visits,
        long_wait_transitions,
        injection_records,
    )

    print("\nCareFlow Validation Report")
    print("--------------------------")

    for name, value in report.items():
        print(f"{name}: {value}")

    print("\nWhole-dataset validation passed!")


if __name__ == "__main__":
    test_full_dataset_validation()
