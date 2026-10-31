INCLUDED_HOURS = {"infant": 20, "toddler": 25, "preschool": 30}


def extra_hours_fee(age_group, hours, has_sibling):
    if age_group not in INCLUDED_HOURS:
        raise ValueError("unknown age group")
    if hours < 0:
        raise ValueError("invalid hours")
    included = INCLUDED_HOURS[age_group]
    if has_sibling and age_group != "infant":
        included += 5
    extra = hours - included
    if extra <= 0:
        return 0
    if age_group == "infant":
        rate = 14
    else:
        rate = 9
    if extra > 20:
        rate = rate + 5
        if age_group == "infant":
            rate += 3
    return extra * rate


def enrolment_allowed(age_months, vacancies, is_immunisation_pending):
    if is_immunisation_pending:
        return age_months >= 12
    if age_months < 6:
        return False
    return vacancies >= 1


def pickup_status(minutes_left, is_aftercare, is_friday):
    if is_aftercare:
        cutoff = 20
    else:
        cutoff = 10
    if is_friday:
        cutoff += 10
    if minutes_left >= cutoff:
        return "on_time"
    elif minutes_left >= cutoff - 15:
        return "late"
    return "overdue"
