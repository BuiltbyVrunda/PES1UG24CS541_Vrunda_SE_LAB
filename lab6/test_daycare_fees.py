import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status

# Example test cases:
def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0

def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True

# Write the rest of the test cases so that the code is 90-100% covered.
