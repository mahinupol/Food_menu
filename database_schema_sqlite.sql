-- Smart Digital Food Menu Database Schema (SQLite Compatible)
-- This database supports a health-focused food recommendation system

-- Drop existing tables if they exist
DROP TABLE IF EXISTS user_meal_plans;
DROP TABLE IF EXISTS food_recommendations;
DROP TABLE IF EXISTS user_health_conditions;
DROP TABLE IF EXISTS food_allergens;
DROP TABLE IF EXISTS allergens;
DROP TABLE IF EXISTS nutrition_facts;
DROP TABLE IF EXISTS food_items;
DROP TABLE IF EXISTS health_conditions;
DROP TABLE IF EXISTS food_categories;
-- Removed users table as we're removing login/registration feature
-- DROP TABLE IF EXISTS users;

-- Create Food Categories table
CREATE TABLE food_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Health Conditions table
CREATE TABLE health_conditions (
    condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    condition_name TEXT UNIQUE NOT NULL,
    condition_code TEXT UNIQUE NOT NULL,
    description TEXT,
    dietary_restrictions TEXT,
    foods_to_avoid TEXT,
    recommended_foods TEXT,
    severity_levels TEXT CHECK(severity_levels IN ('Mild', 'Moderate', 'Severe')),
    icon_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Food Items table
CREATE TABLE food_items (
    food_id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    category_id INTEGER,
    description TEXT,
    image_path TEXT,
    serving_size TEXT,
    serving_unit TEXT,
    preparation_method TEXT,
    origin_cuisine TEXT,
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_vegan BOOLEAN DEFAULT FALSE,
    is_gluten_free BOOLEAN DEFAULT FALSE,
    is_dairy_free BOOLEAN DEFAULT FALSE,
    glycemic_index INTEGER,
    cost_category TEXT CHECK(cost_category IN ('Budget', 'Moderate', 'Premium')),
    availability TEXT CHECK(availability IN ('Common', 'Seasonal', 'Rare')),
    shelf_life_days INTEGER,
    storage_requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES food_categories(category_id)
);

-- Create Nutrition Facts table
CREATE TABLE nutrition_facts (
    nutrition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER,
    calories REAL,
    protein_g REAL,
    carbs_g REAL,
    fat_g REAL,
    saturated_fat_g REAL,
    trans_fat_g REAL,
    cholesterol_mg REAL,
    sodium_mg REAL,
    potassium_mg REAL,
    fiber_g REAL,
    sugar_g REAL,
    vitamin_a_iu REAL,
    vitamin_c_mg REAL,
    calcium_mg REAL,
    iron_mg REAL,
    vitamin_d_iu REAL,
    vitamin_b12_mcg REAL,
    folate_mcg REAL,
    omega3_g REAL,
    antioxidants_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE
);

-- Create Allergens table
CREATE TABLE allergens (
    allergen_id INTEGER PRIMARY KEY AUTOINCREMENT,
    allergen_name TEXT UNIQUE NOT NULL,
    allergen_code TEXT UNIQUE NOT NULL,
    description TEXT,
    severity_warning TEXT,
    alternative_ingredients TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Food Allergens junction table
CREATE TABLE food_allergens (
    food_allergen_id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER,
    allergen_id INTEGER,
    severity_level TEXT CHECK(severity_level IN ('Contains', 'May Contain', 'Traces')),
    notes TEXT,
    FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(allergen_id),
    UNIQUE(food_id, allergen_id)
);

-- Create Food Recommendations table
CREATE TABLE food_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER,
    condition_id INTEGER,
    recommendation_type TEXT CHECK(recommendation_type IN ('Highly Recommended', 'Recommended', 'Caution', 'Avoid')),
    safety_score INTEGER CHECK (safety_score BETWEEN 1 AND 10),
    reasoning TEXT,
    portion_recommendation TEXT,
    frequency_recommendation TEXT,
    preparation_notes TEXT,
    created_by TEXT,
    approved_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE,
    FOREIGN KEY (condition_id) REFERENCES health_conditions(condition_id),
    UNIQUE(food_id, condition_id)
);

-- Create indexes for better performance
CREATE INDEX idx_food_items_category ON food_items(category_id);
CREATE INDEX idx_food_items_name ON food_items(food_name);
CREATE INDEX idx_nutrition_food ON nutrition_facts(food_id);
CREATE INDEX idx_recommendations_food ON food_recommendations(food_id);
CREATE INDEX idx_recommendations_condition ON food_recommendations(condition_id);
CREATE INDEX idx_food_allergens_food ON food_allergens(food_id);
CREATE INDEX idx_food_allergens_allergen ON food_allergens(allergen_id);

-- Create views for common queries
-- Updated view to remove user references
CREATE VIEW food_safety_matrix AS
SELECT 
    fi.food_id,
    fi.food_name,
    fc.category_name,
    hc.condition_name,
    fr.recommendation_type,
    fr.safety_score,
    fr.reasoning
FROM food_items fi
CROSS JOIN health_conditions hc
LEFT JOIN food_recommendations fr ON fi.food_id = fr.food_id AND hc.condition_id = fr.condition_id
LEFT JOIN food_categories fc ON fi.category_id = fc.category_id
ORDER BY fi.food_name, hc.condition_name;

CREATE VIEW comprehensive_nutrition AS
SELECT 
    fi.food_id,
    fi.food_name,
    fc.category_name,
    nf.calories,
    nf.protein_g,
    nf.carbs_g,
    nf.fat_g,
    nf.sodium_mg,
    nf.fiber_g,
    GROUP_CONCAT(DISTINCT a.allergen_name) as allergens,
    fi.is_vegetarian,
    fi.is_vegan,
    fi.is_gluten_free,
    fi.is_dairy_free
FROM food_items fi
LEFT JOIN food_categories fc ON fi.category_id = fc.category_id
LEFT JOIN nutrition_facts nf ON fi.food_id = nf.food_id
LEFT JOIN food_allergens fa ON fi.food_id = fa.food_id
LEFT JOIN allergens a ON fa.allergen_id = a.allergen_id
GROUP BY fi.food_id;