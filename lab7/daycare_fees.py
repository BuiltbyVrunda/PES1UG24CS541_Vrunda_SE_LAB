"""Daycare fees - Lab 7 (fuzz-hardened version).

Parses enrolment details, averages weekly hours and works out the payable fee
after a discount.

Design rule found through fuzzing: every public function is *total*.  For ANY
input (wrong type, empty, malformed, hostile numbers) it returns a result
instead of raising.  Invalid input is rejected by returning ``None``, and the
caller decides how to report it (``main`` prints a friendly message).
"""
import math
import re

# ----------------------------------------------------------------------------
# Limits (defensive bounds so nothing absurd gets through)
# ----------------------------------------------------------------------------
GST_MULTIPLIER = 1.18        # 18% tax added on top of the base fee
MAX_INPUT_LEN = 10_000       # refuse giant strings (cheap DoS guard)
MAX_AGE_GROUP_LEN = 50
MAX_WEEKLY_HOURS = 168       # 24 * 7 - nobody attends more hours than a week has
MAX_FEE = 10_000_000         # sanity ceiling for a fee or discount amount

# Plain ASCII decimal only: no sign, no exponent, no "nan"/"inf", no "1_000",
# no non-ASCII digits (all of which float()/int() would happily accept).
_DECIMAL = re.compile(r"\d+(?:\.\d+)?", re.ASCII)


def _is_valid_text(value):
    """True only for a str of sane length (rejects None, numbers, bytes ...)."""
    return isinstance(value, str) and len(value) <= MAX_INPUT_LEN


def _to_number(token, upper):
    """Convert a token to a finite float in [0, upper], else None."""
    token = token.strip()
    if not _DECIMAL.fullmatch(token):
        return None
    number = float(token)
    if not math.isfinite(number) or number > upper:  # e.g. 400 digits -> inf
        return None
    return number


def parse_enrolment(text):
    """Parse ``"<age group>:<hours>"`` -> ``(Age Group, hours)`` or None."""
    if not _is_valid_text(text):
        return None
    parts = text.split(":")
    if len(parts) != 2:              # "toddler", "a:b:c", ""
        return None
    age_group = parts[0].strip()
    if (not age_group
            or len(age_group) > MAX_AGE_GROUP_LEN
            or not age_group.isprintable()):  # blocks control chars / NULs
        return None
    hours = _to_number(parts[1], MAX_WEEKLY_HOURS)
    if hours is None:
        return None
    return age_group.title(), hours


def hours_average(hours_csv):
    """Average of comma-separated weekly hours (e.g. ``"20,25,30"``) or None."""
    if not _is_valid_text(hours_csv):
        return None
    values = []
    for token in hours_csv.split(","):   # always >= 1 token, so no ZeroDivision
        hours = _to_number(token, MAX_WEEKLY_HOURS)
        if hours is None:                # "", "1,,3", "abc", "-5", "nan" ...
            return None
        values.append(hours)
    # true division: the original used // and turned the mean of 1,2 into 1
    return round(sum(values) / len(values), 2)


def payable_fee(text):
    """``"<fee>|<discount>"`` -> fee with 18% tax minus discount, never < 0."""
    if not _is_valid_text(text):
        return None
    parts = text.split("|")
    if len(parts) != 2:
        return None
    fee = _to_number(parts[0], MAX_FEE)
    discount = _to_number(parts[1], MAX_FEE)   # negative discounts rejected
    if fee is None or discount is None:
        return None
    return round(max(fee * GST_MULTIPLIER - discount, 0.0), 2)


def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    if result is None:
        print("Invalid input: expected '<age group>:<hours 0-168>'.")
    else:
        print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    if result is None:
        print("Invalid input: expected comma-separated hours, each 0-168.")
    else:
        print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    if result is None:
        print("Invalid input: expected '<fee>|<discount>' with non-negative numbers.")
    else:
        print("Payable Fee:", result)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
