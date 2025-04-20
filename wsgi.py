import click, pytest, sys
import csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User,Recipe
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from pathlib import Path
# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

def initialize():
    """Initialize the database with tables and sample data"""
    try:
        db.drop_all()
        db.create_all()
        
        # Create initial user 'bob' with hashed password
        if not User.query.filter_by(username="bob").first():
            bob = User(username="bob")
            bob.set_password("bobpass")  # Hash the password
            db.session.add(bob)
            db.session.commit()
            print("Initial user 'bob' created with password 'bobpass'")
        else:
            print("User 'bob' already exists")

        # Load recipes from CSV
        csv_path = Path("App/data/recipes.csv")
        if csv_path.exists():
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Case-insensitive column matching
                field_map = {
                    'title': None,
                    'number_of_ingredients': None,
                    'ingredients': None,
                    'instructions': None
                }
                
                # Map actual headers to expected fields
                for header in reader.fieldnames:
                    lower_header = header.lower()
                    if 'title' in lower_header:
                        field_map['title'] = header
                    elif 'number' in lower_header and 'ingredient' in lower_header:
                        field_map['number_of_ingredients'] = header
                    elif 'ingredient' in lower_header:
                        field_map['ingredients'] = header
                    elif 'instruction' in lower_header:
                        field_map['instructions'] = header
                
                # Verify we found all required columns
                if None in field_map.values():
                    missing = [k for k,v in field_map.items() if v is None]
                    print(f"CSV missing required columns: {missing}")
                    return False
                
                recipes_added = 0
                for row in reader:
                    try:
                        # Calculate number of ingredients if not provided
                        ingredients = [i.strip() for i in row[field_map['ingredients']].split(';') if i.strip()]
                        num_ingredients = len(ingredients)
                        
                        # Clean instructions
                        instructions = [i.strip() for i in row[field_map['instructions']].split('.') if i.strip()]
                        
                        recipe = Recipe(
                            title=row[field_map['title']],
                            number_of_ingredients=num_ingredients,
                            ingredients=ingredients,
                            instructions=instructions,
                            image="",  # Default empty image
                            user_id=bob.id
                        )
                        db.session.add(recipe)
                        recipes_added += 1
                    except Exception as e:
                        print(f"Error processing row {reader.line_num}: {e}")
                        continue
                
                db.session.commit()
                print(f"Successfully added {recipes_added} recipes")
        else:
            print("No recipes.csv found - database initialized without recipes")
        return True
    except Exception as e:
        print(f"Initialization failed: {e}")
        db.session.rollback()
        return False

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

