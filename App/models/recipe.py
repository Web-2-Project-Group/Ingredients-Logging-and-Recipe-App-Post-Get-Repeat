from App.database import db

class Recipe(db.Model):
    _tablename_ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    #cook_time = db.Column(db.String(500),nullable=False)
    number_of_ingredients = db.Column(db.String(900), nullable=False)
    ingredients = db.Column(db.String(900), nullable=False)
    instructions = db.Column(db.String(900), nullable=False)
    image = db.Column(db.String(256), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, title,number_of_ingredients, ingredients, instructions, image=None, user_id=None):
        self.title = title
        #self.cook_time = cook_time
        self.number_of_ingredients = number_of_ingredients
        self.ingredients = ';;'.join(ingredients)  # Double semicolon delimiter
        self.instructions = '||'.join(instructions)  # Double pipe delimiter
        self.image = image
        self.user_id = user_id
    
    def get_ingredients(self):
        """Return ingredients as list"""
        return self.ingredients.split(';;')
    
    def get_instructions(self):
        """Return instructions as list"""
        return self.instructions.split('||')