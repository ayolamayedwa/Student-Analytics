import datetime
import pytest

from models.assessment import Assessment
from models.module import Module

DUE = datetime.datetime(2026, 12, 1, 9, 0)


def make_module(code="CSC2A", name="Algorithms", credits=16):
    return Module(code, name, credits)


def make_assessment(weight=0.3, mark=None):
    return Assessment("Test", weight, mark, DUE)


# --- calculate_average ---

def test_average_is_none_with_no_assessments():
    assert make_module().calculate_average() is None


def test_average_is_none_when_nothing_is_marked():
    m = make_module()
    m.add_assessment(make_assessment(0.5, None))
    m.add_assessment(make_assessment(0.5, None))
    assert m.calculate_average() is None


def test_average_of_single_mark():
    m = make_module()
    m.add_assessment(make_assessment(0.5, 80))
    assert m.calculate_average() == pytest.approx(80)


def test_average_is_weighted():
    m = make_module()
    m.add_assessment(make_assessment(0.3, 70))
    m.add_assessment(make_assessment(0.3, 80))
    assert m.calculate_average() == pytest.approx(75)


def test_average_ignores_unmarked_and_renormalises():
    # 0.4 of the weight is still unmarked; the average covers only what's marked
    m = make_module()
    m.add_assessment(make_assessment(0.3, 70))
    m.add_assessment(make_assessment(0.3, 80))
    m.add_assessment(make_assessment(0.4, None))
    assert m.calculate_average() == pytest.approx(75)


def test_genuine_zero_mark_is_not_treated_as_missing():
    m = make_module()
    m.add_assessment(make_assessment(0.5, 0))
    assert m.calculate_average() == 0          # 0, not None

    m.add_assessment(make_assessment(0.5, 100))
    assert m.calculate_average() == pytest.approx(50)


# --- add_assessment: weight limit ---

def test_add_assessment_accepts_when_under_limit():
    m = make_module()
    a = make_assessment(0.4)
    assert m.add_assessment(a) is True
    assert a in m.assessments


def test_add_assessment_rejects_when_total_would_exceed_one():
    m = make_module()
    m.add_assessment(make_assessment(0.4))
    m.add_assessment(make_assessment(0.3))
    assert m.add_assessment(make_assessment(0.4)) is False
    assert len(m.assessments) == 2             # nothing was added


def test_add_assessment_accepts_total_of_exactly_one():
    m = make_module()
    assert m.add_assessment(make_assessment(0.4)) is True
    assert m.add_assessment(make_assessment(0.3)) is True
    assert m.add_assessment(make_assessment(0.3)) is True
    assert len(m.assessments) == 3


# PROBE: floating-point. 0.1 + 0.2 isn't exactly 0.3 in binary, so a total that
# is mathematically 1 can drift just above it. If this fails, you've found the
# tolerance problem and need to compare with a small epsilon instead of `> 1`.
def test_probe_four_weights_summing_to_one_are_all_accepted():
    m = make_module()
    for w in (0.1, 0.2, 0.3, 0.4):
        assert m.add_assessment(make_assessment(w)) is True


# --- remove_assessment ---

def test_remove_assessment_removes_it():
    m = make_module()
    a = make_assessment(0.4)
    m.add_assessment(a)
    m.remove_assessment(a)
    assert a not in m.assessments


def test_remove_assessment_not_in_module_changes_nothing():
    m = make_module()
    m.add_assessment(make_assessment(0.4))
    m.remove_assessment(make_assessment(0.4))   # a different object
    assert len(m.assessments) == 1


# --- is_fully_marked ---

def test_fully_marked_true_when_every_assessment_has_a_mark():
    m = make_module()
    m.add_assessment(make_assessment(0.5, 60))
    m.add_assessment(make_assessment(0.5, 70))
    assert m.is_fully_marked() is True


def test_fully_marked_false_when_one_mark_is_missing():
    m = make_module()
    m.add_assessment(make_assessment(0.5, 60))
    m.add_assessment(make_assessment(0.5, None))
    assert m.is_fully_marked() is False


def test_fully_marked_counts_a_zero_mark_as_marked():
    m = make_module()
    m.add_assessment(make_assessment(0.5, 0))
    m.add_assessment(make_assessment(0.5, 70))
    assert m.is_fully_marked() is True


def test_fully_marked_reflects_later_changes():
    # proves the answer is computed on demand and can't go stale
    m = make_module()
    a = make_assessment(0.5, None)
    m.add_assessment(a)
    assert m.is_fully_marked() is False
    a.mark = 55
    assert m.is_fully_marked() is True
    a.mark = None
    assert m.is_fully_marked() is False


# DEPENDS ON YOUR DECISION: this assumes an empty module is NOT fully marked.
# If you decided the opposite, flip the expected value.
def test_fully_marked_for_empty_module():
    assert make_module().is_fully_marked() is False


# --- update_assessment_mark (assumes the version that checks membership) ---

def test_update_mark_on_member_assessment():
    m = make_module()
    a = make_assessment(0.5, None)
    m.add_assessment(a)
    assert m.update_assessment_mark(a, 65) is True
    assert a.mark == 65


def test_update_mark_on_assessment_not_in_module_returns_false():
    m = make_module()
    outsider = make_assessment(0.5, None)
    assert m.update_assessment_mark(outsider, 65) is False
    assert outsider.mark is None


def test_update_mark_rejects_out_of_range_value():
    # relies on the @property setter on Assessment.mark
    m = make_module()
    a = make_assessment(0.5, 60)
    m.add_assessment(a)
    with pytest.raises(ValueError):
        m.update_assessment_mark(a, 250)
    assert a.mark == 60


# --- credits getter ---

def test_get_module_credits():
    assert make_module(credits=16).get_module_credits() == 16


# --- PENDING: these fail until Module.code / Module.credits are properties ---

@pytest.mark.parametrize("bad_credits", [0, -16])
def test_invalid_credits_rejected_at_construction(bad_credits):
    with pytest.raises(ValueError):
        make_module(credits=bad_credits)


def test_invalid_credits_rejected_when_assigned_later():
    m = make_module(credits=16)
    with pytest.raises(ValueError):
        m.credits = -5
    assert m.credits == 16


@pytest.mark.parametrize("bad_code", [12345, None])
def test_non_string_code_rejected(bad_code):
    with pytest.raises(ValueError):
        make_module(code=bad_code)