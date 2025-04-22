from App.database import db
import datetime
class Drecipes(db.Model):
    _tablename_ = 'Drecipes'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, recipe_id):
        self.recipe_id = recipe_id
