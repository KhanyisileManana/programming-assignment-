


```markdown
# Smart Campus Resource Booking System


## Project Overview
The Smart Campus Resource Booking System is a Python-based desktop application built using Tkinter for the Graphical User Interface (GUI) and SQLite for data persistence. It replaces the manual, fragmented booking processes at Richfield Graduate Institution with a centralized, role-based system. 

The system supports multiple campuses, enforces campus-specific booking policies, and prevents overlapping bookings.

## Core Features
* **Role-Based Access Control (RBAC):** Three distinct user roles (Lecturer, Campus Admin, System Operator) implemented using Object-Oriented Programming (Inheritance and Encapsulation).
* **Campus-Specific Booking Policies:** Uses the Strategy Design Pattern to enforce different rules for different campuses (Strict, Moderate, Flexible).
* **Booking Management:** Lecturers can book resources, view their history, and cancel future bookings. The system prevents double-bookings.
* **Resource Management:** Campus Admins can add, update, and delete resources specific to their campus.
* **Reporting:** System Operators can generate cross-campus comparative reports and view usage trends.
* **Persistent Storage:** All users, resources, and bookings are saved in a local SQLite database (`smart_campus.db`).

## Prerequisites
* Python 3.8 or higher
* Tkinter (usually included with standard Python installations)
* SQLite3 (included with Python)

## Project Structure
```text
smart_campus/
│
├── gui/                      # Contains all Tkinter GUI screens
│   ├── __init__.py
│   ├── admin_window.py       # Admin dashboard
│   ├── lecturer.py           # Lecturer dashboard
│   ├── login.py              # Login screen
│   ├── operator_window.py    # Operator dashboard
│   ├── register.py           # Lecturer registration screen
│   └── styles.py             # GUI color themes (Pink/Purple/White)
│
├── booking_rules.py          # Strategy pattern for campus booking policies
├── database.py               # SQLite database schema and CRUD operations
├── main.py                   # Application entry point
├── models.py                 # OOP Class hierarchy (User, Lecturer, Admin, Operator)
├── seed_resources.py         # Script to initialize the database with default data
└── services.py               # Core business logic for validating bookings
```

How to Run the Application

1. Initialize the Database:
   Before running the app for the first time, you must run the seed script to create the database tables and default accounts. Open your terminal in the project folder and run:
   ```bash
   python seed_resources.py
   ```
   (Note: If you ever need to reset the system, delete smart_campus.db and run this script again).
2. Start the Application:
   Run the main file to open the GUI:
   ```bash
   python main.py
   ```

Default Login Credentials

To test the different roles, use the following default accounts created by the seed script.

Password for all default accounts: Khanyi123

Role Username Access Level
System Operator operator Full system access, cross-campus reports.
Campus Admin (JHB) admin_johannesburg Manage JHB resources, view JHB bookings.
Campus Admin (CPT) admin_capetown Manage CPT resources, view CPT bookings.
Campus Admin (DBN) admin_durban Manage DBN resources, view DBN bookings.

Note: Lecturers can create their own accounts using the "Register as Lecturer" button on the login screen.

Campus Booking Policies

Each campus applies a unique rule set (handled dynamically by booking_rules.py):

· Johannesburg (Strict): Bookings allowed only 09:00–16:00. Maximum duration of 60 minutes.
· Cape Town (Moderate): Bookings allowed only 08:00–18:00. Maximum duration of 120 minutes.
· Durban (Flexible): Bookings allowed 07:00–22:00. Maximum duration of 240 minutes.
https://github.com/KhanyisileManana/programming-assignment-.git

```
