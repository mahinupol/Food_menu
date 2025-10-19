"""
FlavorFit Food Validator
Validates and sorts foods according to disease conditions using nutritional information.
"""

# Food Database with Nutritional Information (per serving)
FOOD_DATABASE = {
    "biryani": {
        "name": "Biryani",
        "price": 8.99,
        "calories": 450,
        "sodium_mg": 850,
        "sugar_g": 2,
        "protein_g": 18,
        "fiber_g": 3,
        "fat_g": 12,
        "carbs_g": 65,
        "gluten": True,
        "lactose": False,
        "purine_level": "high"  # Red meat content
    },
    "tandoori": {
        "name": "Tandoori Chicken",
        "price": 9.99,
        "calories": 280,
        "sodium_mg": 650,
        "sugar_g": 1,
        "protein_g": 35,
        "fiber_g": 0,
        "fat_g": 8,
        "carbs_g": 5,
        "gluten": False,
        "lactose": False,
        "purine_level": "medium"
    },
    "salmon": {
        "name": "Grilled Salmon",
        "price": 14.99,
        "calories": 350,
        "sodium_mg": 500,
        "sugar_g": 0,
        "protein_g": 40,
        "fiber_g": 0,
        "fat_g": 20,
        "carbs_g": 0,
        "gluten": False,
        "lactose": False,
        "purine_level": "high",
        "omega3": True
    },
    "steak": {
        "name": "Grilled Steak",
        "price": 16.99,
        "calories": 420,
        "sodium_mg": 700,
        "sugar_g": 0,
        "protein_g": 45,
        "fiber_g": 0,
        "fat_g": 25,
        "carbs_g": 0,
        "gluten": False,
        "lactose": False,
        "purine_level": "very_high"
    },
    "pizza": {
        "name": "Vegetable Pizza",
        "price": 10.99,
        "calories": 380,
        "sodium_mg": 920,
        "sugar_g": 4,
        "protein_g": 14,
        "fiber_g": 5,
        "fat_g": 14,
        "carbs_g": 52,
        "gluten": True,
        "lactose": True,
        "purine_level": "low"
    },
    "hamburger": {
        "name": "Hamburger",
        "price": 7.99,
        "calories": 520,
        "sodium_mg": 1100,
        "sugar_g": 8,
        "protein_g": 28,
        "fiber_g": 2,
        "fat_g": 28,
        "carbs_g": 48,
        "gluten": True,
        "lactose": True,
        "purine_level": "high"
    },
    "chocolate_cake": {
        "name": "Chocolate Cake",
        "price": 5.99,
        "calories": 380,
        "sodium_mg": 200,
        "sugar_g": 45,
        "protein_g": 4,
        "fiber_g": 2,
        "fat_g": 18,
        "carbs_g": 52,
        "gluten": True,
        "lactose": True,
        "purine_level": "low"
    },
    "grilled_meat": {
        "name": "Grilled Meat",
        "price": 12.99,
        "calories": 340,
        "sodium_mg": 600,
        "sugar_g": 0,
        "protein_g": 40,
        "fiber_g": 0,
        "fat_g": 18,
        "carbs_g": 0,
        "gluten": False,
        "lactose": False,
        "purine_level": "high"
    },
    "rice": {
        "name": "Rice",
        "price": 3.99,
        "calories": 206,
        "sodium_mg": 2,
        "sugar_g": 0,
        "protein_g": 4,
        "fiber_g": 0.3,
        "fat_g": 0.3,
        "carbs_g": 45,
        "gluten": False,
        "lactose": False,
        "purine_level": "low"
    },
    "lentils": {
        "name": "Lentil Curry",
        "price": 6.99,
        "calories": 230,
        "sodium_mg": 500,
        "sugar_g": 2,
        "protein_g": 18,
        "fiber_g": 8,
        "fat_g": 3,
        "carbs_g": 40,
        "gluten": False,
        "lactose": False,
        "purine_level": "medium"
    },
    "fruit": {
        "name": "Mixed Fruit Salad",
        "price": 5.49,
        "calories": 80,
        "sodium_mg": 20,
        "sugar_g": 18,
        "protein_g": 1,
        "fiber_g": 3,
        "fat_g": 0,
        "carbs_g": 21,
        "gluten": False,
        "lactose": False,
        "purine_level": "low"
    },
    "green_tea": {
        "name": "Green Tea",
        "price": 2.99,
        "calories": 2,
        "sodium_mg": 5,
        "sugar_g": 0,
        "protein_g": 0,
        "fiber_g": 0,
        "fat_g": 0,
        "carbs_g": 0,
        "gluten": False,
        "lactose": False,
        "purine_level": "low"
    },
    "bottle": {
        "name": "Water Bottle",
        "price": 1.99,
        "calories": 0,
        "sodium_mg": 0,
        "sugar_g": 0,
        "protein_g": 0,
        "fiber_g": 0,
        "fat_g": 0,
        "carbs_g": 0,
        "gluten": False,
        "lactose": False,
        "purine_level": "low"
    }
}

# Disease Validation Rules
DISEASE_RULES = {
    "diabetes": {
        "max_sugar_g": 15,
        "max_carbs_g": 50,
        "min_fiber_g": 2,
        "max_calories": 400,
        "considerations": ["high fiber", "low sugar", "lean protein"]
    },
    "celiac": {
        "gluten": False,
        "max_sodium_mg": 800,
        "min_fiber_g": 3,
        "considerations": ["gluten-free", "naturally processed"]
    },
    "hypertension": {
        "max_sodium_mg": 600,
        "max_calories": 350,
        "min_potassium": True,
        "max_fat_g": 15,
        "considerations": ["low sodium", "high potassium", "lean protein"]
    },
    "kidney": {
        "max_sodium_mg": 400,
        "max_potassium_foods": False,
        "max_protein_g": 25,
        "max_phosphorus": True,
        "considerations": ["low sodium", "moderate protein", "kidney-friendly"]
    },
    "lactose": {
        "lactose": False,
        "considerations": ["lactose-free", "dairy-free alternatives"]
    },
    "gout": {
        "purine_level": ["low", "medium"],  # Avoid high/very_high
        "max_sodium_mg": 700,
        "min_water": True,
        "considerations": ["low purine", "avoid organ meats", "lean protein"]
    },
    "ibs": {
        "min_fiber_g": 5,
        "max_fat_g": 10,
        "avoid_high_fodmap": True,
        "considerations": ["high fiber", "low fat", "easy to digest"]
    }
}

class FoodValidator:
    """Validates and sorts foods according to disease conditions."""
    
    def __init__(self):
        self.database = FOOD_DATABASE
        self.rules = DISEASE_RULES
    
    def validate_food(self, food_id: str, disease: str) -> dict:
        """
        Validate a single food against a disease condition.
        Returns: {'status': 'safe'|'caution'|'avoid', 'reason': str, 'score': int}
        """
        if food_id not in self.database:
            return {"status": "unknown", "reason": "Food not found", "score": 0}
        
        if disease not in self.rules:
            return {"status": "unknown", "reason": "Disease not found", "score": 0}
        
        food = self.database[food_id]
        rules = self.rules[disease]
        violations = []
        score = 100  # Start with perfect score
        
        # Check disease-specific rules
        if disease == "diabetes":
            if food["sugar_g"] > rules["max_sugar_g"]:
                violations.append(f"High sugar: {food['sugar_g']}g (max {rules['max_sugar_g']}g)")
                score -= 15
            if food["carbs_g"] > rules["max_carbs_g"]:
                violations.append(f"High carbs: {food['carbs_g']}g (max {rules['max_carbs_g']}g)")
                score -= 20
            if food["fiber_g"] < rules["min_fiber_g"]:
                violations.append(f"Low fiber: {food['fiber_g']}g (min {rules['min_fiber_g']}g)")
                score -= 10
            if food["calories"] > rules["max_calories"]:
                violations.append(f"High calories: {food['calories']} (max {rules['max_calories']})")
                score -= 5
        
        elif disease == "celiac":
            if food["gluten"]:
                violations.append("Contains gluten")
                score -= 50
            if food["sodium_mg"] > rules["max_sodium_mg"]:
                violations.append(f"High sodium: {food['sodium_mg']}mg (max {rules['max_sodium_mg']}mg)")
                score -= 10
            if food["fiber_g"] < rules["min_fiber_g"]:
                violations.append(f"Low fiber: {food['fiber_g']}g (min {rules['min_fiber_g']}g)")
                score -= 5
        
        elif disease == "hypertension":
            if food["sodium_mg"] > rules["max_sodium_mg"]:
                violations.append(f"High sodium: {food['sodium_mg']}mg (max {rules['max_sodium_mg']}mg)")
                score -= 25
            if food["calories"] > rules["max_calories"]:
                violations.append(f"High calories: {food['calories']} (max {rules['max_calories']})")
                score -= 10
            if food["fat_g"] > rules["max_fat_g"]:
                violations.append(f"High fat: {food['fat_g']}g (max {rules['max_fat_g']}g)")
                score -= 15
        
        elif disease == "lactose":
            if food["lactose"]:
                violations.append("Contains lactose")
                score -= 50
        
        elif disease == "gout":
            if food["purine_level"] in ["high", "very_high"]:
                violations.append(f"High purine level: {food['purine_level']}")
                score -= 30
            if food["sodium_mg"] > rules["max_sodium_mg"]:
                violations.append(f"High sodium: {food['sodium_mg']}mg (max {rules['max_sodium_mg']}mg)")
                score -= 10
        
        elif disease == "kidney":
            if food["sodium_mg"] > rules["max_sodium_mg"]:
                violations.append(f"High sodium: {food['sodium_mg']}mg (max {rules['max_sodium_mg']}mg)")
                score -= 25
            if food["protein_g"] > rules["max_protein_g"]:
                violations.append(f"High protein: {food['protein_g']}g (max {rules['max_protein_g']}g)")
                score -= 20
        
        elif disease == "ibs":
            if food["fiber_g"] < rules["min_fiber_g"]:
                violations.append(f"Low fiber: {food['fiber_g']}g (min {rules['min_fiber_g']}g)")
                score -= 10
            if food["fat_g"] > rules["max_fat_g"]:
                violations.append(f"High fat: {food['fat_g']}g (max {rules['max_fat_g']}g)")
                score -= 20
        
        # Determine status based on score
        if score >= 80:
            status = "safe"
        elif score >= 50:
            status = "caution"
        else:
            status = "avoid"
        
        reason = violations[0] if violations else "Meets dietary requirements"
        
        return {
            "status": status,
            "reason": reason,
            "score": max(0, score),
            "violations": violations
        }
    
    def get_sorted_foods(self, diseases: list) -> dict:
        """
        Get all foods sorted by safety level for each disease.
        Returns: {'disease': {'safe': [...], 'caution': [...], 'avoid': [...]}}
        """
        result = {}
        
        for disease in diseases:
            safe_foods = []
            caution_foods = []
            avoid_foods = []
            
            for food_id, food_data in self.database.items():
                validation = self.validate_food(food_id, disease)
                
                food_info = {
                    "id": food_id,
                    "name": food_data["name"],
                    "price": food_data["price"],
                    "reason": validation["reason"],
                    "score": validation["score"]
                }
                
                if validation["status"] == "safe":
                    safe_foods.append(food_info)
                elif validation["status"] == "caution":
                    caution_foods.append(food_info)
                else:
                    avoid_foods.append(food_info)
            
            # Sort by score (descending)
            safe_foods.sort(key=lambda x: x["score"], reverse=True)
            caution_foods.sort(key=lambda x: x["score"], reverse=True)
            avoid_foods.sort(key=lambda x: x["score"], reverse=True)
            
            result[disease] = {
                "safe": safe_foods,
                "caution": caution_foods,
                "avoid": avoid_foods
            }
        
        return result
    
    def get_food_info(self, food_id: str) -> dict:
        """Get detailed nutritional information for a food."""
        return self.database.get(food_id, {})
    
    def recommend_foods(self, diseases: list, max_items: int = 5) -> dict:
        """Get top recommended foods for multiple diseases."""
        sorted_foods = self.get_sorted_foods(diseases)
        recommendations = {}
        
        for disease, foods in sorted_foods.items():
            # Get safe foods, limit to max_items
            safe = foods["safe"][:max_items]
            recommendations[disease] = {
                "safe_foods": safe,
                "count": len(safe),
                "all_safe": len(foods["safe"]),
                "total_caution": len(foods["caution"]),
                "total_avoid": len(foods["avoid"])
            }
        
        return recommendations

# Export for use in other modules
def export_to_json():
    """Export food database and validation rules to JSON."""
    import json
    data = {
        "foods": FOOD_DATABASE,
        "disease_rules": DISEASE_RULES
    }
    return json.dumps(data, indent=2)

if __name__ == "__main__":
    # Example usage
    validator = FoodValidator()
    
    # Test single food validation
    print("=== Single Food Validation ===")
    result = validator.validate_food("pizza", "celiac")
    print(f"Pizza for Celiac: {result}")
    
    result = validator.validate_food("salmon", "gout")
    print(f"Salmon for Gout: {result}")
    
    # Test sorted foods
    print("\n=== Sorted Foods for Multiple Diseases ===")
    sorted_foods = validator.get_sorted_foods(["diabetes", "hypertension"])
    print(f"Diabetes - Safe foods: {len(sorted_foods['diabetes']['safe'])}")
    print(f"Hypertension - Safe foods: {len(sorted_foods['hypertension']['safe'])}")
    
    # Test recommendations
    print("\n=== Food Recommendations ===")
    recommendations = validator.recommend_foods(["diabetes", "celiac"])
    for disease, recs in recommendations.items():
        print(f"\n{disease.upper()}:")
        for food in recs["safe_foods"]:
            print(f"  - {food['name']}: {food['reason']} (score: {food['score']})")
