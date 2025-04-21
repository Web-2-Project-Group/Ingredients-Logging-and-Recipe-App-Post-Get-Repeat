from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from App.models import Recipe,User,Review,Inventory

daily_recipe_views = Blueprint('daily_recipe_views', __name__, template_folder='../templates')

@daily_recipe_views.route('/daily-recipes')
@jwt_required()
def daily_recipes_page():
    recipes = produce_new_daily_recipes()
    dailyrecipes[]
    for id in dailyrecipes:
        recipe = Recipe.query.get(id)
        dailyrecipes.append(recipe)
    return render_template('dailyrecipe.html', dailyrecipes=dailyrecipes)
