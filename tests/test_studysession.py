import datetime
import pytest

from models.study_session import StudySession

TODAY = datetime.date(2026, 11, 22)


def make_session(module_code="CSC2A", duration=2, date=TODAY):
    return StudySession(module_code, duration, date)


# --- duration: valid ---

def test_valid_duration_is_stored():
    assert make_session(duration=2.5).duration == 2.5


@pytest.mark.parametrize("boundary", [0.5, 24])
def test_boundary_durations_accepted(boundary):
    assert make_session(duration=boundary).duration == boundary


# --- duration: invalid at construction ---

@pytest.mark.parametrize("bad_duration", [0, -1, 24.1, 25])
def test_invalid_duration_rejected_at_construction(bad_duration):
    with pytest.raises(ValueError):
        make_session(duration=bad_duration)


# --- duration: changing it later (needs the property setter) ---

def test_valid_duration_can_be_assigned_later():
    s = make_session(duration=2)
    s.duration = 5
    assert s.duration == 5


@pytest.mark.parametrize("bad_duration", [0, -3, 25])
def test_invalid_duration_rejected_when_assigned_later(bad_duration):
    s = make_session(duration=2)
    with pytest.raises(ValueError):
        s.duration = bad_duration
    assert s.duration == 2  # the old value must survive


# --- module_code ---

def test_module_code_is_stored_as_given():
    assert make_session(module_code="CSC2A").module_code == "CSC2A"


@pytest.mark.parametrize("bad_code", [12345, None, 3.5])
def test_non_string_module_code_rejected(bad_code):
    with pytest.raises(ValueError):
        make_session(module_code=bad_code)


def test_non_string_module_code_rejected_when_assigned_later():
    s = make_session()
    with pytest.raises(ValueError):
        s.module_code = 12345
    assert s.module_code == "CSC2A"


# --- date ---

def test_date_is_stored():
    assert make_session(date=TODAY).date == TODAY


@pytest.mark.parametrize("bad_date", ["2026-11-22", 20261122, None])
def test_non_date_rejected(bad_date):
    with pytest.raises(ValueError):
        make_session(date=bad_date)


def test_datetime_rejected():
    # sessions are tracked by day only, so a full datetime is not allowed
    now = datetime.datetime(2026, 11, 22, 14, 30)
    with pytest.raises(ValueError):
        make_session(date=now)


def test_datetime_rejected_when_assigned_later():
    s = make_session(date=TODAY)
    with pytest.raises(ValueError):
        s.date = datetime.datetime(2026, 11, 22, 14, 30)
    assert s.date == TODAY  # the old value must survive