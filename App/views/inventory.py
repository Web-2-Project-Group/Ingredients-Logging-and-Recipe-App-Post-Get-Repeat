from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, current_user
from App.models import Recipe,User,Review,Inventory

inventory_views = Blueprint('inventory_views', __name__, template_folder='../templates')

@inventory_views.route('/my-ingredients')
@jwt_required()
def my_ingredients_page():
    user = Inventory.query.all()
    return render_template('ingredients.html', user=user)

