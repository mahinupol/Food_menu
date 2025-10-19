#!/usr/bin/env python3
"""
Simple Database Setup Script for Smart Digital Food Menu
This script initializes the database with schema and sample data
"""

import sqlite3
import os
from pathlib import Path

def create_sqlite_database():
    """Create SQLite database and execute schema and data files"""
    try:
        # Database file path
        db_path = 'smart_food_menu.db'
        
        # Remove existing database if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Removed existing database: {db_path}")
        
        # Create new database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Created new SQLite database: smart_food_menu.db")
        
        # Read and execute schema file
        schema_path = Path('database_schema_sqlite.sql')
        if schema_path.exists():
            with open(schema_path, 'r') as schema_file:
                # Split SQL file into individual statements
                sql_content = schema_file.read()
                # Remove MySQL-specific syntax for SQLite compatibility
                sql_content = sql_content.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
                sql_content = sql_content.replace('INT PRIMARY KEY AUTO_INCREMENT', 'INTEGER PRIMARY KEY AUTOINCREMENT')
                sql_content = sql_content.replace('ENGINE=InnoDB', '')
                sql_content = sql_content.replace('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', 'DEFAULT CURRENT_TIMESTAMP')
                
                # Split into statements and execute them in order
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                # Separate table creation statements from indexes and views
                create_table_statements = []
                drop_table_statements = []
                index_statements = []
                view_statements = []
                
                for statement in statements:
                    if statement.upper().startswith('CREATE TABLE'):
                        create_table_statements.append(statement)
                    elif statement.upper().startswith('DROP TABLE'):
                        drop_table_statements.append(statement)
                    elif statement.upper().startswith('CREATE INDEX'):
                        index_statements.append(statement)
                    elif statement.upper().startswith('CREATE VIEW'):
                        view_statements.append(statement)
                    elif statement.upper().startswith(('INSERT', 'ALTER')):
                        # Execute other statements immediately
                        try:
                            cursor.execute(statement)
                            print(f"Executed: {statement[:50]}...")
                        except sqlite3.Error as e:
                            print(f"Warning - SQL statement failed: {e}")
                            print(f"Statement: {statement[:100]}...")
                            continue
                
                # Execute table creation statements first (skip DROP statements)
                print("Creating tables...")
                for statement in create_table_statements:
                    try:
                        cursor.execute(statement)
                        print(f"Executed: {statement[:50]}...")
                    except sqlite3.Error as e:
                        print(f"Warning - SQL statement failed: {e}")
                        print(f"Statement: {statement[:100]}...")
                        continue
                
                # Commit table creation
                conn.commit()
                
                # Execute index statements
                print("Creating indexes...")
                for statement in index_statements:
                    try:
                        cursor.execute(statement)
                        print(f"Executed: {statement[:50]}...")
                    except sqlite3.Error as e:
                        print(f"Warning - SQL statement failed: {e}")
                        print(f"Statement: {statement[:100]}...")
                        continue
                
                # Execute view statements
                print("Creating views...")
                for statement in view_statements:
                    try:
                        cursor.execute(statement)
                        print(f"Executed: {statement[:50]}...")
                    except sqlite3.Error as e:
                        print(f"Warning - SQL statement failed: {e}")
                        print(f"Statement: {statement[:100]}...")
                        continue
                
                conn.commit()
                print("✓ Database schema created successfully")
        else:
            print("Error: database_schema.sql file not found")
            return False
        
        # Read and execute data file
        data_path = Path('database_data.sql')
        if data_path.exists():
            with open(data_path, 'r') as data_file:
                sql_content = data_file.read()
                
                # Execute each statement separately
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement.upper().startswith('INSERT'):
                        try:
                            cursor.execute(statement)
                        except sqlite3.Error as e:
                            print(f"Warning - Data insertion failed: {e}")
                            print(f"Statement: {statement[:100]}...")
                            continue
                
                conn.commit()
                print("✓ Sample data inserted successfully")
        else:
            print("Warning: database_data.sql file not found - skipping sample data")
        
        # Verify the setup by checking table contents
        print("\n=== Database Setup Verification ===")
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        print(f"Created {len(tables)} tables:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  - {table[0]}: {count} records")
        
        # Test some key queries
        print("\n=== Testing Key Queries ===")
        
        # Test health conditions
        cursor.execute("SELECT COUNT(*) FROM health_conditions")
        conditions_count = cursor.fetchone()[0]
        print(f"✓ Health conditions: {conditions_count}")
        
        # Test food items
        cursor.execute("SELECT COUNT(*) FROM food_items")
        foods_count = cursor.fetchone()[0]
        print(f"✓ Food items: {foods_count}")
        
        # Test recommendations
        cursor.execute("SELECT COUNT(*) FROM food_recommendations")
        recommendations_count = cursor.fetchone()[0]
        print(f"✓ Food recommendations: {recommendations_count}")
        
        # Test nutrition facts
        cursor.execute("SELECT COUNT(*) FROM nutrition_facts")
        nutrition_count = cursor.fetchone()[0]
        print(f"✓ Nutrition facts: {nutrition_count}")
        
        # Test a complex query
        cursor.execute("""
            SELECT fi.food_name, fc.category_name, fr.recommendation_type
            FROM food_items fi
            JOIN food_categories fc ON fi.category_id = fc.category_id
            JOIN food_recommendations fr ON fi.food_id = fr.food_id
            LIMIT 5
        """)
        sample_recommendations = cursor.fetchall()
        
        if sample_recommendations:
            print("\n✓ Sample recommendations query successful:")
            for rec in sample_recommendations:
                print(f"  - {rec[0]} ({rec[1]}): {rec[2]}")
        
        conn.close()
        
        print(f"\n🎉 Database setup completed successfully!")
        print(f"Database file: {os.path.abspath(db_path)}")
        print(f"You can now run the API server with: python food_menu_api.py")
        
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == "__main__":
    create_sqlite_database()