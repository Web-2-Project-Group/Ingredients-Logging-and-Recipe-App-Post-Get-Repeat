from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.recipe import Recipe
from App.models.inventory import Inventory



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    recipe = db.relationship('Recipe', backref='user', lazy=True)
    inventory = db.relationship('Inventory', backref='user', lazy=True)
    user_reviews = db.relationship('Review', backref='user', lazy=True)
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def add_recipe(self, title, number_of_ingredients, ingredients, instructions):
        new_recipe = Recipe(title=title, number_of_ingredients=number_of_ingredients, ingredients=ingredients, instructions=instructions, user_id=self.id)
        return new_recipe

    def add_inventory(self, item_name, quantity, category):
        new_inventory = Inventory(item_name=item_name, quantity=quantity, user_id=self.id, category=category)
        return new_inventory

    

