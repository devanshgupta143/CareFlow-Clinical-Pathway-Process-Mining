
import csv
from pathlib import Path


EVENT_COLUMNS = [
    "Case_ID",
    "Activity_Name",
    "Start_Timestamp",
    "End_Timestamp",
]

METADATA_COLUMNS = [
    "Case_ID",
    "Baseline_Pathway",
    "Is_Incomplete",
    "Incomplete_End_Activity",
]

INJECTION_COLUMNS = [
    "Injection_ID",
    "Case_ID",
    "Scenario_Type",
    "Operation_Type",
    "Activity_Name",
    "From_Activity",
    "To_Activity",
    "Injected_Value",
    "Details",
]


def write_csv(file_path, columns, rows):
    """Write dictionaries to a CSV file with a fixed column order."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=columns,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)

    return file_path


def export_careflow_data(
    event_log,
    visits,
    injection_records,
    raw_dir="data/raw",
    metadata_dir="data/metadata",
):
    """Export CareFlow event log, case metadata, and injection log."""

    raw_dir = Path(raw_dir)
    metadata_dir = Path(metadata_dir)

    event_path = write_csv(
        raw_dir / "event_log.csv",
        EVENT_COLUMNS,
        [
            {
                **event,
                "Start_Timestamp": event["Start_Timestamp"].strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "End_Timestamp": event["End_Timestamp"].strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
            for event in event_log
        ],
    )

    metadata_rows = []

    for case_id, visit in visits.items():
        metadata_rows.append({
            "Case_ID": case_id,
            "Baseline_Pathway": visit["baseline_pathway"],
            "Is_Incomplete": visit["is_incomplete"],
            "Incomplete_End_Activity": (
                visit["incomplete_end_activity"]
            ),
        })

    metadata_path = write_csv(
        metadata_dir / "case_metadata.csv",
        METADATA_COLUMNS,
        metadata_rows,
    )

    injection_path = write_csv(
        metadata_dir / "injection_log.csv",
        INJECTION_COLUMNS,
        injection_records,
    )

    return {
        "event_log": event_path,
        "case_metadata": metadata_path,
        "injection_log": injection_path,
    }
