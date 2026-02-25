# 🏆 Habit Tracker – CLI Application

A command-line Habit Tracker built in **Python** that helps you create, manage, and analyze your daily and weekly habits. Track your streaks, view analytics reports, and stay on top of your goals — all from the terminal.

---

## 📖 Description

This project was built as part of the **IU University Python Portfolio (Phase 3)**. It showcases clean, modular Python design using:

- **Object-Oriented Programming** – The `Habit` class encapsulates all habit data and behavior.
- **Functional Programming** – The `analytics` module uses pure functions, `filter()`, `map()`, and lambdas.
- **JSON Persistence** – Habits are saved to and loaded from a local `habits.json` file.
- **Interactive CLI** – The `questionary` library provides a polished, arrow-key-driven menu interface.

On first run, the app automatically generates **5 predefined habits with 4 weeks of sample data** so you can explore analytics immediately.

---

## ✨ Features

| Feature                     | Description                                                  |
|-----------------------------|--------------------------------------------------------------|
| ✅ Check-off a habit        | Record a completion for today                                |
| ➕ Create a habit           | Add a new daily or weekly habit                              |
| ✏️ Edit a habit             | Change a habit's name, periodicity, or both                  |
| 🗑️ Delete a habit           | Remove a habit permanently                                   |
| 📋 List all habits          | View every tracked habit                                     |
| 📋 List by periodicity      | Filter habits by daily or weekly                             |
| 🔥 Longest streak (single)  | See the best streak for one specific habit                   |
| 🏆 Longest streak (all)     | Find the habit with the best streak across all habits        |

---

## 🛠️ Installation

### Prerequisites

- **Python 3.9+** installed on your system.

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/habit_tracker.git
   cd habit_tracker
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS / Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install the required dependencies:**

   ```bash
   pip install questionary pytest
   ```

---

## 🚀 Usage

Run the application from the project root:

```bash
python main.py
```

You will be greeted with an interactive menu:

```
👋 Welcome! Loaded 5 habits.
? What would you like to do?
  ❯ Check-off a habit
    Analyze habits
    Create a new habit
    Edit a habit
    Delete a habit
    Exit
```

Use the **arrow keys** to navigate and **Enter** to select an option.



## 🧪 Running the Tests

The project includes a comprehensive test suite (25+ tests) covering:

- Habit creation, editing, and deletion
- Check-off functionality
- Daily streak calculation (including 4-week continuous data)
- Weekly streak calculation (including 4-week continuous data)
- Every function in the analytics module

### Run all tests:

```bash
python -m pytest test_project.py -v
```

### Expected output:

```
test_project.py::TestHabitCRUD::test_habit_creation         PASSED
test_project.py::TestHabitCRUD::test_habit_creation_weekly   PASSED
test_project.py::TestHabitCRUD::test_habit_edit_name         PASSED
...
========================= 25 passed =========================
```

---

## 📁 Project Structure

```
habit_tracker/
├── main.py              # CLI interface (questionary menus)
├── habit.py             # Habit class (OOP data model)
├── analytics.py         # Analytics functions (functional logic)
├── db.py                # JSON persistence (save/load)
├── test_project.py      # Comprehensive pytest test suite
├── habits.json          # Runtime data (created on first run)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── screenshots/         # Your screenshots go here
    ├── menu.png
    ├── analytics.png
    ├── streak.png
    └── tests.png
```

---

## 📄 License

This project was created for educational purposes as part of the IU University Python course.
