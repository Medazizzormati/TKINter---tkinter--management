#!/usr/bin/env python3
"""
Database Setup Script for Smart Management System
Run this script to create the database and insert sample data.
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DB_CONFIG

def execute_sql_file(cursor, filename):
    """Execute SQL commands from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            sql_content = file.read()

        # Split by semicolon and execute each statement
        statements = sql_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                cursor.execute(statement)
                print(f"Executed: {statement[:50]}...")

    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return False
    except Error as e:
        print(f"Error executing {filename}: {e}")
        return False
    return True

def setup_database():
    """Setup the database and tables"""
    try:
        # Connect without specifying database first
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database', None)

        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()

        print("Connected to MySQL server successfully")

        # Create database and tables
        print("Creating database and tables...")
        if not execute_sql_file(cursor, 'sql/schema.sql'):
            return False

        # Insert sample data
        print("Inserting sample data...")
        if not execute_sql_file(cursor, 'sql/data.sql'):
            return False

        connection.commit()
        print("Database setup completed successfully!")
        print("Default login credentials:")
        print("Username: admin")
        print("Password: admin123")

        return True

    except Error as e:
        print(f"Database setup failed: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("Smart Management System - Database Setup")
    print("=" * 50)

    if setup_database():
        print("\nYou can now run the application with: python main.py")
    else:
        print("\nDatabase setup failed. Please check your MySQL configuration.")
        sys.exit(1)