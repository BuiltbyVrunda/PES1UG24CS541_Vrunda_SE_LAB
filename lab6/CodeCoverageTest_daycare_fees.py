import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


# ---------- extra_hours_fee ----------

def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0

def test_unknown_age_group_raises():
    with pytest.raises(ValueError):
        extra_hours_fee("teen", 10, False)

def test_negative_hours_raises():
    with pytest.raises(ValueError):
        extra_hours_fee("toddler", -1, False)

def test_toddler_with_sibling_gets_extra_included_hours():
    # included = 25 + 5 = 30, extra = 5, rate = 9
    assert extra_hours_fee("toddler", 35, True) == 45

def test_infant_small_extra():
    # included = 20, extra = 5, rate = 14
    assert extra_hours_fee("infant", 25, False) == 70

def test_infant_large_extra():
    # included = 20, extra = 25, rate = 14 + 5 + 3 = 22
    assert extra_hours_fee("infant", 45, False) == 550


# ---------- enrolment_allowed ----------

def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True

def test_enrolment_immunisation_pending_old_enough():
    assert enrolment_allowed(12, 0, True) is True

def test_enrolment_too_young():
    assert enrolment_allowed(5, 3, False) is False


# ---------- pickup_status ----------

def test_pickup_on_time_aftercare():
    # cutoff = 20
    assert pickup_status(25, True, False) == "on_time"

def test_pickup_late_on_friday():
    # cutoff = 10 + 10 = 20, late if 5 <= minutes < 20
    assert pickup_status(10, False, True) == "late"

def test_pickup_overdue():
    # cutoff = 10, overdue if minutes < -5
    assert pickup_status(-10, False, False) == "overdue"