from App.database import db

class Recipe(db.Model):
    _tablename_ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    number_of_ingredients = db.Column(db.String(256), nullable=False)
    ingredients = db.Column(db.String(256), nullable=False)
    instructions = db.Column(db.String(512), nullable=False)
    image = db.Column(db.String(256), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, title, number_of_ingredients, ingredients, instructions, user_id, image):
        self.title = title
        line_number_of_ingredients = ';'.join(number_of_ingredients)
        self.number_of_ingredients = line_number_of_ingredients
        line_ingredients = ';'.join(ingredients)
        self.ingredients = line_ingredients
        line_instructions = ';'.join(instructions)
        self.instructions = line_instructions
        self.image = image
        self.user_id = user_id
        