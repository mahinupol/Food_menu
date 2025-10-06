#!/usr/bin/env python3
"""
script for Smart Digital Food Menu Database

"""

import requests
import json
import time
from database_config import DatabaseOperations

def test_database_direct():
    """Test database operations directly"""
    print("=" * 60)
    print("TESTING DATABASE OPERATIONS DIRECTLY")
    print("=" * 60)
    
    db = DatabaseOperations()
    
    # Test 1: Get all health conditions
    print("\n1. Testing health conditions query...")
    conditions = db.execute_query("SELECT condition_name, condition_code FROM health_conditions")
    if conditions:
        print(f"✓ Found {len(conditions)} health conditions:")
        for condition in conditions:
            print(f"   - {condition[0]} ({condition[1]})")
    else:
        print("✗ No health conditions found")
    
    # Test 2: Get all food categories
    print("\n2. Testing food categories query...")
    categories = db.execute_query("SELECT category_name FROM food_categories")
    if categories:
        print(f"✓ Found {len(categories)} food categories:")
        for category in categories:
            print(f"   - {category[0]}")
    else:
        print("✗ No food categories found")
    
    # Test 3: Get foods with nutrition info
    print("\n3. Testing foods with nutrition query...")
    foods_query = """
    SELECT fi.food_name, fc.category_name, nf.calories, nf.protein_g
    FROM food_items fi
    JOIN food_categories fc ON fi.category_id = fc.category_id
    LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
    LIMIT 5
    """
    foods = db.execute_query(foods_query)
    if foods:
        print(f"✓ Found foods with nutrition data:")
        for food in foods:
            print(f"   - {food[0]} ({food[1]}): {food[2] or 'N/A'} cal, {food[3] or 'N/A'}g protein")
    else:
        print("✗ No foods found")
    
    # Test 4: Get recommendations for diabetes
    print("\n4. Testing diabetes recommendations...")
    diabetes_query = """
    SELECT fi.food_name, fr.recommendation_type, fr.safety_score
    FROM food_items fi
    JOIN food_recommendations fr ON fi.food_id = fr.food_id
    JOIN health_conditions hc ON fr.condition_id = hc.condition_id
    WHERE hc.condition_code = 'DM'
    ORDER BY fr.safety_score DESC
    LIMIT 5
    """
    diabetes_recs = db.execute_query(diabetes_query)
    if diabetes_recs:
        print(f"✓ Found diabetes recommendations:")
        for rec in diabetes_recs:
            print(f"   - {rec[0]}: {rec[1]} (Score: {rec[2]})")
    else:
        print("✗ No diabetes recommendations found")
    
    # Test 5: Test allergen information
    print("\n5. Testing allergen information...")
    allergen_query = """
    SELECT fi.food_name, a.allergen_name, fa.severity_level
    FROM food_items fi
    JOIN food_allergens fa ON fi.food_id = fa.food_id
    JOIN allergens a ON fa.allergen_id = a.allergen_id
    LIMIT 5
    """
    allergens = db.execute_query(allergen_query)
    if allergens:
        print(f"✓ Found allergen information:")
        for allergen in allergens:
            print(f"   - {allergen[0]} contains {allergen[1]} ({allergen[2]})")
    else:
        print("✗ No allergen information found")
    
    db.close()
    print("\n✓ Direct database tests completed")

def test_api_endpoints():
    """Test API endpoints"""
    print("\n" + "=" * 60)
    print("TESTING API ENDPOINTS")
    print("=" * 60)
    
    base_url = "http://localhost:5000/api"
    
    # Test if API server is running
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✓ API server is running")
    except requests.exceptions.RequestException:
        print("✗ API server is not running. Please start it with: python food_menu_api.py")
        return False
    
    # Test 1: Get health conditions
    print("\n1. Testing GET /health-conditions...")
    try:
        response = requests.get(f"{base_url}/health-conditions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✓ Retrieved {len(data['data'])} health conditions")
                for condition in data['data'][:3]:  # Show first 3
                    print(f"   - {condition['name']} ({condition['code']})")
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"✗ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test 2: Get foods
    print("\n2. Testing GET /foods...")
    try:
        response = requests.get(f"{base_url}/foods", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✓ Retrieved {len(data['data'])} food items")
                for food in data['data'][:3]:  # Show first 3
                    nutrition = food['nutrition']
                    print(f"   - {food['name']}: {nutrition['calories']} cal")
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"✗ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test 3: Get food recommendations
    print("\n3. Testing POST /food-recommendations...")
    try:
        payload = {
            "health_conditions": ["DM", "HTN"]  # Diabetes and Hypertension
        }
        response = requests.post(
            f"{base_url}/food-recommendations", 
            json=payload, 
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                recommendations = data['data']
                print(f"✓ Retrieved personalized recommendations:")
                print(f"   - Highly Recommended: {len(recommendations.get('highly_recommended', []))}")
                print(f"   - Recommended: {len(recommendations.get('recommended', []))}")
                print(f"   - Caution: {len(recommendations.get('caution', []))}")
                print(f"   - Avoid: {len(recommendations.get('avoid', []))}")
                
                # Show some examples
                if recommendations.get('highly_recommended'):
                    print("   Top recommendations:")
                    for food in recommendations['highly_recommended'][:2]:
                        print(f"     • {food['name']} (Score: {food['safety_score']})")
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"✗ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test 4: Generate meal plan
    print("\n4. Testing POST /meal-plan...")
    try:
        payload = {
            "health_conditions": ["DM"],  # Diabetes only
            "meal_count": 3
        }
        response = requests.post(
            f"{base_url}/meal-plan", 
            json=payload, 
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                meal_plan = data['data']
                print(f"✓ Generated meal plan with {len(meal_plan)} meals:")
                for meal in meal_plan:
                    food_names = [food['name'] for food in meal['foods']]
                    print(f"   - {meal['meal_type']}: {', '.join(food_names)} ({meal['total_calories']} cal)")
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"✗ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test 5: Allergen filtering
    print("\n5. Testing POST /allergen-filter...")
    try:
        payload = {
            "exclude_allergens": ["gluten", "dairy"]
        }
        response = requests.post(
            f"{base_url}/allergen-filter", 
            json=payload, 
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                safe_foods = data['data']
                print(f"✓ Found {len(safe_foods)} foods without gluten or dairy")
                for food in safe_foods[:3]:  # Show first 3
                    print(f"   - {food['name']} ({food['category']})")
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"✗ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    print("\n✓ API endpoint tests completed")
    return True

def test_integration_scenarios():
    """Test real-world integration scenarios"""
    print("\n" + "=" * 60)
    print("TESTING INTEGRATION SCENARIOS")
    print("=" * 60)
    
    base_url = "http://localhost:5000/api"
    
    # Scenario 1: User with diabetes selects foods
    print("\n📋 Scenario 1: Diabetes patient selecting breakfast")
    try:
        # Get recommendations for diabetes
        response = requests.post(
            f"{base_url}/food-recommendations",
            json={"health_conditions": ["DM"]},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                recommended = data['data'].get('highly_recommended', [])
                avoided = data['data'].get('avoid', [])
                
                print(f"✓ Diabetes-safe foods: {len(recommended)}")
                if recommended:
                    print("   Safe breakfast options:")
                    for food in recommended[:3]:
                        print(f"     • {food['name']} - {food['reasoning']}")
                
                print(f"✓ Foods to avoid: {len(avoided)}")
                if avoided:
                    print("   Foods to avoid:")
                    for food in avoided[:2]:
                        print(f"     • {food['name']} - {food['reasoning']}")
        
    except Exception as e:
        print(f"✗ Scenario 1 failed: {e}")
    
    # Scenario 2: User with multiple conditions
    print("\n📋 Scenario 2: User with diabetes and hypertension")
    try:
        response = requests.post(
            f"{base_url}/food-recommendations",
            json={"health_conditions": ["DM", "HTN"]},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                highly_rec = data['data'].get('highly_recommended', [])
                print(f"✓ Foods safe for both conditions: {len(highly_rec)}")
                if highly_rec:
                    print("   Best options:")
                    for food in highly_rec[:3]:
                        nutrition = food['nutrition']
                        print(f"     • {food['name']}: {nutrition['calories']} cal, {nutrition['sodium']}mg sodium")
        
    except Exception as e:
        print(f"✗ Scenario 2 failed: {e}")
    
    # Scenario 3: Vegetarian with celiac disease
    print("\n📋 Scenario 3: Vegetarian with celiac disease avoiding dairy")
    try:
        # First get celiac-safe foods
        rec_response = requests.post(
            f"{base_url}/food-recommendations",
            json={"health_conditions": ["CD"]},
            timeout=5
        )
        
        # Then filter out dairy
        filter_response = requests.post(
            f"{base_url}/allergen-filter",
            json={"exclude_allergens": ["dairy"]},
            timeout=5
        )
        
        if rec_response.status_code == 200 and filter_response.status_code == 200:
            rec_data = rec_response.json()
            filter_data = filter_response.json()
            
            if rec_data['success'] and filter_data['success']:
                celiac_safe = rec_data['data'].get('highly_recommended', [])
                dairy_free = filter_data['data']
                
                # Find foods that are both celiac-safe and dairy-free
                safe_foods = []
                celiac_food_names = {food['name'] for food in celiac_safe}
                
                for food in dairy_free:
                    if food['name'] in celiac_food_names:
                        safe_foods.append(food)
                
                print(f"✓ Celiac-safe, dairy-free foods: {len(safe_foods)}")
                for food in safe_foods[:3]:
                    print(f"     • {food['name']} ({food['category']})")
        
    except Exception as e:
        print(f"✗ Scenario 3 failed: {e}")
    
    print("\n✓ Integration scenario tests completed")

def main():
    """Run all tests"""
    print("🧪 SMART DIGITAL FOOD MENU DATABASE TESTS")
    print("Starting comprehensive database and API testing...\n")
    
    # Test 1: Direct database operations
    test_database_direct()
    
    # Test 2: API endpoints
    api_success = test_api_endpoints()
    
    # Test 3: Integration scenarios (only if API is working)
    if api_success:
        test_integration_scenarios()
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Integrate these API endpoints with your existing website")
    print("2. Replace static food data with dynamic API calls")
    print("3. Add user authentication and personal profiles")
    print("4. Implement meal planning features")
    print("\nExample integration:")
    print("// Replace your existing disease form submission")
    print("const selectedConditions = ['DM', 'HTN'];")
    print("const response = await fetch('/api/food-recommendations', {")
    print("    method: 'POST',")
    print("    headers: {'Content-Type': 'application/json'},")
    print("    body: JSON.stringify({health_conditions: selectedConditions})")
    print("});")
    print("const recommendations = await response.json();")

if __name__ == "__main__":
    main()