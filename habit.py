"""
habit.py – Habit Data Model
============================
This module defines the Habit class, the core data structure for the
Habit Tracker application. Each Habit object stores its name, periodicity
(daily or weekly), creation date, and a list of completed check-off dates.

The class provides methods to:
    - Check off a habit (record a completion timestamp).
    - Edit a habit's name and/or periodicity.
    - Convert the habit to a dictionary for JSON serialization.
"""

from datetime import datetime


class Habit:
    """
    Represents a single trackable habit.

    Attributes:
        name (str): The display name of the habit (e.g. 'Chewing Gum').
        periodicity (str): How often the habit should be completed —
                           either 'daily' or 'weekly'.
        creation_date (str): ISO-8601 timestamp of when the habit was created.
        completed_dates (list[str]): List of ISO-8601 timestamps recording
                                     each time the habit was checked off.
    """

    def __init__(self, name: str, periodicity: str):
        """
        Initialize a new Habit instance.

        Args:
            name (str): The name of the habit.
            periodicity (str): The habit's periodicity ('daily' or 'weekly').
        """
        self.name = name
        self.periodicity = periodicity
        # Record the exact moment the habit was created
        self.creation_date = datetime.now().isoformat()
        # Start with an empty completion history
        self.completed_dates = []

    # ------------------------------------------------------------------
    # Core Actions
    # ------------------------------------------------------------------

    def check_off(self):
        """
        Mark the habit as completed right now.

        Appends the current timestamp (ISO-8601 format) to the
        completed_dates list so streaks can be calculated later.
        """
        current_time = datetime.now().isoformat()
        self.completed_dates.append(current_time)

    def edit(self, new_name: str = None, new_periodicity: str = None):
        """
        Edit the habit's name and/or periodicity in place.

        Only the attributes for which a non-None value is provided will
        be updated. The completion history is preserved so that existing
        streak data is not lost.

        Args:
            new_name (str, optional): The new name for the habit.
            new_periodicity (str, optional): The new periodicity
                                             ('daily' or 'weekly').

        Raises:
            ValueError: If new_periodicity is not 'daily' or 'weekly'.
        """
        # Update the name only if a new one was provided
        if new_name is not None:
            self.name = new_name

        # Update the periodicity only if a new one was provided
        if new_periodicity is not None:
            # Validate that the periodicity is one of the allowed values
            if new_periodicity not in ("daily", "weekly"):
                raise ValueError(
                    f"Periodicity must be 'daily' or 'weekly', "
                    f"got '{new_periodicity}'."
                )
            self.periodicity = new_periodicity

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Convert the Habit instance to a plain dictionary.

        This is used by the db module to serialize habits into JSON.

        Returns:
            dict: A dictionary with keys 'name', 'periodicity',
                  'creation_date', and 'completed_dates'.
        """
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "creation_date": self.creation_date,
            "completed_dates": self.completed_dates,
        }

    # ------------------------------------------------------------------
    # String Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return (
            f"Habit(name={self.name}, period={self.periodicity}, "
            f"check_offs={len(self.completed_dates)})"
        )