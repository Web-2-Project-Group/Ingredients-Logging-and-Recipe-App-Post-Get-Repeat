from App.database import db

class Inventory(db.Model):
    _tablename_ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, item_name, quantity, user_id):
        self.item_name = item_name
        self.quantity = quantity
        self.user_id = user_id