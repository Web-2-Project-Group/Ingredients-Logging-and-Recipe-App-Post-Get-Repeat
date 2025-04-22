from .user import create_user
from App.database import db


def initialize():
    """Initialize the database with tables and sample data"""
    try:
        db.drop_all()
        db.create_all()
        
        # Create initial user 'bob' - FIXED: provide both username and password
        bob = User.query.filter_by(username="bob").first()
        if not bob:
            # Use the constructor with both required parameters
            bob = User(username="bob", password="bobpass")
            db.session.add(bob)
            db.session.commit()
            print("Initial user 'bob' created with password 'bobpass'")
        else:
            print("User 'bob' already exists")

        carl = signup("carl","carlpass")

        # Load recipes from CSV
        csv_path = Path("App/data/recipe.csv")
        if csv_path.exists():
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                field_map = {
                    'title': None,
                    'number_of_ingrdients': None,
                    'ingredients': None,
                    'instructions': None,
                    'description': None,
                    'cook_time': None
                }
                
                # Map headers case-insensitively
                for header in reader.fieldnames:
                    lower_header = header.lower()
                    if 'title' in lower_header:
                        field_map['title'] = header
                    elif 'ingredient' in lower_header:
                        field_map['ingredients'] = header
                    elif 'instruction' in lower_header:
                        field_map['instructions'] = header
                    elif 'description' in lower_header:
                        field_map['description'] = header
                    elif 'cook' in lower_header and 'time' in lower_header:
                        field_map['cook_time'] = header
                
                recipes_added = 0
                for row in reader:
                    try:
                        ingredients = [i.strip() for i in row[field_map['ingredients']].split(';') if i.strip()]
                        instructions = [i.strip() for i in row[field_map['instructions']].split('.') if i.strip()]
                        recipe = Recipe(
                            title=row[field_map['title']],
                            number_of_ingredients=row['number_of_ingredients'],
                            ingredients=ingredients,
                            instructions=instructions,
                            image=row['image'],
                            user_id=bob.id,
                            description=row.get(field_map['description'], ""),
                            cook_time=row.get(field_map['cook_time'], "")
                        )
                        db.session.add(recipe)
                        recipes_added += 1
                    except Exception as e:
                        print(f"Error processing row {reader.line_num}: {e}")
                        continue
                
                db.session.commit()
                print(f"Successfully added {recipes_added} recipes")
        else:
            print("No recipe.csv found - database initialized without recipes")
        return True
    except Exception as e:
        print(f"Initialization failed: {e}")
        db.session.rollback()
        return False
