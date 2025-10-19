"""
User-related Database Operations for Smart Digital Food Menu
Handles user authentication, registration, and user-specific data
"""

from typing import Optional, List, Dict, Any
from .operations import DatabaseOperations


class UserOperations(DatabaseOperations):
    """User-specific database operations"""
    
    def get_user_by_username_or_email(self, username_or_email: str) -> Optional[Dict]:
        """Get user by username or email"""
        query = """
        SELECT user_id, username, email, password_hash, first_name, last_name, 
               date_of_birth, gender, height_cm, weight_kg, activity_level, 
               dietary_preference, created_at, last_login
        FROM users 
        WHERE username = ? OR email = ?
        """
        result = self.execute_query(query, (username_or_email, username_or_email))
        return result[0] if result else None
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[int]:
        """Create a new user and return user_id"""
        query = """
        INSERT INTO users (username, email, password_hash, first_name, last_name, 
                          date_of_birth, gender, height_cm, weight_kg, 
                          activity_level, dietary_preference)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            user_data['username'],
            user_data['email'],
            user_data['password_hash'],
            user_data['first_name'],
            user_data['last_name'],
            user_data.get('date_of_birth'),
            user_data.get('gender'),
            user_data.get('height_cm'),
            user_data.get('weight_kg'),
            user_data.get('activity_level'),
            user_data.get('dietary_preference')
        )
        
        if self.execute_update(query, params):
            # Get the newly created user ID
            user_id_query = "SELECT user_id FROM users WHERE username = ?"
            user_result = self.execute_query(user_id_query, (user_data['username'],))
            return user_result[0][0] if user_result else None
        return None
    
    def update_user_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp"""
        from datetime import datetime
        query = "UPDATE users SET last_login = ? WHERE user_id = ?"
        return self.execute_update(query, (datetime.now(), user_id))
    
    def check_user_exists(self, username: str, email: str) -> bool:
        """Check if user with given username or email already exists"""
        query = "SELECT user_id FROM users WHERE username = ? OR email = ?"
        result = self.execute_query(query, (username, email))
        return bool(result)
    
    def add_user_health_condition(self, user_id: int, condition_id: int, 
                                 severity: str = 'Moderate', diagnosed_date: Optional[str] = None) -> bool:
        """Add a health condition to a user"""
        query = """
        INSERT INTO user_health_conditions (user_id, condition_id, severity, diagnosed_date)
        VALUES (?, ?, ?, ?)
        """
        params = (user_id, condition_id, severity, diagnosed_date)
        return self.execute_update(query, params)
    
    def get_user_health_conditions(self, user_id: int) -> Optional[List]:
        """Get all health conditions for a specific user"""
        query = """
        SELECT hc.condition_name, hc.condition_code, uhc.severity
        FROM user_health_conditions uhc
        JOIN health_conditions hc ON uhc.condition_id = hc.condition_id
        WHERE uhc.user_id = ?
        """
        return self.execute_query(query, (user_id,))