// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Modern Toast Notification System
    function showToast(message, type = 'info', title = 'Notification') {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) return;

        const toast = toastContainer.querySelector('#liveToast');
        const toastTitle = toast.querySelector('.toast-title');
        const toastBody = toast.querySelector('.toast-body');
        const toastIcon = toast.querySelector('.toast-icon');

        // Set content
        toastTitle.textContent = title;
        toastBody.textContent = message;

        // Set type styling
        toast.className = `toast toast-${type}`;

        // Show toast
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: 4000
        });
        bsToast.show();
    }

    // Health Condition Card Selection
    const healthCards = document.querySelectorAll('.health-card');
    healthCards.forEach(card => {
        card.addEventListener('click', function() {
            const condition = this.getAttribute('data-condition');
            
            // Find the corresponding checkbox
            const checkbox = document.getElementById(condition);
            
            if (checkbox) {
                // Toggle checkbox
                checkbox.checked = !checkbox.checked;
                
                // Update card visual state
                if (checkbox.checked) {
                    this.classList.add('selected');
                    showToast(`${this.querySelector('.health-card-title').textContent} added!`, 'success', '✓ Added');
                } else {
                    this.classList.remove('selected');
                    showToast(`${this.querySelector('.health-card-title').textContent} removed!`, 'info', '✕ Removed');
                }
                
                // Store selected condition
                localStorage.setItem('selectedCondition', condition);
            } else {
                // On homepage - redirect to diseases page
                const isDiseasesPage = window.location.pathname.includes('diseases.html');
                
                if (!isDiseasesPage) {
                    // Show toast notification
                    showToast(`${this.querySelector('.health-card-title').textContent} selected!`, 'success', '✓ Selected');
                    
                    // Store selected condition
                    localStorage.setItem('selectedCondition', condition);
                    
                    // Redirect to diseases page after a short delay
                    setTimeout(() => {
                        window.location.href = 'assets/diseases.html?condition=' + condition;
                    }, 1200);
                }
            }
        });
    });
    
    // Sync card selection state with checkboxes on page load (for diseases page)
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        if (checkbox.checked) {
            const cardElement = document.querySelector(`.health-card[data-condition="${checkbox.value}"]`);
            if (cardElement) {
                cardElement.classList.add('selected');
            }
        }
    });

    // Modern Animation System with Intersection Observer
    const animationObserverOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                animationObserver.unobserve(entry.target);
            }
        });
    }, animationObserverOptions);

    // Observe all cards for animation
    document.querySelectorAll('.animate-card, .food-item').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.8s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
        animationObserver.observe(card);
    });

    // Shopping Cart Management
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Update cart count on page load
    updateCartCount();
    
    // Add to Cart functionality
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const foodName = this.getAttribute('data-food');
            const foodPrice = parseFloat(this.getAttribute('data-price'));
            
            addToCart(foodName, foodPrice);
            
            // Visual feedback
            this.innerHTML = '<i class="fas fa-check"></i> Added!';
            this.classList.add('btn-secondary');
            this.classList.remove('btn-success');
            
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-cart-plus"></i> Add to Cart';
                this.classList.add('btn-success');
                this.classList.remove('btn-secondary');
            }, 1500);
        });
    });
    
    // Buy Now functionality
    document.querySelectorAll('.buy-now-btn').forEach(button => {
        button.addEventListener('click', function() {
            const foodName = this.getAttribute('data-food');
            const foodPrice = parseFloat(this.getAttribute('data-price'));
            
            addToCart(foodName, foodPrice);
            
            // Show toast and redirect to checkout
            showToast(`Added ${foodName} to cart - $${foodPrice.toFixed(2)}`, 'success', 'Quick Purchase');
            setTimeout(() => {
                viewCart();
            }, 800);
        });
    });
    
    // View Cart button
    const viewCartBtn = document.getElementById('viewCartBtn');
    if (viewCartBtn) {
        viewCartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            viewCart();
        });
    }
    
    // Cart functions
    function addToCart(name, price) {
        const existingItem = cart.find(item => item.name === name);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                name: name,
                price: price,
                quantity: 1
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
    }
    
    function updateCartCount() {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        const cartCountElements = document.querySelectorAll('#cartCount');
        cartCountElements.forEach(el => {
            el.textContent = totalItems;
        });
    }
    
    function viewCart() {
        if (cart.length === 0) {
            showToast('Your cart is empty! Add some delicious items first.', 'info', 'Empty Cart');
            return;
        }
        
        let cartHTML = '<div style="max-width: 600px;">';
        cartHTML += '<h3 style="margin-bottom: 20px;">Shopping Cart</h3>';
        cartHTML += '<table style="width: 100%; border-collapse: collapse;">';
        cartHTML += '<tr style="border-bottom: 2px solid #ddd;"><th style="text-align: left; padding: 10px;">Item</th><th style="padding: 10px;">Qty</th><th style="text-align: right; padding: 10px;">Price</th><th style="text-align: right; padding: 10px;">Total</th></tr>';
        
        let total = 0;
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            cartHTML += `<tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px;">${item.name}</td>
                <td style="text-align: center; padding: 10px;">${item.quantity}</td>
                <td style="text-align: right; padding: 10px;">$${item.price.toFixed(2)}</td>
                <td style="text-align: right; padding: 10px;">$${itemTotal.toFixed(2)}</td>
            </tr>`;
        });
        
        cartHTML += `<tr style="font-weight: bold; font-size: 1.2em;">
            <td colspan="3" style="text-align: right; padding: 15px;">Total:</td>
            <td style="text-align: right; padding: 15px;">$${total.toFixed(2)}</td>
        </tr>`;
        cartHTML += '</table>';
        cartHTML += '<div style="margin-top: 20px; display: flex; gap: 10px; justify-content: flex-end;">';
        cartHTML += '<button onclick="clearCart()" style="padding: 10px 20px; background-color: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">Clear Cart</button>';
        cartHTML += '<button onclick="checkout()" style="padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">Checkout</button>';
        cartHTML += '</div></div>';
        
        const cartModal = document.createElement('div');
        cartModal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center; z-index: 10000;';
        cartModal.innerHTML = `<div style="background: white; padding: 30px; border-radius: 10px; max-height: 80vh; overflow-y: auto;">${cartHTML}<button onclick="this.parentElement.parentElement.remove()" style="margin-top: 15px; padding: 10px 20px; background-color: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">Close</button></div>`;
        document.body.appendChild(cartModal);
    }
    
    // Global functions for cart modal
    window.clearCart = function() {
        if (confirm('Are you sure you want to clear your cart?')) {
            cart = [];
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartCount();
            document.querySelector('[style*="position: fixed"]')?.remove();
            showToast('Cart cleared successfully!', 'info', 'Cart Updated');
        }
    };
    
    window.checkout = function() {
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        showToast(`Thank you for your order! Total: $${total.toFixed(2)} - Demo checkout completed`, 'success', 'Order Placed');
        cart = [];
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        document.querySelector('[style*="position: fixed"]')?.remove();
    };
    // Disease Form Submission
    const diseaseForm = document.getElementById('diseaseForm');
    if (diseaseForm) {
        diseaseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get all checked checkboxes
            const checkedDiseases = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                .map(checkbox => checkbox.value);
            
            // Show modern notification and redirect
            if (checkedDiseases.length > 0) {
                showToast(`Filtering foods for: ${checkedDiseases.join(', ')}`, 'success', 'Health Conditions Set');
                
                // Store selected diseases in localStorage for use in menu page
                localStorage.setItem('selectedDiseases', JSON.stringify(checkedDiseases));
                
                // Redirect to menu page with smooth transition
                setTimeout(() => {
                    window.location.href = 'menu.html';
                }, 1500);
            } else {
                showToast('Please select at least one health condition to continue.', 'error', 'Selection Required');
            }
        });
    }
    
    // Contact Form Submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            // Simple validation
            if (name && email && message) {
                showToast(`Thank you for contacting us, ${name}! We'll get back to you soon.`, 'success', 'Message Sent');
                contactForm.reset();
            } else {
                showToast('Please fill in all required fields to send your message.', 'error', 'Incomplete Form');
            }
        });
    }
    
    // Food Menu Search and Filter
    const searchFood = document.getElementById('searchFood');
    const sortFood = document.getElementById('sortFood');
    const foodContainer = document.getElementById('foodContainer');
    
    if (searchFood && sortFood && foodContainer) {
        // Add search tags below search input
        const searchInputContainer = searchFood.parentElement.parentElement;
        const searchTagsDiv = document.createElement('div');
        searchTagsDiv.className = 'search-tags mt-2';
        searchTagsDiv.innerHTML = `
            <span class="search-tag" data-tag="diabetes">Diabetes</span>
            <span class="search-tag" data-tag="hypertension">Hypertension</span>
            <span class="search-tag" data-tag="celiac">Celiac</span>
            <span class="search-tag" data-tag="recommended">Recommended</span>
            <span class="search-tag" data-tag="no allergens">No Allergens</span>
        `;
        searchInputContainer.appendChild(searchTagsDiv);
        
        // Add click event to search tags
        const searchTags = document.querySelectorAll('.search-tag');
        searchTags.forEach(tag => {
            tag.addEventListener('click', function() {
                searchFood.value = this.getAttribute('data-tag');
                filterFoodItems();
            });
        });
        
        // Search functionality
        searchFood.addEventListener('input', function() {
            filterFoodItems();
        });
        
        // Sort functionality
        sortFood.addEventListener('change', function() {
            sortFoodItems();
        });
        
        // Allergen filter functionality
        const allergenCheckboxes = document.querySelectorAll('.allergen-checkbox');
        allergenCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                filterFoodItems();
            });
        });
        
        // Function to filter food items based on search input and allergens
        function filterFoodItems() {
            const searchTerm = searchFood.value.toLowerCase();
            const foodItems = document.querySelectorAll('.food-item');
            
            // Get selected allergens
            const selectedAllergens = Array.from(document.querySelectorAll('.allergen-checkbox:checked'))
                .map(checkbox => checkbox.value);
            
            foodItems.forEach(item => {
                const foodName = item.querySelector('.card-title').textContent.toLowerCase();
                const foodCategory = item.querySelector('.card-text').textContent.toLowerCase();
                const foodAllergens = item.getAttribute('data-allergens')?.split(',') || [];
                const safeFor = item.getAttribute('data-safe-for')?.split(',') || [];
                const unsafeFor = item.getAttribute('data-unsafe-for')?.split(',') || [];
                
                // Check if food contains any selected allergens
                const hasSelectedAllergen = selectedAllergens.some(allergen => 
                    foodAllergens.includes(allergen)
                );
                
                // Check if search term matches food name, category, or disease compatibility
                const matchesSearchTerm = 
                    foodName.includes(searchTerm) || 
                    foodCategory.includes(searchTerm) ||
                    (searchTerm === 'recommended' && item.querySelector('.badge.bg-success')) ||
                    (searchTerm === 'no allergens' && (foodAllergens.length === 0 || foodAllergens[0] === 'none')) ||
                    safeFor.some(disease => disease.includes(searchTerm)) ||
                    unsafeFor.some(disease => disease.includes(searchTerm));
                
                if ((matchesSearchTerm || searchTerm === '') && !hasSelectedAllergen) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
        
        // Function to sort food items
        function sortFoodItems() {
            const sortValue = sortFood.value;
            const foodItems = Array.from(document.querySelectorAll('.food-item'));
            
            // Sort based on selected option
            foodItems.sort((a, b) => {
                const nameA = a.querySelector('.card-title').textContent;
                const nameB = b.querySelector('.card-title').textContent;
                const categoryA = a.getAttribute('data-category');
                const categoryB = b.getAttribute('data-category');
                const badgeA = a.querySelector('.badge');
                const badgeB = b.querySelector('.badge');
                const isRecommendedA = badgeA && badgeA.classList.contains('bg-success');
                const isRecommendedB = badgeB && badgeB.classList.contains('bg-success');
                
                // Default sort - Recommended items first
                if (sortValue === 'default' || !sortValue) {
                    if (isRecommendedA && !isRecommendedB) return -1;
                    if (!isRecommendedA && isRecommendedB) return 1;
                    return nameA.localeCompare(nameB);
                } else if (sortValue === 'name') {
                    return nameA.localeCompare(nameB);
                } else if (sortValue === 'nameDesc') {
                    return nameB.localeCompare(nameA);
                } else if (sortValue === 'category') {
                    return categoryA.localeCompare(categoryB);
                } else if (sortValue === 'recommended') {
                    if (isRecommendedA && !isRecommendedB) return -1;
                    if (!isRecommendedA && isRecommendedB) return 1;
                    return nameA.localeCompare(nameB);
                }
                
                return 0;
            });
            
            // Reappend sorted items
            foodItems.forEach(item => {
                foodContainer.appendChild(item);
            });
        }
        
        // Sort by recommended items first by default when page loads
        sortFoodItems();
        
        // Check if there are selected diseases in localStorage
        const selectedDiseases = JSON.parse(localStorage.getItem('selectedDiseases')) || [];
        
        if (selectedDiseases.length > 0) {
            // Show disease icons based on selected diseases
            const foodItems = document.querySelectorAll('.food-item');
            
            foodItems.forEach(item => {
                const diseaseIcons = item.querySelectorAll('.disease-icon');
                const unsafeFor = item.getAttribute('data-unsafe-for')?.split(',') || [];
                
                // Only show icons for selected diseases
                diseaseIcons.forEach(icon => {
                    const diseaseClass = Array.from(icon.classList).find(cls => 
                        cls !== 'disease-icon'
                    );
                    
                    if (diseaseClass && selectedDiseases.includes(diseaseClass)) {
                        icon.style.display = 'inline-flex';
                    } else {
                        icon.style.display = 'none';
                    }
                });
                
                // Update badge based on compatibility with selected diseases
                const badge = item.querySelector('.badge');
                const isUnsafe = selectedDiseases.some(disease => unsafeFor.includes(disease));
                
                if (isUnsafe) {
                    badge.textContent = 'Avoid';
                    badge.classList.remove('bg-success');
                    badge.classList.add('bg-danger');
                }
            });
            
            // Generate personalized diet plan
            const recommendedSection = document.getElementById('recommendedTodaySection');
            const recommendedMeals = document.getElementById('recommendedMeals');
            
            if (recommendedSection && recommendedMeals) {
                // Find safe foods for the selected diseases
                const safeFoods = Array.from(foodItems).filter(item => {
                    const unsafeFor = item.getAttribute('data-unsafe-for')?.split(',') || [];
                    return !selectedDiseases.some(disease => unsafeFor.includes(disease));
                });
                
                if (safeFoods.length > 0) {
                    // Select a random protein, side, and drink
                    const proteins = safeFoods.filter(item => 
                        item.getAttribute('data-category') === 'Protein' || 
                        item.getAttribute('data-category') === 'Seafood' ||
                        item.getAttribute('data-category') === 'Meat'
                    );
                    
                    const sides = safeFoods.filter(item => 
                        item.getAttribute('data-category') === 'Vegetarian' || 
                        item.getAttribute('data-category') === 'Indian'
                    );
                    
                    const drinks = safeFoods.filter(item => 
                        item.getAttribute('data-category') === 'Drink'
                    );
                    
                    let mealHtml = '';
                    
                    // Add a protein if available
                    if (proteins.length > 0) {
                        const randomProtein = proteins[Math.floor(Math.random() * proteins.length)];
                        const proteinName = randomProtein.querySelector('.card-title').textContent;
                        const proteinImg = randomProtein.querySelector('img').getAttribute('src');
                        
                        mealHtml += `
                            <div class="col-md-4 mb-3">
                                <div class="card h-100">
                                    <img src="${proteinImg}" class="card-img-top food-image" alt="${proteinName}">
                                    <div class="card-body">
                                        <h6 class="card-title">${proteinName}</h6>
                                        <span class="badge bg-success">Main Course</span>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                    
                    // Add a side if available
                    if (sides.length > 0) {
                        const randomSide = sides[Math.floor(Math.random() * sides.length)];
                        const sideName = randomSide.querySelector('.card-title').textContent;
                        const sideImg = randomSide.querySelector('img').getAttribute('src');
                        
                        mealHtml += `
                            <div class="col-md-4 mb-3">
                                <div class="card h-100">
                                    <img src="${sideImg}" class="card-img-top food-image" alt="${sideName}">
                                    <div class="card-body">
                                        <h6 class="card-title">${sideName}</h6>
                                        <span class="badge bg-success">Side Dish</span>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                    
                    // Add a drink if available
                    if (drinks.length > 0) {
                        const randomDrink = drinks[Math.floor(Math.random() * drinks.length)];
                        const drinkName = randomDrink.querySelector('.card-title').textContent;
                        const drinkImg = randomDrink.querySelector('img').getAttribute('src');
                        
                        mealHtml += `
                            <div class="col-md-4 mb-3">
                                <div class="card h-100">
                                    <img src="${drinkImg}" class="card-img-top food-image" alt="${drinkName}">
                                    <div class="card-body">
                                        <h6 class="card-title">${drinkName}</h6>
                                        <span class="badge bg-success">Beverage</span>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                    
                    recommendedMeals.innerHTML = mealHtml;
                    recommendedSection.classList.remove('d-none');
                }
            }
        }
        
        // Food Comparison Tool
        const compareBtns = document.querySelectorAll('.compare-btn');
        const comparisonModal = new bootstrap.Modal(document.getElementById('comparisonModal'));
        let food1Selected = null;
        let food2Selected = null;
        
        compareBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const foodItem = this.closest('.food-item');
                const foodName = this.getAttribute('data-food');
                const foodImg = foodItem.querySelector('img').getAttribute('src');
                const calories = foodItem.getAttribute('data-calories');
                const protein = foodItem.getAttribute('data-protein');
                const carbs = foodItem.getAttribute('data-carbs');
                const fat = foodItem.getAttribute('data-fat');
                const sodium = foodItem.getAttribute('data-sodium');
                const allergens = foodItem.getAttribute('data-allergens')?.split(',') || [];
                const unsafeFor = foodItem.getAttribute('data-unsafe-for')?.split(',') || [];
                const safeFor = foodItem.getAttribute('data-safe-for')?.split(',') || [];
                
                // Format nutrition info
                const nutritionInfo = `
                    <h6>Nutrition Facts</h6>
                    <ul class="list-unstyled">
                        <li><strong>Calories:</strong> ${calories}</li>
                        <li><strong>Protein:</strong> ${protein}g</li>
                        <li><strong>Carbs:</strong> ${carbs}g</li>
                        <li><strong>Fat:</strong> ${fat}g</li>
                        <li><strong>Sodium:</strong> ${sodium}mg</li>
                    </ul>
                `;
                
                // Format allergen info
                let allergenInfo = '<h6>Allergens</h6>';
                if (allergens.length === 0 || allergens[0] === 'none') {
                    allergenInfo += '<p class="text-success">No common allergens</p>';
                } else {
                    allergenInfo += '<ul class="list-unstyled">';
                    allergens.forEach(allergen => {
                        allergenInfo += `<li><i class="fas fa-exclamation-triangle text-warning"></i> ${allergen.charAt(0).toUpperCase() + allergen.slice(1)}</li>`;
                    });
                    allergenInfo += '</ul>';
                }
                
                // Format disease info
                let diseaseInfo = '<h6>Health Conditions</h6>';
                diseaseInfo += '<ul class="list-unstyled">';
                
                if (unsafeFor.length > 0 && unsafeFor[0] !== '') {
                    unsafeFor.forEach(disease => {
                        diseaseInfo += `<li><i class="fas fa-times-circle text-danger"></i> Not safe for ${disease.charAt(0).toUpperCase() + disease.slice(1)}</li>`;
                    });
                }
                
                if (safeFor.length > 0 && safeFor[0] !== '') {
                    safeFor.forEach(disease => {
                        diseaseInfo += `<li><i class="fas fa-check-circle text-success"></i> Safe for ${disease.charAt(0).toUpperCase() + disease.slice(1)}</li>`;
                    });
                }
                
                diseaseInfo += '</ul>';
                
                // Populate comparison modal
                if (!food1Selected) {
                    food1Selected = {
                        name: foodName,
                        img: foodImg,
                        nutrition: nutritionInfo,
                        allergens: allergenInfo,
                        diseases: diseaseInfo
                    };
                    
                    document.getElementById('food1Title').textContent = foodName;
                    document.getElementById('food1Image').innerHTML = `<img src="${foodImg}" alt="${foodName}" class="food-image" style="width: 100px; height: 100px;">`;
                    document.getElementById('food1Nutrition').innerHTML = nutritionInfo;
                    document.getElementById('food1Allergens').innerHTML = allergenInfo;
                    document.getElementById('food1Diseases').innerHTML = diseaseInfo;
                    
                    comparisonModal.show();
                } else if (!food2Selected) {
                    food2Selected = {
                        name: foodName,
                        img: foodImg,
                        nutrition: nutritionInfo,
                        allergens: allergenInfo,
                        diseases: diseaseInfo
                    };
                    
                    document.getElementById('food2Title').textContent = foodName;
                    document.getElementById('food2Image').innerHTML = `<img src="${foodImg}" alt="${foodName}" class="food-image" style="width: 100px; height: 100px;">`;
                    document.getElementById('food2Nutrition').innerHTML = nutritionInfo;
                    document.getElementById('food2Allergens').innerHTML = allergenInfo;
                    document.getElementById('food2Diseases').innerHTML = diseaseInfo;
                    
                    comparisonModal.show();
                } else {
                    // If both foods are already selected, replace food2 with the new selection
                    food2Selected = {
                        name: foodName,
                        img: foodImg,
                        nutrition: nutritionInfo,
                        allergens: allergenInfo,
                        diseases: diseaseInfo
                    };
                    
                    document.getElementById('food2Title').textContent = foodName;
                    document.getElementById('food2Image').innerHTML = `<img src="${foodImg}" alt="${foodName}" class="food-image" style="width: 100px; height: 100px;">`;
                    document.getElementById('food2Nutrition').innerHTML = nutritionInfo;
                    document.getElementById('food2Allergens').innerHTML = allergenInfo;
                    document.getElementById('food2Diseases').innerHTML = diseaseInfo;
                    
                    comparisonModal.show();
                }
            });
        });
        
        // Reset comparison button
        const resetComparisonBtn = document.getElementById('resetComparison');
        if (resetComparisonBtn) {
            resetComparisonBtn.addEventListener('click', function() {
                food1Selected = null;
                food2Selected = null;
                
                document.getElementById('food1Title').textContent = 'Select First Food';
                document.getElementById('food1Image').innerHTML = '';
                document.getElementById('food1Nutrition').innerHTML = '';
                document.getElementById('food1Allergens').innerHTML = '';
                document.getElementById('food1Diseases').innerHTML = '';
                
                document.getElementById('food2Title').textContent = 'Select Second Food';
                document.getElementById('food2Image').innerHTML = '';
                document.getElementById('food2Nutrition').innerHTML = '';
                document.getElementById('food2Allergens').innerHTML = '';
                document.getElementById('food2Diseases').innerHTML = '';
            });
        }
    }
    
    // Add animation class to elements
    const animateElements = document.querySelectorAll('.hero-section, .disease-card');
    animateElements.forEach(element => {
        element.classList.add('fadeIn');
    });
    
    // Add animation for elements with animate-* classes
    const animatedElements = document.querySelectorAll('.animate-fade-in, .animate-slide-up, .animate-card');
    
    // Use Intersection Observer to trigger animations when elements are in view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Category filter functionality for Food Menu
    const filterBtns = document.querySelectorAll('.filter-btn');
    if (filterBtns.length > 0) {
        const foodItems = document.querySelectorAll('.food-item');
        
        filterBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active class from all buttons
                filterBtns.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                const filterValue = this.getAttribute('data-filter');
                
                foodItems.forEach(item => {
                    if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                        item.style.display = 'block';
                        setTimeout(() => {
                            item.classList.add('animated');
                        }, 100);
                    } else {
                        item.style.display = 'none';
                        item.classList.remove('animated');
                    }
                });
            });
        });
    }
});
