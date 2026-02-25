"""
test_project.py – Comprehensive Test Suite for the Habit Tracker
=================================================================
This module contains unit tests for every component of the Habit Tracker
application. Tests are organized into logical groups:

    1. Habit CRUD       – Creation, editing (name / periodicity / both),
                          and deletion of Habit objects.
    2. Check-off        – Verifying that check_off() records valid dates.
    3. Streak (Daily)   – Streak calculations using a 4-week daily fixture.
    4. Streak (Weekly)  – Streak calculations using a 4-week weekly fixture.
    5. Analytics Module  – Every public function in analytics.py.

Fixtures load exactly 4 weeks of predefined time-series
data so that streak calculations are fully reproducible.

Run with:
    python -m pytest test_project.py -v
"""

import pytest
from datetime import datetime, timedelta

from habit import Habit
import analytics


# ======================================================================
# Fixtures – Predefined 4-Week Time-Series Data
# ======================================================================

@pytest.fixture
def daily_habit_4_weeks():
    """
    Create a daily habit with exactly 28 consecutive days of check-offs.

    The fixture uses a fixed start date (2025-01-06) and creates one
    ISO-8601 timestamp per day for 28 days (4 full weeks), producing a
    completely continuous streak of 28.

    Returns:
        Habit: A daily habit with 28 consecutive completed_dates entries.
    """
    habit = Habit("Morning Jog", "daily")

    # Use a fixed, deterministic start date for reproducibility
    start_date = datetime(2025, 1, 6, 8, 0, 0)  # Monday, 6 Jan 2025
    habit.creation_date = start_date.isoformat()

    # Create exactly 28 consecutive daily check-offs
    for day in range(28):
        check_date = start_date + timedelta(days=day)
        habit.completed_dates.append(check_date.isoformat())

    return habit


@pytest.fixture
def weekly_habit_4_weeks():
    """
    Create a weekly habit with exactly 4 consecutive weekly check-offs.

    The fixture uses the same fixed start date and creates one
    check-off per week for 4 weeks, producing a continuous weekly
    streak of 4.

    Returns:
        Habit: A weekly habit with 4 consecutive completed_dates entries.
    """
    habit = Habit("Weekly Review", "weekly")

    # Use a fixed start date aligned to a Monday
    start_date = datetime(2025, 1, 6, 10, 0, 0)  # Monday, 6 Jan 2025
    habit.creation_date = start_date.isoformat()

    # Create exactly 4 consecutive weekly check-offs
    for week in range(4):
        check_date = start_date + timedelta(weeks=week)
        habit.completed_dates.append(check_date.isoformat())

    return habit


@pytest.fixture
def sample_habits():
    """
    Create a mixed list of habits for testing analytics functions.

    Contains:
        - 2 daily habits (one with a 5-day streak, one with a 3-day streak)
        - 1 weekly habit (with a 3-week streak)

    Returns:
        list[Habit]: A list of three Habit objects with preset histories.
    """
    # --- Daily habit 1: 5 consecutive days ---
    h1 = Habit("Read Books", "daily")
    base = datetime(2025, 2, 1, 9, 0, 0)
    h1.creation_date = base.isoformat()
    for day in range(5):
        h1.completed_dates.append(
            (base + timedelta(days=day)).isoformat()
        )

    # --- Daily habit 2: 3 consecutive days ---
    h2 = Habit("Meditate", "daily")
    h2.creation_date = base.isoformat()
    for day in range(3):
        h2.completed_dates.append(
            (base + timedelta(days=day)).isoformat()
        )

    # --- Weekly habit: 3 consecutive weeks ---
    h3 = Habit("Meal Prep", "weekly")
    h3.creation_date = base.isoformat()
    for week in range(3):
        h3.completed_dates.append(
            (base + timedelta(weeks=week)).isoformat()
        )

    return [h1, h2, h3]


# ======================================================================
# 1. Habit CRUD Tests
# ======================================================================

class TestHabitCRUD:
    """Tests for creating, editing, and deleting Habit objects."""

    def test_habit_creation(self):
        """Verify that a new habit is initialized with correct defaults."""
        habit = Habit("Exercise", "daily")

        assert habit.name == "Exercise"
        assert habit.periodicity == "daily"
        assert habit.completed_dates == []
        # creation_date should be a valid ISO string
        datetime.fromisoformat(habit.creation_date)

    def test_habit_creation_weekly(self):
        """Verify weekly habit creation stores the correct periodicity."""
        habit = Habit("Grocery Shopping", "weekly")

        assert habit.name == "Grocery Shopping"
        assert habit.periodicity == "weekly"

    def test_habit_edit_name(self):
        """Verify that editing the name updates only the name."""
        habit = Habit("Old Name", "daily")
        original_periodicity = habit.periodicity

        habit.edit(new_name="New Name")

        assert habit.name == "New Name"
        assert habit.periodicity == original_periodicity  # Unchanged

    def test_habit_edit_periodicity(self):
        """Verify that editing the periodicity updates only the periodicity."""
        habit = Habit("Workout", "daily")
        original_name = habit.name

        habit.edit(new_periodicity="weekly")

        assert habit.periodicity == "weekly"
        assert habit.name == original_name  # Unchanged

    def test_habit_edit_both(self):
        """Verify that editing both name and periodicity at once works."""
        habit = Habit("Old Habit", "daily")

        habit.edit(new_name="New Habit", new_periodicity="weekly")

        assert habit.name == "New Habit"
        assert habit.periodicity == "weekly"

    def test_habit_edit_preserves_history(self):
        """Verify that editing does NOT erase existing check-off history."""
        habit = Habit("Study", "daily")
        habit.check_off()
        habit.check_off()
        original_count = len(habit.completed_dates)

        habit.edit(new_name="Deep Study")

        assert len(habit.completed_dates) == original_count

    def test_habit_edit_invalid_periodicity(self):
        """Verify that an invalid periodicity raises ValueError."""
        habit = Habit("Test", "daily")

        with pytest.raises(ValueError):
            habit.edit(new_periodicity="monthly")

    def test_habit_deletion(self):
        """Verify that deleting a habit removes it from the list."""
        h1 = Habit("Keep", "daily")
        h2 = Habit("Remove", "weekly")
        habits = [h1, h2]

        # Perform deletion (same logic used in main.py)
        habits = [h for h in habits if h.name != "Remove"]

        assert len(habits) == 1
        assert habits[0].name == "Keep"


# ======================================================================
# 2. Check-off Tests
# ======================================================================

class TestCheckOff:
    """Tests for the habit check-off functionality."""

    def test_check_off_adds_date(self):
        """Verify that check_off() adds exactly one entry."""
        habit = Habit("Water Plants", "daily")

        habit.check_off()

        assert len(habit.completed_dates) == 1

    def test_check_off_multiple(self):
        """Verify that multiple check-offs accumulate correctly."""
        habit = Habit("Stretching", "daily")

        habit.check_off()
        habit.check_off()
        habit.check_off()

        assert len(habit.completed_dates) == 3

    def test_check_off_valid_iso_format(self):
        """Verify that check_off() stores a valid ISO-8601 timestamp."""
        habit = Habit("Journal", "daily")
        habit.check_off()

        # This will raise ValueError if the format is invalid
        parsed = datetime.fromisoformat(habit.completed_dates[0])
        assert isinstance(parsed, datetime)


# ======================================================================
# 3. Streak Calculation Tests – Daily Habits
# ======================================================================

class TestStreakDaily:
    """Tests for streak calculation with daily periodicity."""

    def test_daily_streak_full_4_weeks(self, daily_habit_4_weeks):
        """
        A habit with 28 consecutive daily check-offs should have
        a longest streak of exactly 28.
        """
        streak = analytics.calculate_longest_streak(daily_habit_4_weeks)
        assert streak == 28

    def test_daily_streak_with_gap(self):
        """
        Introduce a gap in the middle of a daily series.

        Pattern: 5 consecutive days, then a 1-day gap, then 3 more days.
        Expected longest streak: 5 (the first block).
        """
        habit = Habit("Running", "daily")
        base = datetime(2025, 3, 1, 7, 0, 0)

        # Days 1–5 (consecutive)
        for day in range(5):
            habit.completed_dates.append(
                (base + timedelta(days=day)).isoformat()
            )

        # Day 6 is SKIPPED (gap)

        # Days 7–9 (consecutive, but a separate block of 3)
        for day in range(6, 9):
            habit.completed_dates.append(
                (base + timedelta(days=day)).isoformat()
            )

        streak = analytics.calculate_longest_streak(habit)
        assert streak == 5

    def test_daily_streak_empty(self):
        """A habit with no check-offs should have a streak of 0."""
        habit = Habit("Empty Daily", "daily")

        streak = analytics.calculate_longest_streak(habit)
        assert streak == 0

    def test_daily_streak_single_day(self):
        """A habit with exactly one check-off should have a streak of 1."""
        habit = Habit("One Day", "daily")
        habit.completed_dates.append(datetime(2025, 5, 1, 8, 0).isoformat())

        streak = analytics.calculate_longest_streak(habit)
        assert streak == 1

    def test_daily_streak_duplicate_same_day(self):
        """
        Checking off twice on the same day should NOT inflate the streak.

        Two check-offs on Day 1 + one on Day 2 = streak of 2 (not 3).
        """
        habit = Habit("Duplicate Test", "daily")
        base = datetime(2025, 4, 1, 8, 0, 0)

        # Two check-offs on day 1
        habit.completed_dates.append(base.isoformat())
        habit.completed_dates.append(
            (base + timedelta(hours=6)).isoformat()
        )
        # One check-off on day 2
        habit.completed_dates.append(
            (base + timedelta(days=1)).isoformat()
        )

        streak = analytics.calculate_longest_streak(habit)
        assert streak == 2


# ======================================================================
# 4. Streak Calculation Tests – Weekly Habits
# ======================================================================

class TestStreakWeekly:
    """Tests for streak calculation with weekly periodicity."""

    def test_weekly_streak_full_4_weeks(self, weekly_habit_4_weeks):
        """
        A habit with 4 consecutive weekly check-offs should have
        a longest streak of exactly 4.
        """
        streak = analytics.calculate_longest_streak(weekly_habit_4_weeks)
        assert streak == 4

    def test_weekly_streak_with_gap(self):
        """
        Introduce a gap in the weekly series.

        Pattern: Week 1, Week 2, (skip Week 3), Week 4.
        Expected longest streak: 2 (Weeks 1 and 2).
        """
        habit = Habit("Laundry", "weekly")
        base = datetime(2025, 1, 6, 10, 0, 0)

        habit.completed_dates.append(base.isoformat())                          # Week 1
        habit.completed_dates.append((base + timedelta(weeks=1)).isoformat())   # Week 2
        # Week 3 is SKIPPED
        habit.completed_dates.append((base + timedelta(weeks=3)).isoformat())   # Week 4

        streak = analytics.calculate_longest_streak(habit)
        assert streak == 2

    def test_weekly_streak_empty(self):
        """A weekly habit with no check-offs should have a streak of 0."""
        habit = Habit("Empty Weekly", "weekly")

        streak = analytics.calculate_longest_streak(habit)
        assert streak == 0

    def test_weekly_streak_single_week(self):
        """A weekly habit with one check-off should have a streak of 1."""
        habit = Habit("One Week", "weekly")
        habit.completed_dates.append(datetime(2025, 3, 3, 9, 0).isoformat())

        streak = analytics.calculate_longest_streak(habit)
        assert streak == 1


# ======================================================================
# 5. Analytics Module Tests
# ======================================================================

class TestAnalytics:
    """Tests for every public function in the analytics module."""

    def test_get_all_habits(self, sample_habits):
        """Verify get_all_habits returns a list of all habit names."""
        names = analytics.get_all_habits(sample_habits)

        assert isinstance(names, list)
        assert len(names) == 3
        assert "Read Books" in names
        assert "Meditate" in names
        assert "Meal Prep" in names

    def test_get_all_habits_empty(self):
        """Verify get_all_habits returns an empty list when given no habits."""
        names = analytics.get_all_habits([])
        assert names == []

    def test_get_habits_by_periodicity_daily(self, sample_habits):
        """Verify filtering returns only daily habits."""
        daily = analytics.get_habits_by_periodicity(sample_habits, "daily")

        assert len(daily) == 2
        for h in daily:
            assert h.periodicity == "daily"

    def test_get_habits_by_periodicity_weekly(self, sample_habits):
        """Verify filtering returns only weekly habits."""
        weekly = analytics.get_habits_by_periodicity(sample_habits, "weekly")

        assert len(weekly) == 1
        assert weekly[0].name == "Meal Prep"

    def test_get_habits_by_periodicity_none(self, sample_habits):
        """Verify filtering with non-matching periodicity returns empty."""
        result = analytics.get_habits_by_periodicity(sample_habits, "monthly")
        assert result == []

    def test_calculate_longest_streak_specific(self, sample_habits):
        """Verify streak calculation for individual habits in the fixture."""
        # "Read Books" has 5 consecutive daily check-offs
        read_books = sample_habits[0]
        assert analytics.calculate_longest_streak(read_books) == 5

        # "Meditate" has 3 consecutive daily check-offs
        meditate = sample_habits[1]
        assert analytics.calculate_longest_streak(meditate) == 3

        # "Meal Prep" has 3 consecutive weekly check-offs
        meal_prep = sample_habits[2]
        assert analytics.calculate_longest_streak(meal_prep) == 3

    def test_get_longest_streak_for_all(self, sample_habits):
        """
        Verify that get_longest_streak_for_all identifies 'Read Books'
        as the habit with the longest streak (5 consecutive days).
        """
        result = analytics.get_longest_streak_for_all(sample_habits)

        # The function returns a descriptive string
        assert isinstance(result, str)
        assert "Read Books" in result
        assert "5" in result

    def test_to_dict_serialization(self):
        """Verify to_dict() produces a correct dictionary representation."""
        habit = Habit("Serialize Me", "daily")
        habit.check_off()

        data = habit.to_dict()

        assert data["name"] == "Serialize Me"
        assert data["periodicity"] == "daily"
        assert "creation_date" in data
        assert len(data["completed_dates"]) == 1