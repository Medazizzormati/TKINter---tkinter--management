# Smart Management System

A modern Desktop Management Application built with Python, CustomTkinter, and MySQL.

## Features
- **User Authentication**: Login and signup functionality with secure password hashing
- **Full CRUD**: Manage Categories, Products, and Orders
- **Modern UI**: Dark mode supporting sidebar navigation
- **Advanced Tools**: Statistics dashboard, Dynamic Search, Column Sorting, and CSV Export
- **Robust Architecture**: Follows MVC (Model-View-Controller) design pattern

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure your MySQL credentials in `config.py`.
4. Run the database setup script: `python setup_db.py`.
5. Run the app: `python main.py` or use `run.bat`.

## Database Setup
The `setup_db.py` script will:
- Create the `smart_management_system` database
- Create all necessary tables (users, categories, products, orders)
- Insert sample data including a default admin user

## Credentials (Default)
- **User**: admin
- **Password**: admin123

## User Management
- **Login**: Use existing username and password
- **Signup**: Create new accounts directly from the login screen
- Passwords are securely hashed using SHA-256
# TKINter---tkinter--management
