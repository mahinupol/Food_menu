"""
Food-related Database Operations for Smart Digital Food Menu
Handles food items, categories, nutrition facts, and recommendations
"""

from typing import Optional, List, Dict, Any, Tuple
from .operations import DatabaseOperations


class FoodOperations(DatabaseOperations):
    """Food-specific database operations"""
    
    def get_all_food_categories(self) -> Optional[List]:
        """Get all food categories"""
        query = "SELECT category_id, category_name, description FROM food_categories ORDER BY category_name"
        return self.execute_query(query)
    
    def get_all_health_conditions(self) -> Optional[List]:
        """Get all health conditions"""
        query = "SELECT condition_id, condition_name, condition_code, description FROM health_conditions ORDER BY condition_name"
        return self.execute_query(query)
    
    def search_foods(self, search_term: str, category_filter: Optional[str] = None) -> Optional[List]:
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
    
    def get_food_recommendations_for_user(self, user_id: int) -> Optional[List]:
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
    
    def get_foods_to_avoid_for_user(self, user_id: int) -> Optional[List]:
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
    
    def get_nutrition_facts(self, food_id: int) -> Optional[Tuple]:
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