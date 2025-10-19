# 🗄️ Database Configuration Structure

This directory contains a reorganized database configuration structure for the Smart Digital Food Menu project, making it easier to understand and maintain.

## 📁 Directory Structure

```
db_config/
├── __init__.py          # Package initialization
├── connection.py        # Database connection management
├── operations.py        # Basic database operations
├── food_operations.py   # Food-specific database operations
└── manager.py          # Main database manager
```

## 📄 File Descriptions

### `connection.py`
Handles database connection setup for both SQLite (development) and MySQL (production) databases.
- Database configuration settings
- Connection establishment and management
- Fallback mechanisms

### `operations.py`
Provides basic database operations that can be used by other modules.
- Query execution (`SELECT` statements)
- Update execution (`INSERT`, `UPDATE`, `DELETE` statements)
- Connection management

### `food_operations.py`
Contains all food-related database operations.
- Food item and category management
- Nutrition facts retrieval
- Food recommendations based on health conditions
- Meal planning functionality

### `manager.py`
Main database manager that combines all operations into a single interface.
- Inherits from `FoodOperations`
- Provides health check functionality
- Centralized database access point

## 🔄 Usage

```python
# Import the database manager
from db_config.manager import DatabaseManager

# Initialize database connection
db = DatabaseManager()

# Use database operations
foods = db.search_foods("chicken")

# Close connection when done
db.close()
```

## 🛠️ Benefits of This Structure

1. **Modularity**: Each file has a specific responsibility
2. **Maintainability**: Easier to locate and modify specific functionality
3. **Reusability**: Components can be used independently
4. **Scalability**: Easy to add new database operations
5. **Clarity**: Clear separation of concerns

## 📝 Migration Notes

The previous monolithic `database_config.py` file has been split into multiple specialized files:
- Connection management moved to `connection.py`
- Basic operations moved to `operations.py`
- Food operations moved to `food_operations.py`
- Main interface provided by `manager.py`

This structure maintains full backward compatibility while providing better organization.