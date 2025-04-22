from App.models import User, Recipe, Inventory
from App.database import db
from unicodedata import numeric

def convertFromNumerics(num):
    if len(num) == 1:
        v = numeric(num)
    elif num[-1].isdigit():
        v = float(num)
    else:
        v = float(num[:-1]) + numeric(num[-1])
    return v  

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
        db.session.commit()
        return user
    return None

def add_recipe_to_user(user_id, title, number_of_ingredients, ingredients, instructions, image, description, cook_time):
    user = get_user(user_id)
    recipe = Recipe(title=title, number_of_ingredients=number_of_ingredients, ingredients=ingredients, instructions=instructions, user_id=user_id, image=image, cook_time=cook_time, description=description)
    if recipe and user:
        db.session.add(recipe)
        db.session.commit()
        return recipe
    return None

def add_inventory_to_user(user_id, item_name, quantity, category):
    user = get_user(user_id)
    inventory = Inventory(item_name=item_name, quantity=quantity, user_id=user_id, category=category)
    if inventory and user:
        db.session.add(inventory)
        db.session.commit()
        return inventory
    return None

def check_item_in_inventory(user_id, item_name):
    inventory = Inventory.query.filter_by(item_name=item_name, user_id=user_id).first()
    if inventory:
        return inventory
    else:
        return None

def edit_inventory(user_id, item_name, quantity):
    user = get_user(user_id)
    inventory = Inventory.query.filter_by(item_name=item_name, user_id=user_id).first()
    if inventory and user:
        inventory.quantity = quantity
        db.session.add(inventory)
        db.session.commit()
        return inventory
    return None

def add_to_inventory(user_id, item_name, quantity):
    user = get_user(user_id)
    inventory = Inventory.query.filter_by(item_name=item_name, user_id=user_id).first()
    if inventory and user:
        old = inventory.quantity
        olds = old.split()
        news = quantity.split()
        old_int = int(olds[0])
        new_int = int(news[0])
        sum = old_int + new_int
        inventory.quantity = (f"{sum} {news[1]}")
        db.session.add(inventory)
        db.session.commit()
        return inventory
    return None

def delete_inventory(id):
    inventory = Inventory.query.filter_by(id=id).first()
    if inventory:
        db.session.delete(inventory)
        db.session.commit()
        return inventory
    return None

# ensure that the inventory units is converted to the same unit before comparing
def check_inventory_against_recipe(user_id, recipe_id): # check if the user has the ingredients to make the recipe (take in user_id and recipe_id and return a message if the user has the ingredients or not)
    user = get_user(user_id)
    recipe = Recipe.query.get(recipe_id) # get the recipe by id
    if recipe and user:
        recipe_ingredients = recipe.ingredients.split(';') # split the ingredients of recipe into separate items
        num_ingredients = recipe.number_of_ingredients.split(';') # split the number of ingredients of recipe into separate items
        user_inventory = Inventory.query.filter_by(user_id=user_id).all() # get all the inventory items of the user
        i = 0
        message = []
        for ingredient in recipe_ingredients: # loop through the ingredients of the recipe
            inventory_flag = False
            for item in user_inventory: # loop through the inventory items of the user
                if ingredient.lower() == item.item_name.lower():
                    measurement1 = item.quantity.split(' ') # measurement1 is the measurement from the inventory
                    measurement2 = num_ingredients[i].split(' ') # measurement2 is the measurement from the recipe
                    num1 = convertFromNumerics(measurement1[0])
                    num2 = convertFromNumerics(measurement2[0])
                    sum = num1 - num2
                    if sum < 0:
                        message.append(f"You are missing {sum}")
                    else:
                        message.append(f"You have enough {item.item_name}!")
                    i += 1
                    inventory_flag = True
                    break
                else:
                    i += 1
            if not inventory_flag:
                message.append(f"You are missing {ingredient}")
        return message
    else:
        return ("Either user or recipe does not exist.")
