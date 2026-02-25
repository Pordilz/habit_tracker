from datetime import datetime, timedelta


# --- Core Logic Functions ---

def get_all_habits(habits: list) -> list:
    """Returns a list of all habit names."""
    return [habit.name for habit in habits]


def get_habits_by_periodicity(habits: list, periodicity: str) -> list:
    """Filter habits by 'daily' or 'weekly'."""
    # Functional approach: using filter
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def calculate_longest_streak(habit) -> int:
    """
    Calculates the longest streak for a single habit.
    Logic:
    - Sort dates.
    - Loop through dates and check the gap between them.
    - Daily: Gap must be 1 day (or 0 if same day).
    - Weekly: Gap must be 1 week (based on ISO week number).
    """
    if not habit.completed_dates:
        return 0

    # Convert ISO strings to datetime objects and sort them
    dates = sorted([datetime.fromisoformat(d) for d in habit.completed_dates])

    # Remove time info for easier comparison (keep just the date)
    if habit.periodicity == 'daily':
        dates = [d.date() for d in dates]
        # Remove duplicates (checking off twice in one day shouldn't break logic)
        dates = sorted(list(set(dates)))
    else:
        # For weekly, we care about the Year and ISO Week number
        # Set format: (Year, WeekNum)
        dates = sorted(list(set([(d.isocalendar()[0], d.isocalendar()[1]) for d in dates])))

    streak = 1
    max_streak = 1

    for i in range(1, len(dates)):
        previous = dates[i - 1]
        current = dates[i]

        # Check gap based on periodicity
        is_consecutive = False

        if habit.periodicity == 'daily':
            # Difference should be exactly 1 day
            if (current - previous).days == 1:
                is_consecutive = True
        elif habit.periodicity == 'weekly':
            # Logic: If same year, diff is 1. If year changed, check boundary.
            # Simplified approach: Convert weeks to a continuous number
            prev_week_abs = previous[0] * 52 + previous[1]
            curr_week_abs = current[0] * 52 + current[1]
            if curr_week_abs - prev_week_abs == 1:
                is_consecutive = True

        if is_consecutive:
            streak += 1
        else:
            streak = 1  # Reset streak if gap is too large

        if streak > max_streak:
            max_streak = streak

    return max_streak


def get_longest_streak_for_all(habits: list) -> str:
    """
    Finds the habit with the longest streak among all habits.
    Returns a string describing the result.
    """
    # Functional approach: Map habits to tuples (habit, streak), then find max
    results = map(lambda h: (h.name, calculate_longest_streak(h)), habits)
    best_habit = max(results, key=lambda x: x[1])
    return f"The best habit is '{best_habit[0]}' with a streak of {best_habit[1]}!"