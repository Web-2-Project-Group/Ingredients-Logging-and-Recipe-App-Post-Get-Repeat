from App.models import Recipe, Drecipes
from App.database import db
import schedule
import time
import random 

def produce_new_daily_recipes():
  recipes = Recipe.query.all()
  daily_recipes = random.sample(recipes,4)
  db.session.query(Drecipes).delete()
  for recipe in daily_recipes:
    daily_recipe = Drecipes(recipe_id=recipe.id)
    db.session.add(daily_recipe)
  db.session.commit()
  return daily_recipes

def get_daily_recipes():
  recipes = Drecipes.query.all()
  return recipes    

