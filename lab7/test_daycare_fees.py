"""Lab 7 - Fuzz testing daycare_fees.py with Hypothesis.

Three layers of tests are used for every function:

1. No-crash fuzzing        - arbitrary text / None / other types must never raise.
2. Structured fuzzing      - inputs shaped like the real format ("a:b", "1,2,3",
                             "fee|discount") but filled with hostile values
                             (nan, inf, negatives, empty fields, huge numbers ...).
3. Property / oracle tests - when the input IS valid the answer must be correct,
                             and whenever an answer is returned it must be sane
                             (finite, non-negative, in range).

Invalid input is expected to be *rejected* by returning None, not by raising.

Run with:  pytest test_daycare_fees.py   (or: python -m pytest test_daycare_fees.py)
"""
import math

import pytest
from hypothesis import given, settings, strategies as st

from daycare_fees import hours_average, parse_enrolment, payable_fee

settings.register_profile("lab7", max_examples=500, deadline=None)
settings.load_profile("lab7")

MAX_WEEKLY_HOURS = 168  # hours in a week

# --------------------------------------------------------------------------
# Strategies
# --------------------------------------------------------------------------
# Anything a caller could possibly pass in, not only strings.
any_input = st.one_of(
    st.none(),
    st.text(),
    st.integers(),
    st.floats(),
    st.binary(),
    st.booleans(),
    st.lists(st.text()),
)

# Number-ish tokens that are valid, invalid or downright hostile.
hostile_number = st.one_of(
    st.integers().map(str),
    st.floats().map(repr),
    st.sampled_from(
        ["", " ", "nan", "NaN", "inf", "-inf", "Infinity", "1e999", "-0", "+5",
         "1_000", "0x10", "٣", "１２", "9" * 400, "1.", ".5", "5\n", "--1"]
    ),
    st.text(max_size=8),
)

enrolment_like = st.builds(lambda a, h: f"{a}:{h}", st.text(max_size=12), hostile_number)
csv_like = st.lists(hostile_number, max_size=8).map(",".join)
fee_like = st.builds(lambda f, d: f"{f}|{d}", hostile_number, hostile_number)


def _no_crash(func, value):
    """Call func(value); any exception is a test failure."""
    try:
        return func(value)
    except Exception as exc:  # noqa: BLE001 - we want to catch everything
        crash = exc
    pytest.fail(f"{func.__name__}({value!r}) crashed with {crash!r}")


# --------------------------------------------------------------------------
# 1. No-crash fuzzing (the three tests from the starter file)
# --------------------------------------------------------------------------
@given(st.text() | st.none())
def test_parse_enrolment_no_crash(s):
    _no_crash(parse_enrolment, s)


@given(st.text() | st.none())
def test_hours_average_no_crash(s):
    _no_crash(hours_average, s)


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    _no_crash(payable_fee, s)


# --------------------------------------------------------------------------
# 2. Wider fuzzing: wrong types and structured-but-hostile input
# --------------------------------------------------------------------------
@given(any_input)
def test_parse_enrolment_any_type_no_crash(x):
    _no_crash(parse_enrolment, x)


@given(any_input)
def test_hours_average_any_type_no_crash(x):
    _no_crash(hours_average, x)


@given(any_input)
def test_payable_fee_any_type_no_crash(x):
    _no_crash(payable_fee, x)


@given(enrolment_like)
def test_parse_enrolment_structured_postcondition(s):
    result = _no_crash(parse_enrolment, s)
    if result is not None:
        age_group, hours = result
        assert isinstance(age_group, str) and age_group.strip() == age_group != ""
        assert math.isfinite(hours) and 0 <= hours <= MAX_WEEKLY_HOURS


@given(csv_like)
def test_hours_average_structured_postcondition(s):
    result = _no_crash(hours_average, s)
    if result is not None:
        assert math.isfinite(result) and 0 <= result <= MAX_WEEKLY_HOURS


@given(fee_like)
def test_payable_fee_structured_postcondition(s):
    result = _no_crash(payable_fee, s)
    if result is not None:
        assert math.isfinite(result) and result >= 0


# --------------------------------------------------------------------------
# 3. Property / oracle tests on VALID input
# --------------------------------------------------------------------------
age_names = st.text(alphabet=st.characters(whitelist_categories=("L",)), min_size=1, max_size=20)


@given(age_names, st.integers(0, MAX_WEEKLY_HOURS), st.sampled_from(["", " ", "  "]))
def test_parse_enrolment_valid_roundtrip(name, hours, pad):
    result = parse_enrolment(f"{pad}{name}{pad}:{pad}{hours}{pad}")
    assert result == (name.title(), float(hours))


@given(st.lists(st.integers(0, MAX_WEEKLY_HOURS), min_size=1, max_size=50))
def test_hours_average_valid_is_true_mean(values):
    result = hours_average(",".join(map(str, values)))
    assert result is not None
    assert math.isclose(result, sum(values) / len(values), abs_tol=0.01)
    assert min(values) - 0.01 <= result <= max(values) + 0.01


@given(st.integers(0, 1_000_000), st.integers(0, 2_000_000))
def test_payable_fee_valid_matches_formula(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None
    assert math.isclose(result, max(fee * 1.18 - discount, 0), abs_tol=0.01)
    assert result >= 0


@given(st.integers(0, 1_000_000), st.integers(0, 1_000_000), st.integers(0, 1_000_000))
def test_payable_fee_bigger_discount_never_costs_more(fee, d1, d2):
    lo, hi = sorted((d1, d2))
    assert payable_fee(f"{fee}|{hi}") <= payable_fee(f"{fee}|{lo}")


# --------------------------------------------------------------------------
# Regression tests: every bug that fuzzing / exploration found
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "bad",
    [
        None, 123, b"toddler:5",       # not a string
        "", "toddler", ":", ":5",      # missing separator / empty name
        "toddler:", "toddler:abc",     # missing / non-numeric hours
        "a:b:c", "toddler:5:6",        # too many separators
        "toddler:nan", "toddler:inf",  # non-finite hours
        "toddler:-3",                  # negative hours
        "toddler:169", "toddler:1e3",  # more hours than a week has
        "toddler:1_0",                 # Python-only number syntax
        "tod\x00dler:5",               # control character in name
    ],
)
def test_parse_enrolment_rejects_bad_input(bad):
    assert parse_enrolment(bad) is None


@pytest.mark.parametrize(
    "bad",
    [None, 5, "", ",", "1,,3", "1,2,", ",1", "one,two", "-5,5", "nan,1",
     "inf", "20,x", "1;2", "170,10", "1_0,2"],
)
def test_hours_average_rejects_bad_input(bad):
    assert hours_average(bad) is None


@pytest.mark.parametrize(
    "bad",
    [None, 5, "", "3000", "3000|", "|250", "abc|1", "1|abc", "1|2|3",
     "nan|1", "1|nan", "inf|1", "1|inf", "-100|5", "100|-50", "1e999|1"],
)
def test_payable_fee_rejects_bad_input(bad):
    assert payable_fee(bad) is None


def test_parse_enrolment_example_from_prompt():
    assert parse_enrolment("toddler:25") == ("Toddler", 25.0)
    assert parse_enrolment("  pre-school : 12.5 ") == ("Pre-School", 12.5)


def test_hours_average_does_not_truncate():
    # original used // so "1,2" gave 1 instead of 1.5
    assert hours_average("1,2") == 1.5
    assert hours_average("20,25,30") == 25.0
    assert hours_average("20.5,21") == 20.75


def test_payable_fee_negative_discount_cannot_raise_the_bill():
    # original accepted "3000|-9999" and charged 13539.0
    assert payable_fee("3000|-9999") is None


def test_payable_fee_known_values():
    assert payable_fee("3000|250") == 3290.0
    assert payable_fee("100|1000") == 0.0   # discount larger than bill -> free, never negative
