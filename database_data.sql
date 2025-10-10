-
INSERT INTO food_categories (category_name, description) VALUES
('Fast Food', 'Quick service restaurant foods, typically high in calories and sodium'),
('Indian', 'Traditional Indian cuisine including curries, rice dishes, and spiced foods'),
('Italian', 'Italian cuisine including pasta, pizza, and Mediterranean dishes'),
('Protein', 'High-protein foods including meats, poultry, and protein-rich alternatives'),
('Seafood', 'Fish, shellfish, and other marine protein sources'),
('Vegetarian', 'Plant-based foods suitable for vegetarians'),
('Dessert', 'Sweet treats, baked goods, and confectionery items'),
('Drink', 'Beverages including water, tea, coffee, and other liquids'),
('Meat', 'Red meat, poultry, and processed meat products');

--  Health Conditions
INSERT INTO health_conditions (condition_name, condition_code, description, dietary_restrictions, foods_to_avoid, recommended_foods, icon_path) VALUES
('Diabetes', 'DM', 'A group of metabolic disorders characterized by high blood sugar levels', 'Low glycemic index foods, limited refined carbohydrates', 'Sugary drinks, white bread, pasta, rice, processed sweets, fruit juices', 'Non-starchy vegetables, lean proteins, whole grains in moderation, nuts, seeds, berries', 'IMG/sugar-blood-level.png'),
('Celiac Disease', 'CD', 'An autoimmune disorder triggered by gluten consumption', 'Strict gluten-free diet required', 'Wheat, barley, rye, most breads and pastas, processed foods with gluten', 'Rice, potatoes, corn, quinoa, fresh fruits and vegetables, gluten-free labeled products', 'IMG/gluten-free.png'),
('Hypertension', 'HTN', 'High blood pressure condition requiring low-sodium diet', 'Low sodium, DASH diet principles', 'High sodium foods, processed meats, canned soups, pickled foods, fast food', 'Potassium-rich foods like bananas, leafy greens, beets, low-sodium options', 'IMG/hypertension.png'),
('Chronic Kidney Disease', 'CKD', 'Progressive kidney function decline requiring protein and mineral restrictions', 'Limited protein, phosphorus, and potassium', 'High-protein foods, processed foods, high-potassium foods', 'Low-protein options, controlled portions, fresh vegetables in moderation', 'IMG/fruit.png'),
('Lactose Intolerance', 'LI', 'Inability to digest lactose, requiring dairy-free alternatives', 'Avoid lactose-containing dairy products', 'Milk, ice cream, soft cheeses, regular yogurt, creamy sauces', 'Plant-based milks, hard aged cheeses, lactose-free products, calcium-fortified foods', 'IMG/intolerant.png'),
('Gout', 'GOUT', 'Inflammatory arthritis caused by high uric acid levels', 'Low-purine diet, avoid alcohol', 'Organ meats, red meat, seafood (especially shellfish), alcohol (especially beer)', 'Low-fat dairy, plant proteins, whole grains, fruits, vegetables', 'IMG/gout.png'),
('Irritable Bowel Syndrome', 'IBS', 'Digestive disorder causing abdominal pain and altered bowel habits', 'Low-FODMAP diet may help, avoid trigger foods', 'High-FODMAP foods, caffeine, alcohol, spicy foods, fried foods', 'Soluble fiber foods, lean proteins, cooked vegetables, low-FODMAP fruits', 'IMG/hamburger.png');

-- Allergens
INSERT INTO allergens (allergen_name, allergen_code, description, severity_warning) VALUES
('Gluten', 'GLU', 'Protein found in wheat, barley, and rye', 'Can cause severe reactions in celiac disease'),
('Dairy', 'DAIRY', 'Milk proteins and lactose', 'Can cause digestive issues in lactose intolerant individuals'),
('Eggs', 'EGG', 'Chicken egg proteins', 'Common allergen, especially in children'),
('Soy', 'SOY', 'Soybean proteins', 'Common allergen, often hidden in processed foods'),
('Peanuts', 'PNUT', 'Peanut proteins', 'Can cause severe anaphylactic reactions'),
('Tree Nuts', 'NUTS', 'Various tree nut proteins', 'Can cause severe allergic reactions'),
('Fish', 'FISH', 'Fish proteins', 'Common allergen, cross-contamination possible'),
('Shellfish', 'SHELL', 'Crustacean and mollusk proteins', 'Most common adult food allergen');

-- Food Items with information
INSERT INTO food_items (food_name, category_id, description, image_path, serving_size, serving_unit, is_vegetarian, is_vegan, is_gluten_free, is_dairy_free, glycemic_index) VALUES
('Hamburger', 1, 'Classic fast food burger with beef patty, bun, lettuce, tomato', 'IMG/hamburger.png', '1', 'piece', FALSE, FALSE, FALSE, FALSE, 85),
('Vegetable Biryani', 2, 'Aromatic rice dish with mixed vegetables and spices', 'IMG/biryani.png', '1', 'cup', TRUE, TRUE, TRUE, TRUE, 45),
('Margherita Pizza', 3, 'Traditional Italian pizza with tomato sauce, mozzarella, and basil', 'IMG/pizza.png', '2', 'slices', TRUE, FALSE, FALSE, FALSE, 80),
('Grilled Chicken', 4, 'Lean chicken breast grilled without skin', 'IMG/chicken-leg.png', '100', 'grams', FALSE, FALSE, TRUE, TRUE, 0),
('Grilled Salmon', 5, 'Atlantic salmon fillet grilled with minimal seasoning', 'IMG/salmon.png', '100', 'grams', FALSE, FALSE, TRUE, TRUE, 0),
('Chocolate Cake', 7, 'Rich chocolate layer cake with frosting', 'IMG/chocolate-cake.png', '1', 'slice', TRUE, FALSE, FALSE, FALSE, 70),
('Green Tea', 8, 'Traditional green tea brewed from tea leaves', 'IMG/green-tea.png', '1', 'cup', TRUE, TRUE, TRUE, TRUE, 0),
('Lentil Soup', 6, 'Protein-rich soup made from various lentils', 'IMG/lentils.png', '1', 'cup', TRUE, TRUE, TRUE, TRUE, 35),
('Ribeye Steak', 9, 'Premium cut of beef with high fat marbling', 'IMG/steak.png', '100', 'grams', FALSE, FALSE, TRUE, TRUE, 0),
('Tandoori Chicken', 2, 'Indian-style chicken marinated in yogurt and spices', 'IMG/tandoori.png', '100', 'grams', FALSE, FALSE, TRUE, FALSE, 0),
('Grilled Turkey', 4, 'Lean turkey breast grilled without skin', 'IMG/grilled-meat.png', '100', 'grams', FALSE, FALSE, TRUE, TRUE, 0),
('Mineral Water', 8, 'Pure mineral water for hydration', 'IMG/bottle.png', '500', 'ml', TRUE, TRUE, TRUE, TRUE, 0),
('Brown Rice Bowl', 6, 'Nutritious whole grain brown rice', 'IMG/rice.png', '1', 'cup', TRUE, TRUE, TRUE, TRUE, 50);

-- Nutrition for each food item
INSERT INTO nutrition_facts (food_id, calories, protein_g, carbs_g, fat_g, saturated_fat_g, cholesterol_mg, sodium_mg, potassium_mg, fiber_g, sugar_g) VALUES
(1, 550, 25, 40, 30, 12, 75, 980, 350, 3, 5),
(2, 320, 10, 55, 8, 1.5, 0, 340, 280, 4, 3),
(3, 780, 30, 95, 28, 15, 60, 1200, 280, 4, 8),
(4, 165, 31, 0, 3.6, 1, 85, 74, 256, 0, 0),
(5, 206, 22, 0, 13, 3, 63, 59, 628, 0, 0),
(6, 352, 5, 50, 16, 10, 62, 260, 150, 2, 42),
(7, 2, 0, 0, 0, 0, 0, 0, 25, 0, 0),
(8, 230, 18, 40, 1, 0.2, 0, 500, 731, 16, 2),
(9, 420, 35, 0, 32, 14, 110, 125, 318, 0, 0),
(10, 240, 30, 2, 12, 4, 95, 520, 350, 0, 1),
(11, 189, 29, 0, 7, 2, 74, 68, 302, 0, 0),
(12, 0, 0, 0, 0, 0, 0, 5, 2, 0, 0),
(13, 216, 5, 45, 1.8, 0.4, 0, 10, 84, 3.5, 0.7);

-- Food Allergens 
INSERT INTO food_allergens (food_id, allergen_id, severity_level) VALUES
-- Hamburger 
(1, 1, 'Contains'),
(1, 4, 'Contains'),
-- Pizza 
(3, 1, 'Contains'),
(3, 2, 'Contains'),
-- Chocolate Cake 
(6, 1, 'Contains'),
(6, 2, 'Contains'),
(6, 3, 'Contains'),
-- Grilled Salmon 
(5, 7, 'Contains'),
-- Tandoori Chicken 
(10, 2, 'Contains');

--  Food Recommendations based on health conditions
INSERT INTO food_recommendations (food_id, condition_id, recommendation_type, safety_score, reasoning, portion_recommendation, frequency_recommendation) VALUES
-- Diabetes recommendations
(1, 1, 'Avoid', 2, 'High in refined carbohydrates and may cause blood sugar spikes', 'Avoid', 'Never'),
(2, 1, 'Recommended', 7, 'Complex carbohydrates with moderate glycemic index', '1/2 cup', 'Occasionally'),
(3, 1, 'Avoid', 3, 'High in refined carbs and sodium', 'Avoid', 'Rarely'),
(4, 1, 'Highly Recommended', 9, 'High protein, no carbs, helps maintain stable blood sugar', '100-150g', 'Daily'),
(5, 1, 'Highly Recommended', 9, 'High protein, omega-3 fatty acids, no carbs', '100-150g', '2-3 times per week'),
(6, 1, 'Avoid', 1, 'Very high in sugar and refined carbs', 'Avoid', 'Never'),
(7, 1, 'Highly Recommended', 10, 'No calories, no carbs, antioxidants', 'Unlimited', 'Daily'),
(8, 1, 'Recommended', 8, 'High fiber, plant protein, complex carbs', '1 cup', 'Daily'),
(9, 1, 'Caution', 5, 'High in saturated fat, portion control needed', '100g', 'Occasionally'),

-- Celiac Disease recommendations
(1, 2, 'Avoid', 1, 'Contains gluten from wheat bun', 'Avoid', 'Never'),
(2, 2, 'Highly Recommended', 10, 'Naturally gluten-free rice dish', '1 cup', 'Daily'),
(3, 2, 'Avoid', 1, 'Contains gluten from wheat flour', 'Avoid', 'Never'),
(4, 2, 'Highly Recommended', 10, 'Naturally gluten-free protein source', 'Unlimited', 'Daily'),
(5, 2, 'Highly Recommended', 10, 'Naturally gluten-free, rich in nutrients', 'Unlimited', 'Regular'),
(6, 2, 'Avoid', 1, 'Contains gluten from wheat flour', 'Avoid', 'Never'),
(7, 2, 'Highly Recommended', 10, 'Naturally gluten-free beverage', 'Unlimited', 'Daily'),

-- Hypertension recommendations
(1, 3, 'Avoid', 2, 'Very high in sodium (980mg)', 'Avoid', 'Never'),
(2, 3, 'Recommended', 8, 'Moderate sodium, rich in potassium', '1 cup', 'Daily'),
(3, 3, 'Avoid', 2, 'Very high in sodium (1200mg)', 'Avoid', 'Rarely'),
(4, 3, 'Highly Recommended', 9, 'Low sodium, high protein', 'Unlimited', 'Daily'),
(5, 3, 'Highly Recommended', 9, 'Low sodium, omega-3 fatty acids', 'Unlimited', 'Regular'),
(7, 3, 'Highly Recommended', 10, 'No sodium, antioxidants', 'Unlimited', 'Daily'),
(8, 3, 'Recommended', 7, 'Moderate sodium, high potassium and fiber', '1 cup', 'Daily'),

-- Lactose Intolerance recommendations
(2, 5, 'Highly Recommended', 10, 'Naturally dairy-free', 'Unlimited', 'Daily'),
(3, 5, 'Avoid', 2, 'Contains dairy (mozzarella cheese)', 'Avoid', 'Never'),
(4, 5, 'Highly Recommended', 10, 'Naturally dairy-free protein', 'Unlimited', 'Daily'),
(5, 5, 'Highly Recommended', 10, 'Naturally dairy-free', 'Unlimited', 'Regular'),
(6, 5, 'Avoid', 1, 'Contains dairy (milk, butter)', 'Avoid', 'Never'),
(7, 5, 'Highly Recommended', 10, 'Naturally dairy-free', 'Unlimited', 'Daily'),
(8, 5, 'Highly Recommended', 10, 'Naturally dairy-free', 'Unlimited', 'Daily'),
(10, 5, 'Avoid', 3, 'Contains dairy (yogurt marinade)', 'Avoid or dairy-free version', 'Never'),

-- Gout recommendations
(4, 6, 'Recommended', 7, 'Lean protein, moderate purine content', '100g', 'Moderate'),
(5, 6, 'Caution', 4, 'High purine content fish', '100g', 'Limited'),
(7, 6, 'Highly Recommended', 10, 'No purines, anti-inflammatory', 'Unlimited', 'Daily'),
(8, 6, 'Highly Recommended', 9, 'Plant-based protein, low purines', 'Unlimited', 'Daily'),
(9, 6, 'Avoid', 2, 'High purine red meat', 'Avoid', 'Rarely'),

-- IBS recommendations
(2, 7, 'Recommended', 7, 'Well-cooked vegetables, easy to digest', '1/2 cup', 'Daily'),
(4, 7, 'Highly Recommended', 9, 'Lean protein, easy to digest', 'Unlimited', 'Daily'),
(7, 7, 'Recommended', 8, 'May help with digestion, low caffeine', '2-3 cups', 'Daily'),
(8, 7, 'Recommended', 8, 'Soluble fiber, easy to digest when cooked', '1 cup', 'Daily'),
(12, 7, 'Highly Recommended', 10, 'Essential for hydration, no triggers', 'Unlimited', 'Daily'),
(13, 7, 'Recommended', 7, 'Complex carbs, easy to digest when cooked', '1/2 cup', 'Daily');

-- Insert sample users (for testing purposes)
INSERT INTO users (username, email, password_hash, first_name, last_name, date_of_birth, gender, height_cm, weight_kg, activity_level, dietary_preference) VALUES
('john_doe', 'john@example.com', 'hashed_password_123', 'John', 'Doe', '1985-05-15', 'Male', 175.5, 78.2, 'Moderately Active', 'None'),
('sarah_smith', 'sarah@example.com', 'hashed_password_456', 'Sarah', 'Smith', '1990-08-22', 'Female', 165.0, 65.5, 'Lightly Active', 'Vegetarian'),
('mike_johnson', 'mike@example.com', 'hashed_password_789', 'Mike', 'Johnson', '1978-12-03', 'Male', 180.0, 85.0, 'Very Active', 'None');

-- Insert sample user health conditions
INSERT INTO user_health_conditions (user_id, condition_id, severity, diagnosed_date, is_primary) VALUES
(1, 1, 'Moderate', '2020-03-15', TRUE),  --  has diabetes
(1, 3, 'Mild', '2021-01-10', FALSE),     --  also has hypertension
(2, 2, 'Severe', '2019-06-20', TRUE),    --  has celiac disease
(3, 6, 'Moderate', '2022-02-14', TRUE);  --  has gout

-- sample meal plans
INSERT INTO user_meal_plans (user_id, plan_name, plan_date, meal_type, food_id, portion_size, portion_unit, calories_consumed, is_completed) VALUES
(1, 'Diabetes-Friendly Daily Plan', '2024-01-15', 'Breakfast', 8, 1, 'cup', 230, TRUE),
(1, 'Diabetes-Friendly Daily Plan', '2024-01-15', 'Lunch', 4, 150, 'grams', 248, TRUE),
(1, 'Diabetes-Friendly Daily Plan', '2024-01-15', 'Dinner', 5, 120, 'grams', 247, FALSE),
(2, 'Gluten-Free Weekly Plan', '2024-01-15', 'Lunch', 2, 1, 'cup', 320, TRUE),
(2, 'Gluten-Free Weekly Plan', '2024-01-15', 'Dinner', 13, 0.75, 'cup', 162, TRUE);