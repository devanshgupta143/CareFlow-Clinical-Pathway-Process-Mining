
import csv

from careflow.simulator import generate_baseline_visits
from careflow.validation import validate_dataset
from careflow.export import export_careflow_data


def read_csv(path):
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames, list(reader)


def test_export():
    (
        event_log,
        visits,
        long_wait_transitions,
        injection_records,
    ) = generate_baseline_visits()

    # Validate before exporting.
    validate_dataset(
        event_log,
        visits,
        long_wait_transitions,
        injection_records,
    )

    paths = export_careflow_data(
        event_log,
        visits,
        injection_records,
    )

    event_columns, event_rows = read_csv(paths["event_log"])
    metadata_columns, metadata_rows = read_csv(paths["case_metadata"])
    injection_columns, injection_rows = read_csv(paths["injection_log"])

    assert event_columns == [
        "Case_ID",
        "Activity_Name",
        "Start_Timestamp",
        "End_Timestamp",
    ]

    assert len(event_rows) == len(event_log)
    assert len(metadata_rows) == 1000
    assert len(injection_rows) == len(injection_records)

    assert len(metadata_columns) == 4
    assert len(injection_columns) == 9

    assert event_rows[0]["Start_Timestamp"].endswith(":00")

    print("Event log rows:", len(event_rows))
    print("Case metadata rows:", len(metadata_rows))
    print("Injection log rows:", len(injection_rows))

    for name, path in paths.items():
        print(f"{name}: {path}")

    print("CSV export tests passed!")


if __name__ == "__main__":
    test_export()
