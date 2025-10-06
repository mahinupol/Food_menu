# Smart Digital Food Menu Database

A comprehensive database system for health-focused food recommendations that helps users with various health conditions make informed dietary choices.

## 📋 Overview

This database system supports a smart food recommendation platform that:
- Provides personalized food recommendations based on health conditions
- Tracks nutritional information for all food items
- Manages allergen information and dietary restrictions
- Supports meal planning and nutrition tracking
- Offers RESTful API for frontend integration

## 🗄️ Database Structure

### Core Tables

1. **users** - User profiles and basic information
2. **health_conditions** - Medical conditions and dietary guidelines
3. **food_categories** - Food classification system
4. **food_items** - Complete food database with details
5. **nutrition_facts** - Detailed nutritional information
6. **allergens** - Allergen definitions and warnings
7. **food_allergens** - Food-allergen relationships
8. **user_health_conditions** - User medical history
9. **food_recommendations** - Health-based food safety ratings
10. **user_meal_plans** - Personal meal planning and tracking

### Key Features

- **Health Condition Support**: Diabetes, Celiac Disease, Hypertension, Chronic Kidney Disease, Lactose Intolerance, Gout, IBS
- **Comprehensive Nutrition Data**: Calories, macronutrients, vitamins, minerals
- **Allergen Management**: Common allergens with severity levels
- **Safety Scoring**: 1-10 scale for food safety based on health conditions
- **Meal Planning**: Personalized meal recommendations
- **Food Comparison**: Side-by-side nutritional comparisons

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- SQLite (included with Python) or MySQL Server

### Installation

1. **Clone or download the database files**
2. **Install Python dependencies**:
   ```bash
   pip install flask flask-cors werkzeug
   # For MySQL support (optional):
   pip install mysql-connector-python
   ```

3. **Run the setup script**:
   ```bash
   python setup_database.py
   ```

4. **Start the API server**:
   ```bash
   python food_menu_api.py
   ```

5. **Test the API**:
   ```bash
   curl http://localhost:5000/api/health-conditions
   ```

## 📊 Database Schema Details

### Health Conditions Table
```sql
CREATE TABLE health_conditions (
    condition_id INT PRIMARY KEY AUTO_INCREMENT,
    condition_name VARCHAR(100) UNIQUE NOT NULL,
    condition_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    dietary_restrictions TEXT,
    foods_to_avoid TEXT,
    recommended_foods TEXT,
    icon_path VARCHAR(255)
);
```

**Supported Conditions**:
- `DM` - Diabetes Mellitus
- `CD` - Celiac Disease  
- `HTN` - Hypertension
- `CKD` - Chronic Kidney Disease
- `LI` - Lactose Intolerance
- `GOUT` - Gout
- `IBS` - Irritable Bowel Syndrome

### Food Items Table
```sql
CREATE TABLE food_items (
    food_id INT PRIMARY KEY AUTO_INCREMENT,
    food_name VARCHAR(100) NOT NULL,
    category_id INT,
    description TEXT,
    image_path VARCHAR(255),
    serving_size VARCHAR(50),
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_vegan BOOLEAN DEFAULT FALSE,
    is_gluten_free BOOLEAN DEFAULT FALSE,
    is_dairy_free BOOLEAN DEFAULT FALSE,
    glycemic_index INT
);
```

### Nutrition Facts Table
```sql
CREATE TABLE nutrition_facts (
    nutrition_id INT PRIMARY KEY AUTO_INCREMENT,
    food_id INT,
    calories DECIMAL(7,2),
    protein_g DECIMAL(6,2),
    carbs_g DECIMAL(6,2),
    fat_g DECIMAL(6,2),
    sodium_mg DECIMAL(7,2),
    fiber_g DECIMAL(6,2),
    -- Additional vitamins and minerals...
);
```

### Food Recommendations Table
```sql
CREATE TABLE food_recommendations (
    recommendation_id INT PRIMARY KEY AUTO_INCREMENT,
    food_id INT,
    condition_id INT,
    recommendation_type ENUM('Highly Recommended', 'Recommended', 'Caution', 'Avoid'),
    safety_score INT CHECK (safety_score BETWEEN 1 AND 10),
    reasoning TEXT,
    portion_recommendation VARCHAR(100)
);
```

## 🔌 API Endpoints

### Base URL: `http://localhost:5000/api`

### Health Conditions
- `GET /health-conditions` - Get all health conditions
- Response includes condition details, dietary restrictions, and recommendations

### Food Management
- `GET /foods` - Get all foods (with optional filtering)
- `GET /foods?category=Protein` - Filter by category
- `GET /foods?search=chicken` - Search foods
- `GET /nutrition/{food_id}` - Get detailed nutrition facts

### Personalized Recommendations
- `POST /food-recommendations` - Get recommendations for health conditions
  ```json
  {
    "health_conditions": ["DM", "HTN"]
  }
  ```

### Meal Planning
- `POST /meal-plan` - Generate personalized meal plan
  ```json
  {
    "health_conditions": ["DM"],
    "meal_count": 3
  }
  ```

### Food Comparison
- `POST /compare-foods` - Compare two foods nutritionally
  ```json
  {
    "food_ids": [1, 2]
  }
  ```

### Allergen Filtering
- `POST /allergen-filter` - Filter foods by excluding allergens
  ```json
  {
    "exclude_allergens": ["gluten", "dairy"]
  }
  ```

## 📱 Frontend Integration

### JavaScript Integration Example

```javascript
// Get health conditions
async function getHealthConditions() {
    const response = await fetch('/api/health-conditions');
    const data = await response.json();
    return data.data;
}

// Get personalized recommendations
async function getRecommendations(conditions) {
    const response = await fetch('/api/food-recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            health_conditions: conditions
        })
    });
    const data = await response.json();
    return data.data;
}

// Example usage in your existing website
document.getElementById('diseaseForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const selectedConditions = getSelectedConditions(); // Your existing function
    const recommendations = await getRecommendations(selectedConditions);
    
    // Update your food display with personalized recommendations
    displayRecommendedFoods(recommendations.highly_recommended);
    displayFoodsToAvoid(recommendations.avoid);
});
```

### Updating Your Current Website

1. **Replace Static Data**: Update your `script.js` to fetch data from the API instead of using hardcoded food data

2. **Dynamic Health Conditions**: Load health conditions from the database instead of hardcoded HTML

3. **Real-time Recommendations**: Get personalized recommendations based on user selections

4. **Enhanced Nutrition Display**: Show complete nutrition facts from the database

## 🗃️ Sample Data

The database comes pre-populated with:
- **7 Health Conditions**: Diabetes, Celiac, Hypertension, Kidney Disease, Lactose Intolerance, Gout, IBS
- **13 Food Items**: Covering various categories from your website
- **Complete Nutrition Data**: Calories, macronutrients, micronutrients
- **80+ Food Recommendations**: Safety ratings for each food-condition combination
- **Allergen Information**: Common allergens with severity levels

## 🔧 Configuration

### Database Configuration
Edit `database_config.py` to modify database settings:

```python
# For SQLite (default)
DATABASE_TYPE = 'sqlite'

# For MySQL
DATABASE_TYPE = 'mysql'
MYSQL_CONFIG = {
    'host': 'localhost',
    'database': 'smart_food_menu',
    'user': 'your_username',
    'password': 'your_password'
}
```

### API Configuration
Edit `food_menu_api.py` for API settings:

```python
# Development
app.run(debug=True, host='0.0.0.0', port=5000)

# Production
app.run(debug=False, host='0.0.0.0', port=80)
```

## 📈 Advanced Queries

### Custom Views
The database includes pre-built views for common operations:

```sql
-- Get user health profile
SELECT * FROM user_health_profile WHERE user_id = 1;

-- Get comprehensive food information
SELECT * FROM comprehensive_nutrition WHERE food_name LIKE '%chicken%';

-- Get food safety matrix
SELECT * FROM food_safety_matrix WHERE condition_name = 'Diabetes';
```

### Complex Queries Examples

```sql
-- Find foods safe for multiple conditions
SELECT fi.food_name, COUNT(*) as safe_conditions
FROM food_items fi
JOIN food_recommendations fr ON fi.food_id = fr.food_id
WHERE fr.recommendation_type IN ('Highly Recommended', 'Recommended')
GROUP BY fi.food_id, fi.food_name
HAVING safe_conditions >= 3;

-- Get daily nutrition summary for a user
SELECT 
    DATE(plan_date) as date,
    SUM(calories_consumed) as total_calories,
    SUM(nf.protein_g * portion_size / 100) as total_protein
FROM user_meal_plans ump
JOIN nutrition_facts nf ON ump.food_id = nf.food_id
WHERE user_id = 1 AND plan_date >= DATE('2024-01-01')
GROUP BY DATE(plan_date);
```

## 🚀 Deployment

### Development Environment
```bash
python setup_database.py  # Choose SQLite option
python food_menu_api.py   # Start development server
```

### Production Environment
1. Set up MySQL database
2. Update configuration files
3. Use proper WSGI server (Gunicorn, uWSGI)
4. Configure reverse proxy (Nginx, Apache)
5. Set up SSL/TLS certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new food items or health conditions
4. Update recommendations based on medical research
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Integration with Existing Website

Your current website (`index.html`, `menu.html`, `diseases.html`) can be enhanced by:

1. **Dynamic Content Loading**: Replace static HTML with API-driven content
2. **Real-time Filtering**: Use API endpoints for search and filtering
3. **Personalized Recommendations**: Show user-specific food safety information
4. **Enhanced Nutrition Display**: Complete nutritional information from database
5. **Meal Planning**: Generate and save personalized meal plans

The database is designed to seamlessly integrate with your existing frontend while providing a robust, scalable backend for health-focused food recommendations.

---

**Need Help?** 
- Check the API documentation: `http://localhost:5000/` 
- Review the sample queries in `database_examples.sql`
- Test endpoints using the included test scripts

**Next Steps:**
- Integrate the API with your existing frontend
- Add more foods and health conditions
- Implement user authentication
- Add nutrition tracking features
- Build mobile app integration