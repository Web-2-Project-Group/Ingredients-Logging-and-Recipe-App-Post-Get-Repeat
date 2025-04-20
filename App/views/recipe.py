from App.database import db
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from App.models import Recipe,User,Review,Inventory
from flask_login import current_user, login_required
from flask_jwt_extended import jwt_required, current_user
from App.controllers import (
    add_recipe_to_user,
    add_inventory_to_user,
    check_inventory_against_recipe,
    get_user
)

recipe_views = Blueprint('recipe_views', __name__, template_folder='../templates')

# Render form to add a new recipe
@recipe_views.route('/recipes/add', methods=['GET'])
def add_recipe_page():
    return render_template('add-recipe.html')

# Handle form submission to add a recipe
@recipe_views.route('/recipes/add', methods=['POST'])
@jwt_required()
def add_recipe_action():
    data = request.form
    
    try:
        # Parse ingredients and measurements with categories
        ingredients = []
        quantities = []
        categories = []
        i = 0
        
        while f'ingredient_name_{i}' in data:
            category = data.get(f'ingredient_category_{i}', '').strip()
            name = data[f'ingredient_name_{i}'].strip()
            quantity = data[f'ingredient_quantity_{i}'].strip()
            unit = data[f'ingredient_unit_{i}'].strip()
            
            if name and quantity:  # Only add if both fields have values
                if not category:
                    flash(f"Please select a category for ingredient: {name}", "error")
                    return redirect(url_for('recipe_views.add_recipe_page'))
                
                ingredients.append(name)
                quantities.append(f"{quantity} {unit}")
                categories.append(category)
            i += 1

        if not ingredients:
            flash("At least one ingredient is required", "error")
            return redirect(url_for('recipe_views.add_recipe_page'))

        # Split instructions by newlines and filter empty lines
        instructions = [line.strip() for line in data['instructions'].split('\n') if line.strip()]

        # First add the recipe
        recipe = Recipe(
            title=data['title'],
            number_of_ingredients=';'.join(quantities),
            ingredients=';'.join(ingredients),
            instructions=';'.join(instructions),
            image=data.get('image_url', ''),
            description=data.get('description', ''),
            cook_time=data.get('cook_time', ''),
            user_id=current_user.id
        )
        
        db.session.add(recipe)
        db.session.commit()

        # Then add ingredients to inventory if they don't exist
        for i in range(len(ingredients)):
            # Check if ingredient already exists in user's inventory
            existing = Inventory.query.filter_by(
                item_name=ingredients[i],
                user_id=current_user.id
            ).first()
            
            if not existing:
                new_inventory = Inventory(
                    item_name=ingredients[i],
                    quantity=quantities[i],
                    category=categories[i],
                    user_id=current_user.id
                )
                db.session.add(new_inventory)
        
        db.session.commit()
        flash("Recipe added successfully and new ingredients added to your inventory!", "success")
        return redirect(url_for('recipe_views.my_recipes_page'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('recipe_views.add_recipe_page'))
# Add an ingredient to a user's inventory
@recipe_views.route('/inventory/add', methods=['POST'])
def add_ingredient_action():
    data = request.form
    try:
        result = add_inventory_to_user(
            user_id=int(data['user_id']),
            item_name=data['item_name'],
            quantity=data['quantity'],
            category=data['category']
        )
        if result:
            flash("Ingredient added to inventory!")
            return redirect(url_for('recipe_views.add_recipe_page'))
        else:
            flash("Failed to add ingredient.", "error")
            return redirect(url_for('recipe_views.add_recipe_page'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Check if a user can make a recipe based on their inventory
@recipe_views.route('/recipes/<int:recipe_id>/check', methods=['GET'])
def check_recipe_ingredients(recipe_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400

    try:
        result = check_inventory_against_recipe(int(user_id), recipe_id)
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Add this to your recipe_views.py
@recipe_views.route('/recipes/<int:recipe_id>', methods=['GET'])
def recipe_details_page(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        flash('Recipe not found', 'error')
        return redirect(url_for('recipe_views.my_recipes_page'))
    return render_template('recipe-details.html', recipe=recipe)

@recipe_views.route('/my-recipes')
@jwt_required()
def my_recipes_page():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('recipes.html', recipes=recipes)


@recipe_views.route('/recipes/<int:recipe_id>/review', methods=['POST'])
@jwt_required()
def add_review(recipe_id):
    try:
        # Get and validate rating
        rating = float(request.form.get('rating'))
        if not (1 <= rating <= 5):
            flash('Rating must be between 1 and 5', 'error')
            return redirect(url_for('recipe_views.recipe_details_page', recipe_id=recipe_id))
        
        # Get and validate comment
        comment = request.form.get('comment', '').strip()
        if not comment:
            flash('Please enter a review comment', 'error')
            return redirect(url_for('recipe_views.recipe_details_page', recipe_id=recipe_id))
        
        # Create and save review
        review = Review(
            rating=rating,
            comment=comment,
            user_id=current_user.id,
            recipe_id=recipe_id
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Your review has been added!', 'success')
    except ValueError:
        flash('Please enter a valid number for rating', 'error')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add review: ' + str(e), 'error')
    
    return redirect(url_for('recipe_views.recipe_details_page', recipe_id=recipe_id))