from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from App.models import Recipe,User,Review,Inventory
from App.controllers import (add_inventory_to_user, add_to_inventory, check_item_in_inventory, delete_inventory)
from App.database import db

inventory_views = Blueprint('inventory_views', __name__, template_folder='../templates')

@inventory_views.route('/my-ingredients')
@jwt_required()
def my_ingredients_page():
    user = Inventory.query.all()
    return render_template('ingredients.html', user=user)

@inventory_views.route('/my-ingredients/add', methods=['GET'])
@jwt_required()
def add_ingredients_page():
    return render_template('add-ingredients.html')

@inventory_views.route('/my-ingredients/add', methods=['POST'])
@jwt_required()
def add_ingredients_action():  
    data = request.form
    ingredients = []
    categories = []
    quantities = []
    i = 0
    while f'ingredient_name_{i}' in data:
        category = data.get(f'ingredient_category_{i}', '').strip()
        name = data[f'ingredient_name_{i}'].strip().lower()
        quantity = data[f'ingredient_quantity_{i}'].strip()
        unit = data[f'ingredient_unit_{i}'].strip()

        inventory = check_item_in_inventory(item_name=name, user_id=current_user.id)
        if inventory:
            add_to_inventory(user_id=current_user.id, item_name=name, quantity=f"{quantity} {unit}")
            i += 1
        else:  
            ingredients.append(name)
            quantities.append(f"{quantity} {unit}")
            categories.append(category)
            i += 1

    nums = len(ingredients)
    if nums == 0:
        flash('Inventory was added successfully')
        return render_template('add-ingredients.html')
    else:
        flag = True
        for num in range(nums):
            print(num)
            stock = add_inventory_to_user(
                item_name=ingredients[num],
                quantity=quantities[num],
                category=categories[num],
                user_id=current_user.id
            )
            if stock == None:
                flag = False
        if flag:
            flash('Inventory was added successfully')
            return render_template('add-ingredients.html')
        else:
            flash('Inventory was not added successfully')
            return render_template('add-ingredients.html')
    
@inventory_views.route('/my-ingredients/delete/<int:id>', methods=['GET'])
@jwt_required()
def delete_ingredients_action(id):
    inventory = Inventory.query.filter_by(id=id, user_id=current_user.id )
    if inventory:
        check = delete_inventory(id)
        if check:
            flash('Inventory was deleted succesfully')
            return redirect(url_for('inventory_views.my_ingredients_page'))
        else:
            flash('Inventory was not deleted')
            return redirect(url_for('inventory_views.my_ingredients_page'))
    else:
        flash('Inventory was not deleted')
        return redirect(url_for('inventory_views.my_ingredients_page'))