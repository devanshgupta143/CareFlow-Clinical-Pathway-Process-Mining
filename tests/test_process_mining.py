import pandas as pd
import pytest

from src.process_mining import build_tables, export_tables


def test_build_tables_normalizes_events_and_calculates_waits(tmp_path):
    event_path = tmp_path / "events.csv"
    pd.DataFrame(
        [
            {
                "Case ID": "P1",
                "Activity": "Registration",
                "Start_Timestamp": "2026-01-05 08:00:00",
                "End_Timestamp": "2026-01-05 08:10:00",
                "Department": "Emergency",
                "Diagnosis": "Infection",
            },
            {
                "Case ID": "P1",
                "Activity": "Diagnostic_Test",
                "Start_Timestamp": "2026-01-05 08:40:00",
                "End_Timestamp": "2026-01-05 09:00:00",
                "Department": "Emergency",
                "Diagnosis": "Infection",
            },
            {
                "Case ID": "P2",
                "Activity": "Registration",
                "Start_Timestamp": "2026-01-06 09:00:00",
                "End_Timestamp": "2026-01-06 09:15:00",
                "Department": "Surgery",
                "Diagnosis": "Injury",
            },
        ]
    ).to_csv(event_path, index=False)
    metadata_path = tmp_path / "cases.csv"
    pd.DataFrame(
        [
            {"Case_ID": "P1", "IsReadmitted": "true", "PatientSatisfactionPct": 82},
            {"Case_ID": "P2", "IsReadmitted": "false", "PatientSatisfactionPct": 94},
        ]
    ).to_csv(metadata_path, index=False)

    tables = build_tables(event_path, metadata_path)

    assert len(tables["Events"]) == 3
    assert tables["Events"].loc[1, "WaitHours"] == pytest.approx(0.5)
    assert tables["Cases"].set_index("CaseID").loc["P1", "DurationHours"] == pytest.approx(1)
    assert bool(tables["Cases"].set_index("CaseID").loc["P1", "IsReadmitted"])
    assert tables["Cases"].set_index("CaseID").loc["P1", "PatientSatisfactionPct"] == 82
    assert tables["Bottlenecks"].set_index("ProcessStep").loc[
        "Diagnostic_Test", "DiagnosticWaitCount"
    ] == 1
    assert set(tables["VariantFrequency"]["CaseCount"]) == {1}
    assert "Start" in set(tables["VariantFlows"]["Source"])
    assert "End" in set(tables["VariantFlows"]["Target"])

    exported = export_tables(tables, tmp_path / "processed", "csv")
    assert len(exported) == len(tables)
    assert (tmp_path / "processed" / "Cases.csv").is_file()


def test_build_tables_rejects_bad_event_rows(tmp_path):
    event_path = tmp_path / "events.csv"
    pd.DataFrame(
        [{"CaseID": "P1", "Activity": "Triage", "Timestamp": "not a timestamp"}]
    ).to_csv(event_path, index=False)

    with pytest.raises(ValueError, match="invalid event row"):
        build_tables(event_path)


def test_build_tables_rejects_duplicate_case_metadata(tmp_path):
    event_path = tmp_path / "events.csv"
    pd.DataFrame(
        [{"CaseID": "P1", "Activity": "Triage", "Timestamp": "2026-01-01 08:00"}]
    ).to_csv(event_path, index=False)
    metadata_path = tmp_path / "cases.csv"
    pd.DataFrame(
        [
            {"CaseID": "P1", "IsReadmitted": "true"},
            {"CaseID": "P1", "IsReadmitted": "false"},
        ]
    ).to_csv(metadata_path, index=False)

    with pytest.raises(ValueError, match="duplicate CaseID"):
        build_tables(event_path, metadata_path)
