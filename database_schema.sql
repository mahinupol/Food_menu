-- Smart Digital Food Menu Database Schema
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
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS food_categories;

-- Create Users table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    height_cm DECIMAL(5,2),
    weight_kg DECIMAL(5,2),
    activity_level ENUM('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extremely Active'),
    dietary_preference ENUM('None', 'Vegetarian', 'Vegan', 'Pescatarian', 'Keto', 'Paleo'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create Food Categories table
CREATE TABLE food_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Health Conditions table
CREATE TABLE health_conditions (
    condition_id INT PRIMARY KEY AUTO_INCREMENT,
    condition_name VARCHAR(100) UNIQUE NOT NULL,
    condition_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    dietary_restrictions TEXT,
    foods_to_avoid TEXT,
    recommended_foods TEXT,
    severity_levels ENUM('Mild', 'Moderate', 'Severe'),
    icon_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Food Items table
CREATE TABLE food_items (
    food_id INT PRIMARY KEY AUTO_INCREMENT,
    food_name VARCHAR(100) NOT NULL,
    category_id INT,
    description TEXT,
    image_path VARCHAR(255),
    serving_size VARCHAR(50),
    serving_unit VARCHAR(20),
    preparation_method VARCHAR(100),
    origin_cuisine VARCHAR(50),
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_vegan BOOLEAN DEFAULT FALSE,
    is_gluten_free BOOLEAN DEFAULT FALSE,
    is_dairy_free BOOLEAN DEFAULT FALSE,
    glycemic_index INT,
    cost_category ENUM('Budget', 'Moderate', 'Premium'),
    availability ENUM('Common', 'Seasonal', 'Rare'),
    shelf_life_days INT,
    storage_requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES food_categories(category_id)
);

-- Create Nutrition Facts table
CREATE TABLE nutrition_facts (
    nutrition_id INT PRIMARY KEY AUTO_INCREMENT,
    food_id INT,
    calories DECIMAL(7,2),
    protein_g DECIMAL(6,2),
    carbs_g DECIMAL(6,2),
    fat_g DECIMAL(6,2),
    saturated_fat_g DECIMAL(6,2),
    trans_fat_g DECIMAL(6,2),
    cholesterol_mg DECIMAL(6,2),
    sodium_mg DECIMAL(7,2),
    potassium_mg DECIMAL(7,2),
    fiber_g DECIMAL(6,2),
    sugar_g DECIMAL(6,2),
    vitamin_a_iu DECIMAL(8,2),
    vitamin_c_mg DECIMAL(6,2),
    calcium_mg DECIMAL(7,2),
    iron_mg DECIMAL(6,2),
    vitamin_d_iu DECIMAL(8,2),
    vitamin_b12_mcg DECIMAL(6,2),
    folate_mcg DECIMAL(6,2),
    omega3_g DECIMAL(6,3),
    antioxidants_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE
);

-- Create Allergens table
CREATE TABLE allergens (
    allergen_id INT PRIMARY KEY AUTO_INCREMENT,
    allergen_name VARCHAR(50) UNIQUE NOT NULL,
    allergen_code VARCHAR(10) UNIQUE NOT NULL,
    description TEXT,
    severity_warning TEXT,
    alternative_ingredients TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Food Allergens junction table
CREATE TABLE food_allergens (
    food_allergen_id INT PRIMARY KEY AUTO_INCREMENT,
    food_id INT,
    allergen_id INT,
    severity_level ENUM('Contains', 'May Contain', 'Traces'),
    notes TEXT,
    FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(allergen_id),
    UNIQUE KEY unique_food_allergen (food_id, allergen_id)
);

-- Create User Health Conditions junction table
CREATE TABLE user_health_conditions (
    user_condition_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    condition_id INT,
    severity ENUM('Mild', 'Moderate', 'Severe'),
    diagnosed_date DATE,
    is_primary BOOLEAN DEFAULT FALSE,
    medication_affected BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (condition_id) REFERENCES health_conditions(condition_id),
    UNIQUE KEY unique_user_condition (user_id, condition_id)
);

-- Create Food Recommendations table
CREATE TABLE food_recommendations (
    recommendation_id INT PRIMARY KEY AUTO_INCREMENT,
    food_id INT,
    condition_id INT,
    recommendation_type ENUM('Highly Recommended', 'Recommended', 'Caution', 'Avoid'),
    safety_score INT CHECK (safety_score BETWEEN 1 AND 10),
    reasoning TEXT,
    portion_recommendation VARCHAR(100),
    frequency_recommendation VARCHAR(100),
    preparation_notes TEXT,
    created_by VARCHAR(100),
    approved_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE,
    FOREIGN KEY (condition_id) REFERENCES health_conditions(condition_id),
    UNIQUE KEY unique_food_condition (food_id, condition_id)
);

-- Create User Meal Plans table
CREATE TABLE user_meal_plans (
    meal_plan_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    plan_name VARCHAR(100),
    plan_date DATE,
    meal_type ENUM('Breakfast', 'Lunch', 'Dinner', 'Snack'),
    food_id INT,
    portion_size DECIMAL(6,2),
    portion_unit VARCHAR(20),
    calories_consumed DECIMAL(7,2),
    notes TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES food_items(food_id)
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_food_items_category ON food_items(category_id);
CREATE INDEX idx_food_items_name ON food_items(food_name);
CREATE INDEX idx_nutrition_food ON nutrition_facts(food_id);
CREATE INDEX idx_user_conditions_user ON user_health_conditions(user_id);
CREATE INDEX idx_user_conditions_condition ON user_health_conditions(condition_id);
CREATE INDEX idx_recommendations_food ON food_recommendations(food_id);
CREATE INDEX idx_recommendations_condition ON food_recommendations(condition_id);
CREATE INDEX idx_meal_plans_user_date ON user_meal_plans(user_id, plan_date);
CREATE INDEX idx_food_allergens_food ON food_allergens(food_id);
CREATE INDEX idx_food_allergens_allergen ON food_allergens(allergen_id);

-- Create views for common queries
CREATE VIEW user_health_profile AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    u.first_name,
    u.last_name,
    GROUP_CONCAT(hc.condition_name SEPARATOR ', ') as health_conditions,
    GROUP_CONCAT(uhc.severity SEPARATOR ', ') as severities
FROM users u
LEFT JOIN user_health_conditions uhc ON u.user_id = uhc.user_id
LEFT JOIN health_conditions hc ON uhc.condition_id = hc.condition_id
WHERE u.is_active = TRUE
GROUP BY u.user_id;

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
    GROUP_CONCAT(DISTINCT a.allergen_name SEPARATOR ', ') as allergens,
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