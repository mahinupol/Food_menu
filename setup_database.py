#!/usr/bin/env python3
"""
Database Setup Script for Smart Digital Food Menu
This script initializes the database with schema and sample data
"""

import sqlite3
import os
import sys
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
        schema_path = Path('database_schema.sql')
        if schema_path.exists():
            with open(schema_path, 'r') as schema_file:
                # Split SQL file into individual statements
                sql_content = schema_file.read()
                # Remove MySQL-specific syntax for SQLite compatibility
                sql_content = sql_content.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
                sql_content = sql_content.replace('INT PRIMARY KEY AUTO_INCREMENT', 'INTEGER PRIMARY KEY AUTOINCREMENT')
                sql_content = sql_content.replace('ENGINE=InnoDB', '')
                sql_content = sql_content.replace('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', 'DEFAULT CURRENT_TIMESTAMP')
                
                # Execute each statement separately
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement.upper().startswith(('CREATE', 'DROP', 'INSERT', 'ALTER')):
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

def create_mysql_database():
    """Create MySQL database (requires MySQL server running)"""
    try:
        import mysql.connector
        from mysql.connector import Error
        
        # MySQL connection configuration
        config = {
            'host': 'localhost',
            'user': input("Enter MySQL username: "),
            'password': input("Enter MySQL password: "),
            'port': 3306
        }
        
        # Connect to MySQL server
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database
        database_name = 'smart_food_menu'
        cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cursor.execute(f"CREATE DATABASE {database_name}")
        cursor.execute(f"USE {database_name}")
        
        print(f"Created MySQL database: {database_name}")
        
        # Read and execute schema file
        schema_path = Path('database_schema.sql')
        if schema_path.exists():
            with open(schema_path, 'r') as schema_file:
                sql_content = schema_file.read()
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement.upper().startswith(('CREATE', 'DROP', 'INSERT', 'ALTER')):
                        try:
                            cursor.execute(statement)
                        except Error as e:
                            print(f"Warning - SQL statement failed: {e}")
                            continue
                
                connection.commit()
                print("✓ Database schema created successfully")
        
        # Read and execute data file
        data_path = Path('database_data.sql')
        if data_path.exists():
            with open(data_path, 'r') as data_file:
                sql_content = data_file.read()
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement.upper().startswith('INSERT'):
                        try:
                            cursor.execute(statement)
                        except Error as e:
                            print(f"Warning - Data insertion failed: {e}")
                            continue
                
                connection.commit()
                print("✓ Sample data inserted successfully")
        
        connection.close()
        
        print(f"🎉 MySQL database setup completed successfully!")
        print(f"Database: {database_name}")
        print(f"Update database_config.py with your MySQL credentials")
        
        return True
        
    except ImportError:
        print("MySQL connector not installed. Install with: pip install mysql-connector-python")
        return False
    except Exception as e:
        print(f"Error setting up MySQL database: {e}")
        return False

def install_requirements():
    """Install Python requirements"""
    try:
        import subprocess
        import sys
        
        requirements = [
            'flask',
            'flask-cors',
            'werkzeug'
        ]
        
        print("Installing Python requirements...")
        for req in requirements:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
                print(f"✓ Installed {req}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {req}")
        
        return True
    except Exception as e:
        print(f"Error installing requirements: {e}")
        return False

def main():
    """Main setup function"""
    print("Smart Digital Food Menu - Database Setup")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ['database_schema.sql', 'database_data.sql', 'database_config.py']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        return False
    
    # Install requirements
    print("Step 1: Installing Python requirements...")
    if not install_requirements():
        print("Warning: Some requirements failed to install")
    
    # Choose database type
    print("\nStep 2: Choose database type:")
    print("1. SQLite (recommended for development)")
    print("2. MySQL (for production)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '2':
        success = create_mysql_database()
    else:
        success = create_sqlite_database()
    
    if success:
        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run the API server: python food_menu_api.py")
        print("2. Access the API at: http://localhost:5000")
        print("3. Test endpoints:")
        print("   - GET /api/health-conditions")
        print("   - GET /api/foods")
        print("   - POST /api/food-recommendations")
        print("\nIntegrate with your existing HTML/JavaScript frontend!")
    else:
        print("\nSetup failed. Please check the error messages above.")
        return False
    
    return True

if __name__ == "__main__":
    main()