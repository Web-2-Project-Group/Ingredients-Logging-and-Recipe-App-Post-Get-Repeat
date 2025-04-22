from App.models import Recipe, Review
from App.database import db

def get_all_recipes():
    return Recipe.query.all()

def add_review_to_recipe(recipe_id, rating, comment, user_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        review = Review(rating=rating, comment=comment, user_id=user_id, recipe_id=recipe_id)
        db.session.add(review)
        db.session.commit()
        return review
    return None

def get_recipe_by_id(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        return recipe
    return None

