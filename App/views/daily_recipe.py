from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

daily_recipe_views = Blueprint('daily_recipe_views', __name__, template_folder='../templates')

@daily_recipe_views.route('/daily-recipes')
@jwt_required()
def daily_recipes_page():
    return render_template('dailyrecipe.html')
