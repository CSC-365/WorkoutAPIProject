from datetime import date
import datetime
from typing import List, Tuple
import pytest
from sqlalchemy.engine.row import Row


def calculate_projection(logs: List[Row], projection_date: date) -> int:
    if len(logs) == 0 or len(logs) == 1:  # meaning they have no logs
        raise ValueError("user does not have enough logs to make a projection")

    # check for projection date in the past
    if projection_date < date.today():
        raise ValueError(
            "projection date is in the past, cannot make a projection")

    # x-axis difference in days
    x = (logs[-1].time_posted.date() - logs[0].time_posted.date()).days
    if x == 0:
        raise ValueError(
            "user's logs are on the same day, cannot make a projection")

    # y-axis difference in lbs
    y = logs[-1].current_lbs - logs[0].current_lbs

    # slope
    m = round(y / x, 2)

    days = (projection_date - date.today()).days
    projected_loss = int(round(logs[-1].current_lbs + (days * m), 0))

    return projected_loss


def calculate_workout_plan(user: Row, target_weight: int) -> Tuple[float, int]:
    if user is None:
        raise ValueError("User not found")

    # Calculate basal metabolic rate (BMR)
    current_date = date.today()
    age = current_date.year - user.birthday.year
    bmr = 10 * user.starting_lbs + 6.25 * user.height_inches - 5 * age + \
        5 if user.gender == 'M' else 10 * user.starting_lbs + \
        6.25 * user.height_inches - 5 * age - 161

    # Calculate total daily energy expenditure (TDEE)
    tdee = bmr * 1.55

    # Calculate daily caloric deficit
    daily_caloric_deficit = 500 * (user.starting_lbs - target_weight)

    # Calculate feet per week needed to lose weight
    miles_per_week = daily_caloric_deficit / 100
    feet_per_week = miles_per_week * 5280

    # check to make sure value isn't negative
    if feet_per_week < 0:
        feet_per_week = 0

    return feet_per_week / 7, 7


def test_calculate_projection_with_future_logs(mocker):
    logs = [
        mocker.MagicMock(
            current_lbs=160, time_posted=datetime.now() + timedelta(days=1)),
        mocker.MagicMock(
            current_lbs=155, time_posted=datetime.now() + timedelta(days=2)),
    ]
    projection_date = (datetime.now() + timedelta(days=3)).date()

    with pytest.raises(ValueError):
        calculate_projection(logs, projection_date)


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
    assert distance_ft > 0
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
