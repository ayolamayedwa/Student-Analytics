import datetime
import pytest

from models.assessment import Assessment

DUE = datetime.datetime(2026, 12, 1, 9, 0)


def make_assessment(weight=0.3, mark=None):
    return Assessment("Test 1", weight, mark, DUE)


#  test area: valid input

def test_valid_mark_is_stored():
    assert make_assessment(mark=70).mark == 70


def test_none_mark_is_accepted():
    assert make_assessment(mark=None).mark is None


def test_zero_mark_stays_zero():
    # a real 0 must not be confused with "no mark yet"
    a = make_assessment(mark=0)
    assert a.mark == 0
    assert a.mark is not None


def test_boundary_marks_are_accepted():
    assert make_assessment(mark=100).mark == 100


# --- construction: invalid input ---

@pytest.mark.parametrize("bad_mark", [-1, 101, 250])
def test_out_of_range_mark_rejected_at_construction(bad_mark):
    with pytest.raises(ValueError):
        make_assessment(mark=bad_mark)


@pytest.mark.parametrize("bad_weight", [0, -0.1, 1.5])
def test_invalid_weight_rejected_at_construction(bad_weight):
    with pytest.raises(ValueError):
        make_assessment(weight=bad_weight)


# --- changing the mark after construction (needs the @property setter) ---

def test_valid_mark_can_be_assigned_later():
    a = make_assessment()
    a.mark = 85
    assert a.mark == 85


def test_out_of_range_mark_rejected_when_assigned_later():
    a = make_assessment(mark=60)
    with pytest.raises(ValueError):
        a.mark = 250
    assert a.mark == 60  # the bad value must not have been stored