#!/usr/bin/env python3
"""
Smart Digital Food Menu API
RESTful API for managing food recommendations based on health conditions
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import json
import os
from typing import Dict, List, Optional, Any

# Import our database operations
from db_config.manager import DatabaseManager

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
CORS(app)  # Enable CORS for frontend integration

# Initialize database
db = DatabaseManager()

@app.route('/')
def index():
    """API health check endpoint"""
    return jsonify({
        'message': 'Smart Digital Food Menu API',
        'version': '1.0.0',
        'status': 'healthy'
    })

@app.route('/api/health-conditions', methods=['GET'])
def get_health_conditions():
    """Get all available health conditions"""
    try:
        query = """
        SELECT condition_id, condition_name, condition_code, description, 
               dietary_restrictions, foods_to_avoid, recommended_foods, icon_path
        FROM health_conditions
        ORDER BY condition_name
        """
        conditions = db.execute_query(query)
        
        if conditions:
            result = []
            for condition in conditions:
                result.append({
                    'id': condition[0],
                    'name': condition[1],
                    'code': condition[2],
                    'description': condition[3],
                    'dietary_restrictions': condition[4],
                    'foods_to_avoid': condition[5],
                    'recommended_foods': condition[6],
                    'icon_path': condition[7]
                })
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'message': 'No health conditions found'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/food-categories', methods=['GET'])
def get_food_categories():
    """Get all food categories"""
    try:
        query = "SELECT category_id, category_name, description FROM food_categories ORDER BY category_name"
        categories = db.execute_query(query)
        
        if categories:
            result = []
            for category in categories:
                result.append({
                    'id': category[0],
                    'name': category[1],
                    'description': category[2]
                })
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'message': 'No categories found'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/foods', methods=['GET'])
def get_foods():
    """Get all foods with optional filtering"""
    try:
        category = request.args.get('category')
        search = request.args.get('search', '')
        
        if category:
            query = """
            SELECT fi.food_id, fi.food_name, fc.category_name, fi.description,
                   fi.image_path, fi.serving_size, fi.serving_unit,
                   fi.is_vegetarian, fi.is_vegan, fi.is_gluten_free, fi.is_dairy_free,
                   nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g, nf.sodium_mg
            FROM food_items fi
            JOIN food_categories fc ON fi.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
            WHERE fc.category_name = ?
            ORDER BY fi.food_name
            """
            foods = db.execute_query(query, (category,))
        elif search:
            search_pattern = f"%{search}%"
            query = """
            SELECT fi.food_id, fi.food_name, fc.category_name, fi.description,
                   fi.image_path, fi.serving_size, fi.serving_unit,
                   fi.is_vegetarian, fi.is_vegan, fi.is_gluten_free, fi.is_dairy_free,
                   nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g, nf.sodium_mg
            FROM food_items fi
            JOIN food_categories fc ON fi.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
            WHERE fi.food_name LIKE ? OR fi.description LIKE ?
            ORDER BY fi.food_name
            """
            foods = db.execute_query(query, (search_pattern, search_pattern))
        else:
            query = """
            SELECT fi.food_id, fi.food_name, fc.category_name, fi.description,
                   fi.image_path, fi.serving_size, fi.serving_unit,
                   fi.is_vegetarian, fi.is_vegan, fi.is_gluten_free, fi.is_dairy_free,
                   nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g, nf.sodium_mg
            FROM food_items fi
            JOIN food_categories fc ON fi.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
            ORDER BY fi.food_name
            """
            foods = db.execute_query(query)
        
        if foods:
            result = []
            for food in foods:
                result.append({
                    'id': food[0],
                    'name': food[1],
                    'category': food[2],
                    'description': food[3],
                    'image_path': food[4],
                    'serving_size': food[5],
                    'serving_unit': food[6],
                    'is_vegetarian': bool(food[7]),
                    'is_vegan': bool(food[8]),
                    'is_gluten_free': bool(food[9]),
                    'is_dairy_free': bool(food[10]),
                    'nutrition': {
                        'calories': float(food[11]) if food[11] else 0,
                        'protein': float(food[12]) if food[12] else 0,
                        'carbs': float(food[13]) if food[13] else 0,
                        'fat': float(food[14]) if food[14] else 0,
                        'sodium': float(food[15]) if food[15] else 0
                    }
                })
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'message': 'No foods found'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/food-recommendations', methods=['POST'])
def get_food_recommendations():
    """Get personalized food recommendations based on health conditions"""
    try:
        data = request.get_json()
        if not data or 'health_conditions' not in data:
            return jsonify({'success': False, 'message': 'Health conditions required'}), 400
        
        health_conditions = data['health_conditions']
        if not isinstance(health_conditions, list) or len(health_conditions) == 0:
            return jsonify({'success': False, 'message': 'At least one health condition required'}), 400
        
        # Convert condition names to condition IDs
        placeholders = ','.join(['?' for _ in health_conditions])
        condition_query = f"""
        SELECT condition_id FROM health_conditions 
        WHERE condition_code IN ({placeholders})
        """
        condition_results = db.execute_query(condition_query, tuple(health_conditions))
        
        if not condition_results:
            return jsonify({'success': False, 'message': 'Invalid health conditions provided'}), 400
        
        condition_ids = [str(result[0]) for result in condition_results]
        
        # Get food recommendations
        rec_placeholders = ','.join(['?' for _ in condition_ids])
        query = f"""
        SELECT DISTINCT fi.food_id, fi.food_name, fc.category_name, fi.description,
               fi.image_path, fr.recommendation_type, fr.safety_score, fr.reasoning,
               nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g, nf.sodium_mg,
               fi.is_vegetarian, fi.is_vegan, fi.is_gluten_free, fi.is_dairy_free
        FROM food_items fi
        JOIN food_categories fc ON fi.category_id = fc.category_id
        JOIN nutrition_facts nf ON fi.food_id = nf.food_id
        JOIN food_recommendations fr ON fi.food_id = fr.food_id
        WHERE fr.condition_id IN ({rec_placeholders})
        ORDER BY fr.safety_score DESC, fi.food_name
        """
        
        recommendations = db.execute_query(query, tuple(condition_ids))
        
        if recommendations:
            # Group recommendations by type
            result = {
                'highly_recommended': [],
                'recommended': [],
                'caution': [],
                'avoid': []
            }
            
            for rec in recommendations:
                food_data = {
                    'id': rec[0],
                    'name': rec[1],
                    'category': rec[2],
                    'description': rec[3],
                    'image_path': rec[4],
                    'safety_score': rec[6],
                    'reasoning': rec[7],
                    'nutrition': {
                        'calories': float(rec[8]) if rec[8] else 0,
                        'protein': float(rec[9]) if rec[9] else 0,
                        'carbs': float(rec[10]) if rec[10] else 0,
                        'fat': float(rec[11]) if rec[11] else 0,
                        'sodium': float(rec[12]) if rec[12] else 0
                    },
                    'dietary_flags': {
                        'vegetarian': bool(rec[13]),
                        'vegan': bool(rec[14]),
                        'gluten_free': bool(rec[15]),
                        'dairy_free': bool(rec[16])
                    }
                }
                
                recommendation_type = rec[5].lower().replace(' ', '_')
                if recommendation_type in result:
                    result[recommendation_type].append(food_data)
            
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'message': 'No recommendations found for provided conditions'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/nutrition/<int:food_id>', methods=['GET'])
def get_nutrition_details(food_id):
    """Get detailed nutrition information for a specific food"""
    try:
        query = """
        SELECT nf.*, fi.food_name, fi.serving_size, fi.serving_unit,
               fi.description, fi.image_path, fc.category_name
        FROM nutrition_facts nf
        JOIN food_items fi ON nf.food_id = fi.food_id
        JOIN food_categories fc ON fi.category_id = fc.category_id
        WHERE nf.food_id = ?
        """
        result = db.execute_query(query, (food_id,))
        
        if result:
            nutrition = result[0]
            data = {
                'food_id': nutrition[1],
                'food_name': nutrition[17],
                'serving_size': nutrition[18],
                'serving_unit': nutrition[19],
                'description': nutrition[20],
                'image_path': nutrition[21],
                'category': nutrition[22],
                'nutrition': {
                    'calories': float(nutrition[2]) if nutrition[2] else 0,
                    'protein_g': float(nutrition[3]) if nutrition[3] else 0,
                    'carbs_g': float(nutrition[4]) if nutrition[4] else 0,
                    'fat_g': float(nutrition[5]) if nutrition[5] else 0,
                    'saturated_fat_g': float(nutrition[6]) if nutrition[6] else 0,
                    'trans_fat_g': float(nutrition[7]) if nutrition[7] else 0,
                    'cholesterol_mg': float(nutrition[8]) if nutrition[8] else 0,
                    'sodium_mg': float(nutrition[9]) if nutrition[9] else 0,
                    'potassium_mg': float(nutrition[10]) if nutrition[10] else 0,
                    'fiber_g': float(nutrition[11]) if nutrition[11] else 0,
                    'sugar_g': float(nutrition[12]) if nutrition[12] else 0,
                    'vitamin_a_iu': float(nutrition[13]) if nutrition[13] else 0,
                    'vitamin_c_mg': float(nutrition[14]) if nutrition[14] else 0,
                    'calcium_mg': float(nutrition[15]) if nutrition[15] else 0,
                    'iron_mg': float(nutrition[16]) if nutrition[16] else 0
                }
            }
            
            # Get allergen information
            allergen_query = """
            SELECT a.allergen_name, fa.severity_level
            FROM food_allergens fa
            JOIN allergens a ON fa.allergen_id = a.allergen_id
            WHERE fa.food_id = ?
            """
            allergens = db.execute_query(allergen_query, (food_id,))
            data['allergens'] = [{'name': a[0], 'severity': a[1]} for a in allergens] if allergens else []
            
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'message': 'Food not found'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/compare-foods', methods=['POST'])
def compare_foods():
    """Compare nutrition facts between two foods"""
    try:
        data = request.get_json()
        if not data or 'food_ids' not in data:
            return jsonify({'success': False, 'message': 'Food IDs required'}), 400
        
        food_ids = data['food_ids']
        if not isinstance(food_ids, list) or len(food_ids) != 2:
            return jsonify({'success': False, 'message': 'Exactly two food IDs required'}), 400
        
        comparisons = []
        for food_id in food_ids:
            query = """
            SELECT fi.food_name, fc.category_name, fi.image_path,
                   nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g, nf.sodium_mg,
                   nf.fiber_g, nf.sugar_g, nf.saturated_fat_g
            FROM food_items fi
            JOIN food_categories fc ON fi.category_id = fc.category_id
            JOIN nutrition_facts nf ON fi.food_id = nf.food_id
            WHERE fi.food_id = ?
            """
            result = db.execute_query(query, (food_id,))
            
            if result:
                food_data = result[0]
                comparisons.append({
                    'id': food_id,
                    'name': food_data[0],
                    'category': food_data[1],
                    'image_path': food_data[2],
                    'nutrition': {
                        'calories': float(food_data[3]) if food_data[3] else 0,
                        'protein': float(food_data[4]) if food_data[4] else 0,
                        'carbs': float(food_data[5]) if food_data[5] else 0,
                        'fat': float(food_data[6]) if food_data[6] else 0,
                        'sodium': float(food_data[7]) if food_data[7] else 0,
                        'fiber': float(food_data[8]) if food_data[8] else 0,
                        'sugar': float(food_data[9]) if food_data[9] else 0,
                        'saturated_fat': float(food_data[10]) if food_data[10] else 0
                    }
                })
            else:
                return jsonify({'success': False, 'message': f'Food with ID {food_id} not found'}), 404
        
        # Calculate differences
        if len(comparisons) == 2:
            nutrition_diff = {}
            for key in comparisons[0]['nutrition'].keys():
                nutrition_diff[key] = comparisons[1]['nutrition'][key] - comparisons[0]['nutrition'][key]
            
            return jsonify({
                'success': True,
                'data': {
                    'foods': comparisons,
                    'differences': nutrition_diff
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Unable to compare foods'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/meal-plan', methods=['POST'])
def generate_meal_plan():
    """Generate a personalized meal plan based on health conditions"""
    try:
        data = request.get_json()
        if not data or 'health_conditions' not in data:
            return jsonify({'success': False, 'message': 'Health conditions required'}), 400
        
        health_conditions = data['health_conditions']
        meal_count = data.get('meal_count', 3)  # breakfast, lunch, dinner
        
        # Get safe foods for the health conditions
        placeholders = ','.join(['?' for _ in health_conditions])
        condition_query = f"""
        SELECT condition_id FROM health_conditions 
        WHERE condition_code IN ({placeholders})
        """
        condition_results = db.execute_query(condition_query, tuple(health_conditions))
        
        if not condition_results:
            return jsonify({'success': False, 'message': 'Invalid health conditions'}), 400
        
        condition_ids = [str(result[0]) for result in condition_results]
        
        # Get recommended foods by category
        rec_placeholders = ','.join(['?' for _ in condition_ids])
        query = f"""
        SELECT DISTINCT fi.food_id, fi.food_name, fc.category_name, fi.image_path,
               fr.safety_score, nf.calories, nf.protein_g, nf.carbs_g
        FROM food_items fi
        JOIN food_categories fc ON fi.category_id = fc.category_id
        JOIN nutrition_facts nf ON fi.food_id = nf.food_id
        JOIN food_recommendations fr ON fi.food_id = fr.food_id
        WHERE fr.condition_id IN ({rec_placeholders}) 
              AND fr.recommendation_type IN ('Highly Recommended', 'Recommended')
              AND fr.safety_score >= 7
        ORDER BY fr.safety_score DESC
        """
        
        safe_foods = db.execute_query(query, tuple(condition_ids))
        
        if safe_foods:
            # Group foods by category
            foods_by_category = {}
            for food in safe_foods:
                category = food[2]
                if category not in foods_by_category:
                    foods_by_category[category] = []
                foods_by_category[category].append({
                    'id': food[0],
                    'name': food[1],
                    'category': food[2],
                    'image_path': food[3],
                    'safety_score': food[4],
                    'calories': float(food[5]) if food[5] else 0,
                    'protein': float(food[6]) if food[6] else 0,
                    'carbs': float(food[7]) if food[7] else 0
                })
            
            # Generate meal plan
            meal_plan = []
            meal_types = ['Breakfast', 'Lunch', 'Dinner']
            
            for i in range(min(meal_count, len(meal_types))):
                meal = {
                    'meal_type': meal_types[i],
                    'foods': [],
                    'total_calories': 0
                }
                
                # Try to include a protein and a side
                protein_categories = ['Protein', 'Seafood', 'Meat']
                side_categories = ['Vegetarian', 'Indian']
                drink_categories = ['Drink']
                
                # Add protein if available
                for cat in protein_categories:
                    if cat in foods_by_category and foods_by_category[cat]:
                        protein = foods_by_category[cat][0]  # Get highest scored
                        meal['foods'].append(protein)
                        meal['total_calories'] += protein['calories']
                        break
                
                # Add side if available
                for cat in side_categories:
                    if cat in foods_by_category and foods_by_category[cat]:
                        side = foods_by_category[cat][0]
                        meal['foods'].append(side)
                        meal['total_calories'] += side['calories']
                        break
                
                # Add drink if available
                for cat in drink_categories:
                    if cat in foods_by_category and foods_by_category[cat]:
                        drink = foods_by_category[cat][0]
                        meal['foods'].append(drink)
                        meal['total_calories'] += drink['calories']
                        break
                
                meal_plan.append(meal)
            
            return jsonify({'success': True, 'data': meal_plan})
        else:
            return jsonify({'success': False, 'message': 'No safe foods found for the provided conditions'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/allergen-filter', methods=['POST'])
def filter_by_allergens():
    """Filter foods by excluding specified allergens"""
    try:
        data = request.get_json()
        if not data or 'exclude_allergens' not in data:
            return jsonify({'success': False, 'message': 'Allergens to exclude required'}), 400
        
        exclude_allergens = data['exclude_allergens']
        if not isinstance(exclude_allergens, list):
            return jsonify({'success': False, 'message': 'Allergens must be provided as a list'}), 400
        
        if len(exclude_allergens) == 0:
            # If no allergens to exclude, return all foods
            return get_foods()
        
        # Get foods that don't contain the specified allergens
        placeholders = ','.join(['?' for _ in exclude_allergens])
        query = f"""
        SELECT DISTINCT fi.food_id, fi.food_name, fc.category_name, fi.description,
               fi.image_path, nf.calories, nf.protein_g, nf.carbs_g, nf.fat_g, nf.sodium_mg
        FROM food_items fi
        JOIN food_categories fc ON fi.category_id = fc.category_id
        LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
        WHERE fi.food_id NOT IN (
            SELECT DISTINCT fa.food_id
            FROM food_allergens fa
            JOIN allergens a ON fa.allergen_id = a.allergen_id
            WHERE a.allergen_name IN ({placeholders})
        )
        ORDER BY fi.food_name
        """
        
        safe_foods = db.execute_query(query, tuple(exclude_allergens))
        
        if safe_foods:
            result = []
            for food in safe_foods:
                result.append({
                    'id': food[0],
                    'name': food[1],
                    'category': food[2],
                    'description': food[3],
                    'image_path': food[4],
                    'nutrition': {
                        'calories': float(food[5]) if food[5] else 0,
                        'protein': float(food[6]) if food[6] else 0,
                        'carbs': float(food[7]) if food[7] else 0,
                        'fat': float(food[8]) if food[8] else 0,
                        'sodium': float(food[9]) if food[9] else 0
                    }
                })
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'message': 'No safe foods found after allergen filtering'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)