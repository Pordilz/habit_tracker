import json
import os
from habit import Habit

FILE_NAME = "habits.json"


def get_db_path():
    """Returns the absolute path to the database file."""
    # This ensures the file is created in the same directory as the script
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_NAME)


def save_data(habits: list):
    """Saves the list of Habit objects to the JSON file."""
    # Convert list of Objects -> List of Dictionaries
    data = [h.to_dict() for h in habits]

    with open(get_db_path(), "w") as f:
        json.dump(data, f, indent=4)


def load_data() -> list:
    """
    Loads data from JSON and returns a list of Habit objects.
    If file doesn't exist, returns an empty list.
    """
    if not os.path.exists(get_db_path()):
        return []

    try:
        with open(get_db_path(), "r") as f:
            data = json.load(f)

        habits = []
        for entry in data:
            # Recreate the Habit object from the dictionary
            h = Habit(entry["name"], entry["periodicity"])
            h.creation_date = entry["creation_date"]
            h.completed_dates = entry["completed_dates"]
            habits.append(h)
        return habits
    except (json.JSONDecodeError, FileNotFoundError):
        return []