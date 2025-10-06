# Database Configuration for Smart Digital Food Menu
# Copy this file to 'database_config.py' and update with your actual database credentials

import os
import mysql.connector
from mysql.connector import Error
import sqlite3
from typing import Optional, Dict, Any

class DatabaseConfig:
    """Database configuration and connection management"""
    
    # MySQL Configuration (Production)
    MYSQL_CONFIG = {
        'host': 'localhost',
        'database': 'smart_food_menu',
        'user': 'your_username',
        'password': 'your_password',
        'port': 3306,
        'charset': 'utf8mb4',
        'autocommit': True
    }
    
    # SQLite Configuration (Development/Testing)
    SQLITE_CONFIG = {
        'database': 'smart_food_menu.db'
    }
    
    # Environment-based database selection
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')  # 'mysql' or 'sqlite'
    
    @classmethod
    def get_mysql_connection(cls) -> Optional[mysql.connector.MySQLConnection]:
        """Create and return MySQL database connection"""
        try:
            connection = mysql.connector.connect(**cls.MYSQL_CONFIG)
            if connection.is_connected():
                print("Successfully connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @classmethod
    def get_sqlite_connection(cls) -> Optional[sqlite3.Connection]:
        """Create and return SQLite database connection"""
        try:
            connection = sqlite3.connect(cls.SQLITE_CONFIG['database'])
            connection.row_factory = sqlite3.Row  # Enable dict-like access to rows
            print("Successfully connected to SQLite database")
            return connection
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            return None
    
    @classmethod
    def get_connection(cls):
        """Get database connection based on environment configuration"""
        if cls.DATABASE_TYPE.lower() == 'mysql':
            return cls.get_mysql_connection()
        else:
            return cls.get_sqlite_connection()
    
    @classmethod
    def close_connection(cls, connection):
        """Close database connection"""
        if connection:
            try:
                connection.close()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing connection: {e}")

class DatabaseOperations:
    """Common database operations for the Smart Food Menu application"""
    
    def __init__(self):
        self.connection = DatabaseConfig.get_connection()
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        """Execute a SELECT query and return results"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute an INSERT, UPDATE, or DELETE query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error executing update: {e}")
            return False
    
    def get_user_health_conditions(self, user_id: int) -> list:
        """Get all health conditions for a specific user"""
        query = """
        SELECT hc.condition_name, hc.condition_code, uhc.severity
        FROM user_health_conditions uhc
        JOIN health_conditions hc ON uhc.condition_id = hc.condition_id
        WHERE uhc.user_id = ?
        """
        return self.execute_query(query, (user_id,))
    
    def get_food_recommendations_for_user(self, user_id: int) -> list:
        """Get personalized food recommendations for a user based on their health conditions"""
        query = """
        SELECT DISTINCT fi.food_name, fc.category_name, fr.recommendation_type, 
               fr.safety_score, fr.reasoning, nf.calories, nf.protein_g, 
               nf.carbs_g, nf.fat_g, nf.sodium_mg, fi.image_path
        FROM food_items fi
        JOIN food_categories fc ON fi.category_id = fc.category_id
        JOIN nutrition_facts nf ON fi.food_id = nf.food_id
        JOIN food_recommendations fr ON fi.food_id = fr.food_id
        JOIN user_health_conditions uhc ON fr.condition_id = uhc.condition_id
        WHERE uhc.user_id = ? AND fr.recommendation_type IN ('Highly Recommended', 'Recommended')
        ORDER BY fr.safety_score DESC, fi.food_name
        """
        return self.execute_query(query, (user_id,))
    
    def get_foods_to_avoid_for_user(self, user_id: int) -> list:
        """Get foods that should be avoided by a user based on their health conditions"""
        query = """
        SELECT DISTINCT fi.food_name, fc.category_name, fr.recommendation_type, 
               fr.reasoning, fi.image_path
        FROM food_items fi
        JOIN food_categories fc ON fi.category_id = fc.category_id
        JOIN food_recommendations fr ON fi.food_id = fr.food_id
        JOIN user_health_conditions uhc ON fr.condition_id = uhc.condition_id
        WHERE uhc.user_id = ? AND fr.recommendation_type IN ('Avoid', 'Caution')
        ORDER BY fr.recommendation_type, fi.food_name
        """
        return self.execute_query(query, (user_id,))
    
    def search_foods(self, search_term: str, category_filter: str = None) -> list:
        """Search for foods by name or category"""
        if category_filter:
            query = """
            SELECT fi.food_id, fi.food_name, fc.category_name, fi.description,
                   fi.image_path, nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g
            FROM food_items fi
            JOIN food_categories fc ON fi.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
            WHERE (fi.food_name LIKE ? OR fi.description LIKE ?) 
                  AND fc.category_name = ?
            ORDER BY fi.food_name
            """
            search_pattern = f"%{search_term}%"
            return self.execute_query(query, (search_pattern, search_pattern, category_filter))
        else:
            query = """
            SELECT fi.food_id, fi.food_name, fc.category_name, fi.description,
                   fi.image_path, nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g
            FROM food_items fi
            JOIN food_categories fc ON fi.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
            WHERE fi.food_name LIKE ? OR fi.description LIKE ?
            ORDER BY fi.food_name
            """
            search_pattern = f"%{search_term}%"
            return self.execute_query(query, (search_pattern, search_pattern))
    
    def get_nutrition_facts(self, food_id: int) -> Optional[dict]:
        """Get detailed nutrition facts for a specific food item"""
        query = """
        SELECT nf.*, fi.food_name, fi.serving_size, fi.serving_unit
        FROM nutrition_facts nf
        JOIN food_items fi ON nf.food_id = fi.food_id
        WHERE nf.food_id = ?
        """
        result = self.execute_query(query, (food_id,))
        return result[0] if result else None
    
    def add_user_meal_plan(self, user_id: int, plan_data: Dict[str, Any]) -> bool:
        """Add a meal to user's meal plan"""
        query = """
        INSERT INTO user_meal_plans 
        (user_id, plan_name, plan_date, meal_type, food_id, portion_size, 
         portion_unit, calories_consumed, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            user_id,
            plan_data['plan_name'],
            plan_data['plan_date'],
            plan_data['meal_type'],
            plan_data['food_id'],
            plan_data['portion_size'],
            plan_data['portion_unit'],
            plan_data['calories_consumed'],
            plan_data.get('notes', '')
        )
        return self.execute_update(query, params)
    
    def get_user_daily_nutrition(self, user_id: int, date: str) -> Dict[str, float]:
        """Calculate total daily nutrition for a user on a specific date"""
        query = """
        SELECT SUM(ump.calories_consumed) as total_calories,
               SUM(nf.protein_g * ump.portion_size / 100) as total_protein,
               SUM(nf.carbs_g * ump.portion_size / 100) as total_carbs,
               SUM(nf.fat_g * ump.portion_size / 100) as total_fat,
               SUM(nf.sodium_mg * ump.portion_size / 100) as total_sodium
        FROM user_meal_plans ump
        JOIN nutrition_facts nf ON ump.food_id = nf.food_id
        WHERE ump.user_id = ? AND ump.plan_date = ? AND ump.is_completed = 1
        """
        result = self.execute_query(query, (user_id, date))
        if result and result[0]:
            return {
                'calories': result[0][0] or 0,
                'protein': result[0][1] or 0,
                'carbs': result[0][2] or 0,
                'fat': result[0][3] or 0,
                'sodium': result[0][4] or 0
            }
        return {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'sodium': 0}
    
    def close(self):
        """Close database connection"""
        DatabaseConfig.close_connection(self.connection)

# Example usage and testing
if __name__ == "__main__":
    # Test database connection
    db = DatabaseOperations()
    
    # Test queries
    print("Testing database connection and queries...")
    
    # Get all food categories
    categories = db.execute_query("SELECT * FROM food_categories LIMIT 5")
    print(f"Food categories: {categories}")
    
    # Get all health conditions
    conditions = db.execute_query("SELECT condition_name, condition_code FROM health_conditions")
    print(f"Health conditions: {conditions}")
    
    # Search for foods
    foods = db.search_foods("chicken")
    print(f"Foods matching 'chicken': {foods}")
    
    # Close connection
    db.close()