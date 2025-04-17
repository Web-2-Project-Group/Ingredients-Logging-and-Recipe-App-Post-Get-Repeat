from App.models import User, Recipe, Inventory
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def add_recipe_to_user(user_id, title, number_of_ingredients, ingredients, instructions):
    user = get_user(user_id)
    recipe = Recipe(title=title, number_of_ingredients=number_of_ingredients, ingredients=ingredients, instructions=instructions, user_id=user_id)
    if recipe and user:
        user.recipe.append(recipe)
        db.session.add(user)
        return db.session.commit()
    return None

def add_inventory_to_user(user_id, item_name, quantity):
    user = get_user(user_id)
    inventory = Inventory(item_name=item_name, quantity=quantity, user_id=user_id)
    if inventory and user:
        user.inventory.append(inventory)
        db.session.add(user)
        return db.session.commit()
    return None

def edit_inventory(user_id, item_name, quantity):
    user = get_user(user_id)
    inventory = Inventory.query.filter_by(item_name=item_name, user_id=user_id).first()
    if inventory and user:
        inventory.quantity = quantity
        db.session.add(inventory)
        return db.session.commit()
    return None

def delete_inventory(user_id, item_name):
    user = get_user(user_id)
    inventory = Inventory.query.filter_by(item_name=item_name, user_id=user_id).first()
    if inventory and user:
        db.session.delete(inventory)
        return db.session.commit()
    return None
# ensure that the inventory units is converted to the same unit before comparing
def check_inventory_against_recipe(user_id, recipe_id):
    user = get_user(user_id)
    recipe = Recipe.query.get(recipe_id)
    if recipe and user:
        recipe_ingredients = recipe.ingredients.split(';')
        user_inventory = Inventory.query.filter_by(user_id=user_id).all()
        message = []
        for ingredient in recipe_ingredients:
            for item in user_inventory:
                if ingredient == item.item_name:
                    measurement1 = item.quantity.split(' ')
                    measurement2 = ingredient.