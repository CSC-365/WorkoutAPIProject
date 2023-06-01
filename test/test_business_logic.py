import pytest
from datetime import datetime, timedelta
from src.api.business_logic import calculate_projection
from sqlalchemy.engine.row import RowProxy
from src.api.business_logic import calculate_workout_plan


def test_calculate_projection_with_valid_logs(mocker):
    logs = [
        mocker.MagicMock(
            current_lbs=160, time_posted=datetime.now() - timedelta(days=2)),
        mocker.MagicMock(
            current_lbs=155, time_posted=datetime.now() - timedelta(days=1)),
    ]
    projection_date = (datetime.now() + timedelta(days=3)).date()

    result = calculate_projection(logs, projection_date)
    assert result == 140


def test_calculate_projection_with_insufficient_logs(mocker):
    logs = [
        mocker.MagicMock(
            current_lbs=160, time_posted=datetime.now() - timedelta(days=2)),
    ]
    projection_date = datetime.now() + timedelta(days=3)

    with pytest.raises(ValueError, match='user does not have enough logs to make a projection'):
        calculate_projection(logs, projection_date)


def test_calculate_projection_with_same_day_logs(mocker):
    now = datetime.now()
    logs = [
        mocker.MagicMock(current_lbs=160, time_posted=now),
        mocker.MagicMock(current_lbs=155, time_posted=now),
    ]
    projection_date = (now + timedelta(days=3)).date()

    with pytest.raises(ValueError, match="user's logs are on the same day, cannot make a projection"):
        calculate_projection(logs, projection_date)


def test_calculate_workout_plan_with_valid_user(mocker):
    user = mocker.MagicMock(starting_lbs=160,
                            birthday=datetime.now() - timedelta(days=365*25),
                            gender='M',
                            height_inches=70)
    target_weight = 150

    distance_ft, times_per_week = calculate_workout_plan(user, target_weight)
    assert distance_ft > 0
    assert times_per_week == 7


def test_calculate_workout_plan_with_nonexistent_user():
    user = None
    target_weight = 150

    with pytest.raises(ValueError, match="User not found"):
        calculate_workout_plan(user, target_weight)


def test_calculate_projection_with_past_projection_date(mocker):
    logs = [
        mocker.MagicMock(
            current_lbs=160, time_posted=datetime.now() - timedelta(days=2)),
        mocker.MagicMock(
            current_lbs=155, time_posted=datetime.now() - timedelta(days=1)),
    ]
    projection_date = (datetime.now() - timedelta(days=1)).date()

    with pytest.raises(ValueError):
        calculate_projection(logs, projection_date)


def test_calculate_workout_plan_with_higher_target_weight(mocker):
    user = mocker.MagicMock(starting_lbs=160,
                            birthday=datetime.now() - timedelta(days=365*25),
                            gender='M',
                            height_inches=70)
    target_weight = 170

    distance_ft, times_per_week = calculate_workout_plan(user, target_weight)
    assert distance_ft == 0.0
    assert times_per_week == 7


def test_calculate_workout_plan_with_same_target_weight(mocker):
    user = mocker.MagicMock(starting_lbs=160,
                            birthday=datetime.now() - timedelta(days=365*25),
                            gender='M',
                            height_inches=70)
    target_weight = 160

    distance_ft, times_per_week = calculate_workout_plan(user, target_weight)
    assert distance_ft == 0
    assert times_per_week == 7


def test_calculate_workout_plan_with_female_user(mocker):
    user = mocker.MagicMock(starting_lbs=160,
                            birthday=datetime.now() - timedelta(days=365*25),
                            gender='F',
                            height_inches=70)
    target_weight = 150

    distance_ft, times_per_week = calculate_workout_plan(user, target_weight)
    assert distance_ft > 0
    assert times_per_week == 7
