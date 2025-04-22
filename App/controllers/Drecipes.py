from App.models import Recipe, Drecipes
from App.database import db
import random 
import datetime

def produce_new_daily_recipes():
  recipes = Recipe.query.all()
  daily_recipes = random.sample(recipes,4)
  for recipe in daily_recipes:
    daily_recipe = Drecipes(recipe_id=recipe.id)
    db.session.add(daily_recipe)
  db.session.commit()

  return daily_recipes

def get_daily_recipes():
  day_test =check_day_passed()
  if(day_test):
      recipes = produce_new_daily_recipes()
  else:
    recipes = get_latest_recipes()

  return recipes[len(recipes) - 4:len(recipes)]    

def get_latest_recipes():
  recipes = Drecipes.query.all()
  recipeList = recipes[len(recipes) - 4:len(recipes)] 
  lastestRecipes = []
  for r in recipeList:
    lastestRecipes.append(Recipe.query.get(r.recipe_id))

  return lastestRecipes
  
def check_day_passed():
  dailyRecipes = Drecipes.query.all()
 

  if(len(dailyRecipes) == 0):
     return True
  lastRecipe = dailyRecipes[-1]
  date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
  print(date)
  if(lastRecipe.date < date):
    return True
  
  return False
