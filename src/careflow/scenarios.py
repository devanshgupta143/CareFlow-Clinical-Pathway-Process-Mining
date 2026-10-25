
import random

from careflow.config import (
    REWORK_PROBABILITY,
    PATHWAY_DEVIATION_PROBABILITY,
    INCOMPLETE_VISIT_PROBABILITY,
)


def apply_visit_scenarios(case_id, pathway, rng):
    """
    Apply independent visit-level scenarios.

    Returns:
        modified_pathway: the pathway after scenario injection
        is_incomplete: whether the visit ends without Discharge
        incomplete_end_activity: final activity for incomplete visits
        records: scenario records without Injection_ID
    """

    pathway = pathway.copy()
    records = []

    # Scenario probabilities are independent.
    # A visit may receive more than one scenario.

    # 1. Rework: repeat one eligible activity exactly once.
    if rng.random() < REWORK_PROBABILITY:
        eligible = [
            activity
            for activity in (
                "Triage",
                "Doctor_Consultation",
                "Diagnostic_Test",
            )
            if activity in pathway
        ]

        if eligible:
            activity = rng.choice(eligible)
            position = pathway.index(activity)
            pathway.insert(position + 1, activity)

            records.append({
                "Case_ID": case_id,
                "Scenario_Type": "Rework",
                "Operation_Type": "Repeat_Activity",
                "Activity_Name": activity,
                "From_Activity": activity,
                "To_Activity": activity,
                "Injected_Value": "",
                "Details": "One additional occurrence of an activity",
            })

    # 2. Other pathway deviation.
    if rng.random() < PATHWAY_DEVIATION_PROBABILITY:
        # A diagnostic test and its results review form a dependent
        # sequence. Skip both together when using the skip operation.
        if rng.random() < 0.5:
            if (
                "Diagnostic_Test" in pathway
                and "Review_Results" in pathway
            ):
                pathway.remove("Diagnostic_Test")
                pathway.remove("Review_Results")

                records.append({
                    "Case_ID": case_id,
                    "Scenario_Type": "Pathway_Deviation",
                    "Operation_Type": "Skip_Sequence",
                    "Activity_Name": "",
                    "From_Activity": "Diagnostic_Test",
                    "To_Activity": "Review_Results",
                    "Injected_Value": "",
                    "Details": (
                        "Diagnostic sequence skipped as a simulated "
                        "pathway deviation"
                    ),
                })
            else:
                # For direct pathways, skip one eligible activity.
                eligible = [
                    activity
                    for activity in ("Triage", "Doctor_Consultation")
                    if activity in pathway
                ]

                if eligible:
                    activity = rng.choice(eligible)
                    pathway.remove(activity)

                    records.append({
                        "Case_ID": case_id,
                        "Scenario_Type": "Pathway_Deviation",
                        "Operation_Type": "Skip_Activity",
                        "Activity_Name": activity,
                        "From_Activity": "",
                        "To_Activity": "",
                        "Injected_Value": "",
                        "Details": (
                            "Activity skipped as a simulated "
                            "pathway deviation"
                        ),
                    })
        else:
            # No adjacent swap is defined as valid for the current
            # reference pathways. Record the fallback explicitly.
            eligible = [
                activity
                for activity in ("Triage", "Doctor_Consultation")
                if activity in pathway
            ]

            if eligible:
                activity = rng.choice(eligible)
                pathway.remove(activity)

                records.append({
                    "Case_ID": case_id,
                    "Scenario_Type": "Pathway_Deviation",
                    "Operation_Type": "Skip_Activity",
                    "Activity_Name": activity,
                    "From_Activity": "",
                    "To_Activity": "",
                    "Injected_Value": "",
                    "Details": (
                        "Fallback skip used because no approved "
                        "adjacent reorder exists in the reference path"
                    ),
                })

    # 3. Incomplete visit: end at an eligible activity, without Discharge.
    is_incomplete = rng.random() < INCOMPLETE_VISIT_PROBABILITY
    incomplete_end_activity = ""

    if is_incomplete:
        eligible_endings = [
            activity
            for activity in (
                "Triage",
                "Doctor_Consultation",
                "Diagnostic_Test",
                "Review_Results",
            )
            if activity in pathway
        ]

        if eligible_endings:
            incomplete_end_activity = rng.choice(eligible_endings)
            stop_index = pathway.index(incomplete_end_activity)
            pathway = pathway[:stop_index + 1]

            records.append({
                "Case_ID": case_id,
                "Scenario_Type": "Incomplete_Visit",
                "Operation_Type": "Truncate_Pathway",
                "Activity_Name": incomplete_end_activity,
                "From_Activity": "",
                "To_Activity": "",
                "Injected_Value": "",
                "Details": (
                    "Simulated journey ends without a Discharge event; "
                    "this does not establish why the visit ended"
                ),
            })
        else:
            is_incomplete = False

    return (
        pathway,
        is_incomplete,
        incomplete_end_activity,
        records,
    )
