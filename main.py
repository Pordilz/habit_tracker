"""
main.py – CLI Interface for the Habit Tracker
===============================================
This module provides the command-line interface (CLI) for the Habit Tracker
application. It uses the `questionary` library to present interactive menus
that let users create, edit, delete, check off, and analyze their habits.

On first run, the application automatically loads 5 predefined habits
with 4 weeks of sample completion history so users can immediately
explore the analytics features.

Usage:
    python main.py
"""

import questionary
from datetime import datetime, timedelta
import random
from habit import Habit
import analytics
import db


# ======================================================================
# Predefined Data Initialization
# ======================================================================

def initialize_sample_data():
    """
    Create 5 predefined habits with 4 weeks of sample check-off history.

    This function is called automatically on the first run (when no
    habits.json file exists). It creates realistic time-series data
    so that analytics and streak calculations can be demonstrated
    immediately.

    Habits created:
        - Code Commits (weekly)
        - Job Application Sprint (weekly)
        - Scent of the Day (daily)
        - Anime/Gaming Break (daily)
        - Chewing Gum (daily)

    Returns:
        list[Habit]: The list of newly created Habit objects with
                     pre-populated completion histories.
    """
    print("✨ First run detected: Loading 4 weeks of sample data...")

    habits = []

    # Define the 5 predefined habits with their periodicities
    definitions = [
        ("Code Commits", "weekly"),
        ("Job Application Sprint", "weekly"),
        ("Scent of the Day", "daily"),
        ("Anime/Gaming Break", "daily"),
        ("Chewing Gum", "daily"),
    ]

    for name, period in definitions:
        h = Habit(name, period)

        # Set the creation date to exactly 4 weeks ago
        start_date = datetime.now() - timedelta(weeks=4)
        h.creation_date = start_date.isoformat()

        # Create sample completion data based on periodicity
        if period == "daily":
            # Realistic pattern: ~80% daily completion rate
            for i in range(28):
                if random.random() > 0.2:
                    date = start_date + timedelta(days=i)
                    h.completed_dates.append(date.isoformat())
        else:
            # Weekly habits: complete once per week for all 4 weeks
            for i in range(4):
                date = start_date + timedelta(weeks=i)
                h.completed_dates.append(date.isoformat())

        habits.append(h)

    # Save the initial data to disk
    db.save_data(habits)
    return habits


# ======================================================================
# Main CLI Loop
# ======================================================================

def cli():
    """
    Run the interactive command-line interface.

    Presents a main menu with the following options:
        1. Check-off a habit   – Record today's completion.
        2. Analyze habits      – View reports and streak statistics.
        3. Create a new habit  – Add a habit with a name and periodicity.
        4. Edit a habit        – Change a habit's name or periodicity.
        5. Delete a habit      – Remove a habit permanently.
        6. Exit                – Quit the application.
    """
    # Load existing habits from the JSON database
    habits = db.load_data()

    # If no habits exist, initialize the predefined sample data
    if not habits:
        habits = initialize_sample_data()

    print(f"👋 Welcome! Loaded {len(habits)} habits.")

    # Main application loop — keeps running until the user selects "Exit"
    while True:
        # Display the main menu using questionary's interactive select
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Check-off a habit",
                "Analyze habits",
                "Create a new habit",
                "Edit a habit",
                "Delete a habit",
                "Exit",
            ],
        ).ask()

        # ---- EXIT ----
        if choice == "Exit":
            print("Bye! 👋")
            break

        # ---- CHECK OFF ----
        elif choice == "Check-off a habit":
            habit_names = analytics.get_all_habits(habits)

            # Guard clause: cannot check off if there are no habits
            if not habit_names:
                print("No habits found!")
                continue

            # Let the user pick which habit to check off
            selected = questionary.select(
                "Select habit:", choices=habit_names
            ).ask()

            # Find the matching Habit object and record the check-off
            for h in habits:
                if h.name == selected:
                    h.check_off()
                    print(f"✅ Checked off '{h.name}'!")
                    db.save_data(habits)  # Persist the change immediately
                    break

        # ---- ANALYZE ----
        elif choice == "Analyze habits":
            # Show a sub-menu with the available analytics reports
            sub_choice = questionary.select(
                "Which report?",
                choices=[
                    "List all habits",
                    "List by periodicity",
                    "Longest streak for a specific habit",
                    "Longest streak across ALL habits",
                ],
            ).ask()

            if sub_choice == "List all habits":
                # Display every habit name
                print("\n📋 All Habits:")
                for name in analytics.get_all_habits(habits):
                    print(f"  - {name}")
                print("")

            elif sub_choice == "List by periodicity":
                # Let the user filter by daily or weekly
                p_type = questionary.select(
                    "Which type?", choices=["daily", "weekly"]
                ).ask()
                results = analytics.get_habits_by_periodicity(habits, p_type)
                print(f"\n📋 {p_type.capitalize()} Habits:")
                for h in results:
                    print(f"  - {h.name}")
                print("")

            elif sub_choice == "Longest streak for a specific habit":
                # Calculate the longest streak for one chosen habit
                habit_names = analytics.get_all_habits(habits)
                selected = questionary.select(
                    "Select habit:", choices=habit_names
                ).ask()
                for h in habits:
                    if h.name == selected:
                        streak = analytics.calculate_longest_streak(h)
                        print(f"\n🔥 Longest streak for '{h.name}': {streak}")

            elif sub_choice == "Longest streak across ALL habits":
                # Find the habit with the best streak overall
                result = analytics.get_longest_streak_for_all(habits)
                print(f"\n🏆 {result}")

        # ---- CREATE ----
        elif choice == "Create a new habit":
            # Prompt for the new habit's details
            name = questionary.text("Habit name:").ask()
            period = questionary.select(
                "Periodicity:", choices=["daily", "weekly"]
            ).ask()

            # Create the Habit object and add it to the list
            habits.append(Habit(name, period))
            db.save_data(habits)  # Persist immediately
            print(f"✨ Created '{name}'!")

        # ---- EDIT ----
        elif choice == "Edit a habit":
            habit_names = analytics.get_all_habits(habits)

            # Guard clause: cannot edit if there are no habits
            if not habit_names:
                print("No habits found!")
                continue

            # Let the user select which habit to edit
            selected = questionary.select(
                "Which habit do you want to edit?", choices=habit_names
            ).ask()

            # Ask what the user wants to change
            edit_choice = questionary.select(
                "What would you like to edit?",
                choices=["Name", "Periodicity", "Both"],
            ).ask()

            # Find the matching Habit object
            for h in habits:
                if h.name == selected:
                    new_name = None
                    new_periodicity = None

                    # Collect the new name if requested
                    if edit_choice in ("Name", "Both"):
                        new_name = questionary.text(
                            "New name:", default=h.name
                        ).ask()

                    # Collect the new periodicity if requested
                    if edit_choice in ("Periodicity", "Both"):
                        new_periodicity = questionary.select(
                            "New periodicity:",
                            choices=["daily", "weekly"],
                        ).ask()

                    # Apply the edit using the Habit's edit method
                    h.edit(new_name=new_name, new_periodicity=new_periodicity)
                    db.save_data(habits)  # Persist the change
                    print(f"✏️ Updated habit to '{h.name}' ({h.periodicity}).")
                    break

        # ---- DELETE ----
        elif choice == "Delete a habit":
            habit_names = analytics.get_all_habits(habits)

            # Guard clause: cannot delete if there are no habits
            if not habit_names:
                print("No habits found!")
                continue

            # Let the user select which habit to delete
            selected = questionary.select(
                "Delete which habit?", choices=habit_names
            ).ask()

            # Remove the matching habit from the list using a list comprehension
            habits = [h for h in habits if h.name != selected]
            db.save_data(habits)  # Persist the deletion
            print(f"🗑️ Deleted '{selected}'.")


# ======================================================================
# Entry Point
# ======================================================================

if __name__ == "__main__":
    cli()