"""
Basic Database Operations for Smart Digital Food Menu
Handles common database operations like query execution and updates
"""

from typing import Optional, Tuple, List
from .connection import DatabaseConfig


class DatabaseOperations:
    """Common database operations for the Smart Food Menu application"""
    
    def __init__(self):
        self.connection = DatabaseConfig.get_connection()
        self.is_mysql = DatabaseConfig.DATABASE_TYPE == 'mysql' and MYSQL_AVAILABLE
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Optional[List]:
        """Execute a SELECT query and return results"""
        if not self.connection:
            print("No database connection available")
            return None
            
        try:
            cursor = self.connection.cursor()
            # Adjust query for MySQL if needed
            if self.is_mysql:
                query = query.replace('?', '%s')
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            cursor.close()
            
            # Convert MySQL results to list of tuples for consistency
            if self.is_mysql and results:
                return [tuple(row) for row in results]
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> bool:
        """Execute an INSERT, UPDATE, or DELETE query"""
        if not self.connection:
            print("No database connection available")
            return False
            
        try:
            cursor = self.connection.cursor()
            # Adjust query for MySQL if needed
            if self.is_mysql:
                query = query.replace('?', '%s')
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if not self.is_mysql:  # SQLite needs explicit commit
                self.connection.commit()
            
            cursor.close()
            return True
        except Exception as e:
            print(f"Error executing update: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        DatabaseConfig.close_connection(self.connection)