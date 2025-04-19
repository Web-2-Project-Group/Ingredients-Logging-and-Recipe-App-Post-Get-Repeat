from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
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
def add_recipe_action():
    data = request.form

    try:
        # Parse ingredients and measurements
        ingredients = []
        number_of_ingredients = []
        i = 0
        while f'ingredient_name_{i}' in data:
            name = data[f'ingredient_name_{i}']
            measurement = data[f'ingredient_measurement_{i}']
            ingredients.append(name)
            number_of_ingredients.append(measurement)
            i += 1

        result = add_recipe_to_user(
            user_id=int(data['user_id']),
            title=data['title'],
            number_of_ingredients=number_of_ingredients,
            ingredients=ingredients,
            instructions=data['instructions'].split('\n'),
            image=data.get('image_url', '')
        )

        if result:
            flash("Recipe added successfully!")
            return redirect(url_for('recipe_views.add_recipe_page'))
        else:
            flash("Failed to add recipe.", "error")
            return redirect(url_for('recipe_views.add_recipe_page'))

    except Exception as e:
        return jsonify({'error': str(e)}), 400

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
