/**
 * FlavorFit Food Validation System
 * Sorts and validates foods according to disease conditions
 */

class FoodValidator {
  constructor(foodData) {
    this.foodData = foodData || {};
    this.validationStatus = {
      safe: { color: '#10b981', icon: 'fa-check-circle', label: 'Safe' },
      caution: { color: '#f59e0b', icon: 'fa-exclamation-circle', label: 'Caution' },
      avoid: { color: '#ef4444', icon: 'fa-times-circle', label: 'Avoid' }
    };
  }

  /**
   * Get validation status for a food and disease
   */
  getValidation(foodId, disease) {
    if (this.foodData.foods && this.foodData.foods[foodId]) {
      const food = this.foodData.foods[foodId];
      if (food.validation && food.validation[disease]) {
        return food.validation[disease];
      }
    }
    return { status: 'unknown', reason: 'No data available' };
  }

  /**
   * Filter foods by disease(s)
   */
  filterFoodsByDiseases(diseases) {
    if (!Array.isArray(diseases) || diseases.length === 0) {
      return null;
    }

    const result = {};

    diseases.forEach(disease => {
      const safe = [];
      const caution = [];
      const avoid = [];

      for (const [foodId, food] of Object.entries(this.foodData.foods || {})) {
        const validation = this.getValidation(foodId, disease);
        const foodInfo = {
          id: foodId,
          name: food.name,
          price: food.price,
          ...validation
        };

        if (validation.status === 'safe') {
          safe.push(foodInfo);
        } else if (validation.status === 'caution') {
          caution.push(foodInfo);
        } else {
          avoid.push(foodInfo);
        }
      }

      result[disease] = { safe, caution, avoid };
    });

    return result;
  }

  /**
   * Sort foods by rating/score for a disease
   */
  sortFoodsByDisease(disease) {
    const foods = [];

    for (const [foodId, food] of Object.entries(this.foodData.foods || {})) {
      const validation = this.getValidation(foodId, disease);
      foods.push({
        id: foodId,
        name: food.name,
        price: food.price,
        ...validation,
        ...food
      });
    }

    // Sort by status (safe first) then by availability
    const statusOrder = { safe: 0, caution: 1, avoid: 2, unknown: 3 };
    foods.sort((a, b) => {
      const statusDiff = statusOrder[a.status] - statusOrder[b.status];
      if (statusDiff !== 0) return statusDiff;
      return a.name.localeCompare(b.name);
    });

    return foods;
  }

  /**
   * Get nutritional info for a food
   */
  getNutrition(foodId) {
    const food = this.foodData.foods?.[foodId];
    if (!food) return null;

    return {
      name: food.name,
      price: food.price,
      calories: food.calories,
      protein: food.protein_g,
      carbs: food.carbs_g,
      fat: food.fat_g,
      fiber: food.fiber_g,
      sodium: food.sodium_mg,
      sugar: food.sugar_g,
      gluten: food.gluten,
      lactose: food.lactose
    };
  }

  /**
   * Get badge HTML for validation status
   */
  getBadgeHtml(status) {
    const statusInfo = this.validationStatus[status] || this.validationStatus.unknown;
    return `<span class="badge" style="background-color: ${statusInfo.color}; font-size: 0.85rem; padding: 6px 10px; border-radius: 20px;">
      <i class="fas ${statusInfo.icon} me-1"></i>${statusInfo.label}
    </span>`;
  }

  /**
   * Get food recommendation card HTML
   */
  getFoodCardHtml(foodId, disease) {
    const food = this.foodData.foods?.[foodId];
    if (!food) return '';

    const validation = this.getValidation(foodId, disease);
    const statusInfo = this.validationStatus[validation.status] || this.validationStatus.unknown;

    return `
      <div class="food-validation-card">
        <div class="food-header">
          <h5>${food.name}</h5>
          <span class="badge" style="background-color: ${statusInfo.color}; color: white;">
            <i class="fas ${statusInfo.icon}"></i> ${validation.status.charAt(0).toUpperCase() + validation.status.slice(1)}
          </span>
        </div>
        <div class="food-info">
          <p class="reason"><strong>${validation.reason}</strong></p>
          <div class="nutrition-mini">
            <span><i class="fas fa-flame"></i> ${food.calories} cal</span>
            <span><i class="fas fa-salt"></i> ${food.sodium_mg}mg Na</span>
            <span><i class="fas fa-cube"></i> ${food.protein_g}g Protein</span>
          </div>
          <p class="price" style="font-size: 1.2rem; color: #43a047; margin-top: 10px;">$${food.price.toFixed(2)}</p>
        </div>
      </div>
    `;
  }

  /**
   * Generate comparison table for all foods and a disease
   */
  getComparisonTableHtml(disease) {
    const sorted = this.sortFoodsByDisease(disease);
    let html = `<table class="table table-hover">
      <thead class="table-light">
        <tr>
          <th>Food</th>
          <th>Status</th>
          <th>Reason</th>
          <th>Calories</th>
          <th>Sodium (mg)</th>
          <th>Protein (g)</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>`;

    sorted.forEach(food => {
      const statusInfo = this.validationStatus[food.status];
      html += `<tr style="border-left: 4px solid ${statusInfo.color};">
        <td><strong>${food.name}</strong></td>
        <td><span class="badge" style="background-color: ${statusInfo.color};">${food.status}</span></td>
        <td>${food.reason}</td>
        <td>${food.calories}</td>
        <td>${food.sodium_mg}</td>
        <td>${food.protein_g}</td>
        <td>$${food.price.toFixed(2)}</td>
      </tr>`;
    });

    html += `</tbody></table>`;
    return html;
  }
}

// Initialize validator when food data is loaded
let foodValidator = null;

async function initializeFoodValidator() {
  try {
    const response = await fetch('./food_validation_data.json');
    const data = await response.json();
    foodValidator = new FoodValidator(data);
    console.log('Food validator initialized successfully');
    return true;
  } catch (error) {
    console.error('Failed to load food validation data:', error);
    return false;
  }
}

// Helper function to display sorted foods
function displayValidatedFoods(diseases, containerId) {
  if (!foodValidator) {
    console.error('Food validator not initialized');
    return;
  }

  const container = document.getElementById(containerId);
  if (!container) return;

  const filtered = foodValidator.filterFoodsByDiseases(diseases);
  let html = '';

  diseases.forEach(disease => {
    const foods = filtered[disease];
    html += `
      <div class="disease-foods mb-4">
        <h4>${disease.charAt(0).toUpperCase() + disease.slice(1)}</h4>
        <div class="row">
          <div class="col-md-4">
            <h6 class="text-success"><i class="fas fa-check-circle"></i> Safe (${foods.safe.length})</h6>
            ${foods.safe.map(f => `<div class="food-item mb-2">✓ ${f.name} - $${f.price}</div>`).join('')}
          </div>
          <div class="col-md-4">
            <h6 class="text-warning"><i class="fas fa-exclamation-circle"></i> Caution (${foods.caution.length})</h6>
            ${foods.caution.map(f => `<div class="food-item mb-2">⚠ ${f.name} - $${f.price}</div>`).join('')}
          </div>
          <div class="col-md-4">
            <h6 class="text-danger"><i class="fas fa-times-circle"></i> Avoid (${foods.avoid.length})</h6>
            ${foods.avoid.map(f => `<div class="food-item mb-2">✗ ${f.name} - $${f.price}</div>`).join('')}
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { FoodValidator, initializeFoodValidator, displayValidatedFoods };
}
