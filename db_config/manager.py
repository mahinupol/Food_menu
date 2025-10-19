"""
Database Manager for Smart Digital Food Menu
Main interface for all database operations
"""

from .connection import DatabaseConfig
from .operations import DatabaseOperations
# Removed user_operations import as we're removing login/registration feature
# from .user_operations import UserOperations
from .food_operations import FoodOperations


class DatabaseManager(FoodOperations):
    """
    Main database manager that combines all database operations
    Inherits from FoodOperations only (UserOperations removed)
    """
    
    def __init__(self):
        # Initialize the base DatabaseOperations class
        DatabaseOperations.__init__(self)
    
    def health_check(self) -> bool:
        """Check if database connection is healthy"""
        try:
            result = self.execute_query("SELECT 1")
            return bool(result)
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def get_database_info(self) -> dict:
        """Get database information"""
        return {
            'database_type': DatabaseConfig.DATABASE_TYPE,
            'is_mysql': self.is_mysql,
            'connection_status': 'connected' if self.connection else 'disconnected'
        }


# Example usage
if __name__ == "__main__":
    # Test database connection
    db = DatabaseManager()
    
    # Test health check
    print("Database health check:", db.health_check())
    
    # Get database info
    print("Database info:", db.get_database_info())
    
    # Test queries
    print("Testing database connection and queries...")
    
    # Get all food categories
    categories = db.get_all_food_categories()
    print(f"Food categories: {categories[:5] if categories else 'None'}")
    
    # Get all health conditions
    conditions = db.get_all_health_conditions()
    print(f"Health conditions: {len(conditions) if conditions else 0} found")
    
    # Close connection
    db.close()