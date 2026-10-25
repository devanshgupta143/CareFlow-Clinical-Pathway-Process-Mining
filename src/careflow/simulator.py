
import random
from datetime import datetime, timedelta
from careflow.scenarios import apply_visit_scenarios

from careflow.config import (
    ACTIVITY_DURATIONS,
    ARRIVAL_PERIOD_WEIGHTS,
    CLOSING_HOUR,
    DIAGNOSTIC_PATHWAY,
    DIAGNOSTIC_VISITS,
    DIRECT_PATHWAY,
    DIRECT_VISITS,
    EXTENDED_ACTIVITY_PROBABILITY,
    LONG_WAIT_PROPORTION,
    OPENING_HOUR,
    RANDOM_SEED,
    SIMULATION_END,
    SIMULATION_START,
    TOTAL_VISITS,
)


def get_operating_dates():
    """Return dates within the simulation window when the OPD is open."""
    dates = []
    current_date = SIMULATION_START.date()
    end_date = SIMULATION_END.date()

    while current_date < end_date:
        # Monday = 0; Sunday = 6.
        if current_date.weekday() < 6:
            dates.append(current_date)

        current_date += timedelta(days=1)

    return dates


def allocate_daily_visits(dates, total_visits, rng):
    """Allocate exactly the requested visit count across operating dates."""
    if not dates:
        raise ValueError("No operating dates found.")

    # Give each date a moderate random weight.
    weights = [rng.uniform(0.75, 1.25) for _ in dates]
    total_weight = sum(weights)

    exact_counts = [
        total_visits * weight / total_weight
        for weight in weights
    ]

    counts = [int(count) for count in exact_counts]
    remaining = total_visits - sum(counts)

    # Distribute remaining visits according to largest fractional parts.
    order = sorted(
        range(len(dates)),
        key=lambda i: exact_counts[i] - counts[i],
        reverse=True,
    )

    for index in order[:remaining]:
        counts[index] += 1

    return dict(zip(dates, counts))


def generate_arrival_time(date, rng, latest_minute=None):
    """Generate a registration start time within OPD hours."""
    periods = [
        ("morning", 9, 11),
        ("midday", 11, 14),
        ("afternoon", 14, 16),
        ("late", 16, 17),
    ]

    names = [period[0] for period in periods]
    weights = [ARRIVAL_PERIOD_WEIGHTS[name] for name in names]

    closing_minute = CLOSING_HOUR * 60
    if latest_minute is None:
        latest_minute = closing_minute - 1
    else:
        latest_minute = min(latest_minute, closing_minute)

    available_periods = [
        period
        for period in periods
        if period[0] in ARRIVAL_PERIOD_WEIGHTS
        and period[2] * 60 - 1 >= period[1] * 60
        and period[1] * 60 <= latest_minute
    ]
    if not available_periods:
        raise ValueError(
            "No arrival time can fit the visit before closing time."
        )

    available_names = [period[0] for period in available_periods]
    available_weights = [
        ARRIVAL_PERIOD_WEIGHTS[name]
        for name in available_names
    ]
    selected_name = rng.choices(
        available_names,
        weights=available_weights,
        k=1,
    )[0]
    _, start_hour, end_hour = next(
        period for period in available_periods
        if period[0] == selected_name
    )

    start_minute = start_hour * 60
    end_minute = min(end_hour * 60, latest_minute + 1)

    # Pick a whole-minute arrival in the chosen period.
    minute_of_day = rng.randrange(start_minute, end_minute)

    return datetime.combine(
        date,
        datetime.min.time(),
    ) + timedelta(minutes=minute_of_day)


def generate_activity_duration(activity_name, rng):
    """
    Generate an activity duration in whole minutes.

    Ordinary duration: triangular distribution.
    Extended duration: uniform integer distribution.
    """
    ordinary_min, ordinary_mode, ordinary_max, extended_min, extended_max = (
        ACTIVITY_DURATIONS[activity_name]
    )

    # Decide whether this activity gets an extended duration.
    is_extended = rng.random() < EXTENDED_ACTIVITY_PROBABILITY

    if is_extended:
        duration = rng.randint(extended_min, extended_max)
    else:
        duration = round(
            rng.triangular(
                ordinary_min,
                ordinary_max,
                ordinary_mode,
            )
        )

    return duration, is_extended


if __name__ == "__main__":
    rng = random.Random(RANDOM_SEED)

    for activity in ACTIVITY_DURATIONS:
        duration, is_extended = generate_activity_duration(activity, rng)

        print(
            f"{activity}: {duration} minutes "
            f"| Extended: {is_extended}"
        )


from careflow.config import (
    ORDINARY_WAIT_MIN,
    ORDINARY_WAIT_MODE,
    ORDINARY_WAIT_MAX,
    LONG_WAIT_MIN,
    LONG_WAIT_MODE,
    LONG_WAIT_MAX,
)


def generate_waiting_time(rng, is_long_wait=False):
    """Generate an ordinary or injected long wait in whole minutes."""

    if is_long_wait:
        minimum = LONG_WAIT_MIN
        mode = LONG_WAIT_MODE
        maximum = LONG_WAIT_MAX
    else:
        minimum = ORDINARY_WAIT_MIN
        mode = ORDINARY_WAIT_MODE
        maximum = ORDINARY_WAIT_MAX

    wait = round(rng.triangular(minimum, maximum, mode))

    return wait



def create_activity_event(case_id, activity_name, start_time, rng):
    """Create one timestamped activity event."""

    duration, is_extended = generate_activity_duration(
        activity_name, rng
    )

    end_time = start_time + timedelta(minutes=duration)

    event = {
        "Case_ID": case_id,
        "Activity_Name": activity_name,
        "Start_Timestamp": start_time,
        "End_Timestamp": end_time,
    }

    return event, is_extended




from careflow.config import BOTTLENECK_TRANSITIONS, BOTTLENECK_WEIGHT


def select_long_wait_transitions(pathways, rng):
    """Select an exact count of transitions using weighted sampling."""

    eligible = []

    for case_id, pathway in pathways.items():
        for index in range(len(pathway) - 1):
            from_activity = pathway[index]
            to_activity = pathway[index + 1]

            weight = (
                BOTTLENECK_WEIGHT
                if (from_activity, to_activity) in BOTTLENECK_TRANSITIONS
                else 1
            )

            eligible.append(
                (case_id, from_activity, to_activity, weight)
            )

    target_count = round(len(eligible) * LONG_WAIT_PROPORTION)

    if target_count > len(eligible):
        raise ValueError("Long-wait target exceeds eligible transitions.")

    remaining = eligible.copy()
    selected = set()

    for _ in range(target_count):
        total_weight = sum(item[3] for item in remaining)
        draw = rng.uniform(0, total_weight)
        cumulative_weight = 0

        for item in remaining:
            cumulative_weight += item[3]

            if draw <= cumulative_weight:
                selected.add(item[:3])
                remaining.remove(item)
                break

    return selected


def generate_baseline_visits():
    """Generate baseline visits with scenario injections."""

    rng = random.Random(RANDOM_SEED)

    operating_dates = get_operating_dates()
    daily_counts = allocate_daily_visits(
        operating_dates,
        TOTAL_VISITS,
        rng,
    )

    pathways_list = (
        [DIRECT_PATHWAY.copy() for _ in range(DIRECT_VISITS)]
        + [DIAGNOSTIC_PATHWAY.copy() for _ in range(DIAGNOSTIC_VISITS)]
    )
    rng.shuffle(pathways_list)

    # Apply the normal 20% diagnostic return loop first.
    for pathway in pathways_list:
        if (
            pathway == DIAGNOSTIC_PATHWAY
            and rng.random() < 0.20
        ):
            review_index = pathway.index("Review_Results")
            pathway.insert(review_index + 1, "Doctor_Consultation")

    visit_dates = []
    for date in operating_dates:
        visit_dates.extend([date] * daily_counts[date])

    visits = {}
    injection_records = []

    # Apply visit-level scenarios before selecting long waits.
    for index, (date, original_pathway) in enumerate(
        zip(visit_dates, pathways_list),
        start=1,
    ):
        case_id = f"CF{index:04d}"

        (
            modified_pathway,
            is_incomplete,
            incomplete_end_activity,
            records,
        ) = apply_visit_scenarios(
            case_id,
            original_pathway,
            rng,
        )

        visits[case_id] = {
            "pathway": modified_pathway,
            "arrival_time": None,
            "baseline_pathway": (
                "diagnostic"
                if "Diagnostic_Test" in original_pathway
                else "direct"
            ),
            "baseline_has_return_loop": (
                original_pathway.count("Doctor_Consultation") == 2
                and "Review_Results" in original_pathway
                and original_pathway[
                    original_pathway.index("Review_Results") + 1
                ] == "Doctor_Consultation"
            ),
            "is_incomplete": is_incomplete,
            "incomplete_end_activity": incomplete_end_activity,
        }

        injection_records.extend(records)

    # Select long waits from the final, modified pathways.
    pathway_mapping = {
        case_id: visit["pathway"]
        for case_id, visit in visits.items()
    }

    long_wait_transitions = select_long_wait_transitions(
        pathway_mapping,
        rng,
    )

    event_log = []

    for case_id, visit in visits.items():
        events = generate_visit_timeline(
            case_id=case_id,
            pathway=visit["pathway"],
            arrival_time=datetime.combine(
                visit_dates[int(case_id[2:]) - 1],
                datetime.min.time().replace(hour=OPENING_HOUR),
            ),
            rng=rng,
            long_wait_transitions=long_wait_transitions,
            injection_records=injection_records,
        )

        elapsed_minutes = int(
            (
                events[-1]["End_Timestamp"]
                - events[0]["Start_Timestamp"]
            ).total_seconds() / 60
        )
        arrival_time = generate_arrival_time(
            events[0]["Start_Timestamp"].date(),
            rng,
            latest_minute=CLOSING_HOUR * 60 - elapsed_minutes,
        )
        shift = arrival_time - events[0]["Start_Timestamp"]
        for event in events:
            event["Start_Timestamp"] += shift
            event["End_Timestamp"] += shift

        visit["arrival_time"] = arrival_time
        event_log.extend(events)

    # Assign stable injection IDs.
    for index, record in enumerate(injection_records, start=1):
        record["Injection_ID"] = f"INJ{index:04d}"

    # Sort raw events and preserve exactly four columns.
    event_log.sort(
        key=lambda event: (
            event["Case_ID"],
            event["Start_Timestamp"],
        )
    )

    expected_columns = {
        "Case_ID",
        "Activity_Name",
        "Start_Timestamp",
        "End_Timestamp",
    }

    assert len(visits) == TOTAL_VISITS
    assert len({event["Case_ID"] for event in event_log}) == TOTAL_VISITS
    assert all(set(event.keys()) == expected_columns for event in event_log)

    return event_log, visits, long_wait_transitions, injection_records


def generate_visit_timeline(
    case_id,
    pathway,
    arrival_time,
    rng,
    long_wait_transitions=None,
    injection_records=None,
):
    """Generate timestamped events and optionally record injections."""

    if long_wait_transitions is None:
        long_wait_transitions = set()

    events = []
    current_start = arrival_time

    for index, activity_name in enumerate(pathway):
        event, is_extended = create_activity_event(
            case_id,
            activity_name,
            current_start,
            rng,
        )
        events.append(event)

        # Record extended activity duration separately.
        if is_extended and injection_records is not None:
            duration_minutes = int(
                (
                    event["End_Timestamp"]
                    - event["Start_Timestamp"]
                ).total_seconds() / 60
            )

            injection_records.append({
                "Case_ID": case_id,
                "Scenario_Type": "Extended_Duration",
                "Operation_Type": "Extend_Activity",
                "Activity_Name": activity_name,
                "From_Activity": "",
                "To_Activity": "",
                "Injected_Value": duration_minutes,
                "Details": "Activity duration sampled from extended range",
            })

        if index < len(pathway) - 1:
            next_activity = pathway[index + 1]

            transition = (
                case_id,
                activity_name,
                next_activity,
            )
            is_long_wait = transition in long_wait_transitions

            waiting_time = generate_waiting_time(
                rng,
                is_long_wait=is_long_wait,
            )

            # Record long waits separately.
            if is_long_wait and injection_records is not None:
                injection_records.append({
                    "Case_ID": case_id,
                    "Scenario_Type": "Long_Wait",
                    "Operation_Type": "Extend_Wait",
                    "Activity_Name": "",
                    "From_Activity": activity_name,
                    "To_Activity": next_activity,
                    "Injected_Value": waiting_time,
                    "Details": "Selected long-wait transition",
                })

            current_start = (
                event["End_Timestamp"]
                + timedelta(minutes=waiting_time)
            )

    return events
