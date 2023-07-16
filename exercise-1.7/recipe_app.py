from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_


#Creates the connection to the DB
engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

#Generates a class from SQLAlchemy to be used in Recipe Class
Base = declarative_base()
#The model that defines the query the DB
class Recipe(Base):
    __tablename__ = "final_recipes"

    #Defines the shape of the class
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + " - " + self.name + " - " + self.difficulty + ">"
    
    #Is printed when the recipe is printed
    def __str__(self):
        output = "\nRecipe ID: " + str(self.id) + \
        "\nRecipe Name: " + str(self.name) + \
        "\nCooking Time: " + str(self.cooking_time) + \
        "\nIngredients: " + (self.ingredients) + \
        "\nDifficulty: " + str(self.difficulty)
        #print(output)
        return output

    #Calculates the difficulty of the recipe, function is called in create_recipe()
    def calc_difficulty(self, name, ingredients, cooking_time):
        #print('ingredients', ingredients)
        #print('Here')
        ingredients = ingredients.split(', ')
        length = len(ingredients)
        #print('length', length)
        if cooking_time < 10 and length < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and length >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and length < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and length >= 4:
            difficulty = "Hard"
        #print('Difficulty: ', difficulty)
        #Sets the difficulty of the recipe in the database
        session.query(Recipe).filter(Recipe.name == name).update({Recipe.difficulty: difficulty})
        session.commit()
        return self.difficulty

#Creates the table in the database if it is not already there
Base.metadata.create_all(engine)

#Class that moves the data across the engine connection
Session = sessionmaker(bind=engine)
session = Session()

#Prompts user to enter the recipe details
def create_recipe():
    #print('create_recipe')

    #Walks the user through entering a recipe
    name = None
    while True:
        name = str(input("What is the name of your recipe? "))
        if type(name) == str and len(name) < 51:
            break
        else:
            print('Please enter a valid name, with no more than 50 characters.')

    cooking_time = None
    while True:
        try:
            cooking_time = int(input("How many minutes does your recipe take to make? "))
            break
        except ValueError:
            print('Please enter a number.')

    number_of_ingredients = None
    while True:
        try:
            number_of_ingredients = int(input("How many ingredients does your recipe have? "))
            break
        except ValueError:        
            print('Please enter a number.')

    #Walks the user through entering the ingredients
    ingredients = []
    stringified_ingredients = ''
    while True:
        total_length = 0
        ingredients = []
        for number_of_ingredients in range(0, number_of_ingredients):
            ingredient = str(input("Enter an ingredient: "))
            ingredient_length = len(ingredient)
            if total_length + ingredient_length > 250:
                print("Total length of ingredients cannot exeed more than 250")
                break
            total_length += ingredient_length
            ingredients.append(ingredient)
        else:
            # If the loop completes without breaking, it means the total length is within the limit
            stringified_ingredients = ', '.join(str(item) for item in ingredients)
            break

    #print('Recipe: ', name, 'Cooking Time: ', cooking_time, 'Ingredients: ', stringified_ingredients)
    #Creates the recipe using the Recipe class
    recipe = Recipe(
        name = name,
        ingredients = stringified_ingredients,
        cooking_time = cooking_time
    )

    #Adds the recipe to the DB
    session.add(recipe)
    session.commit()

    #Calculates the difficulty
    recipe.calc_difficulty(name, stringified_ingredients, cooking_time)

    print('*'*10 + ' RECIPE CREATED ' + '*'*10)

#View all recipes
def view_all_recipes():
    #print('view_all_recipes')

    #Gets all recipes from the DB
    recipes_list = session.query(Recipe).all()
    #Checks for recipes
    if recipes_list == []:
        print()
        print('No recipes available. Please add a recipe.')
        return None
    #Prints all recipes
    else:
        print()
        print('*'*10 + ' ALL RECIPES ' + '*'*10)
        for recipe in recipes_list:
            print(recipe)
        print()
        print('*'*10 + ' END OF RECIPES ' + '*'*10)
        
def search_recipe():
    #print('search_recipe')
    print()
    #Counts recipes
    recipe_count = session.query(Recipe).count()
    #Checks for no recipes
    if recipe_count == 0:
        print()
        print('No recipes available. Please add a recipe.')
        return None
    #Prints all ingredients with no repetitions
    else:
        print('Choose one or more ingredients.')
        print()
        results = session.query(Recipe).all()
        all_ingredients = []
        #choice = ''
        for result in results:
            ingredients = result.ingredients
            recipe_ingredient_split = ingredients.split(", ")
            
            for ingredient in recipe_ingredient_split:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
        for index, ingredient in enumerate(all_ingredients):        
            print(str(index) + ": " + ingredient)
        
        try:
            search_ingredients = input('\nEnter your choice, separate multiple ingredients with a space: ')
            search_ingredients_split = search_ingredients.split()
            search_ingredients = []
            for ingredient in search_ingredients_split:
                ingredient = int(ingredient)
                if ingredient < len(all_ingredients):
                    ingredient = all_ingredients[ingredient]
                    search_ingredients.append(ingredient)
                else: 
                    print('\nPlease enter a valid number')
                    return None
            print('\nYou searched for: \n')
            for ingredient in search_ingredients:
                print(ingredient)
            
            conditions = []
            for ingredient in search_ingredients:
                like_term = "%"+ingredient+"%"
                ingredient = Recipe.ingredients.like(like_term)
                conditions.append(ingredient)
            query_result = session.query(Recipe).filter(or_(*conditions)).all()
            print()
            print('*'*10 + ' SEARCH RESULTS ' + '*'*10)
            for recipe in query_result:
                print(recipe)
            print()
            print('*'*10 + ' END OF SEARCH RESULTS ' + '*'*10)

        except:
            print('An unexpected error occurred. Make sure to select a number from the list.')

def update_recipe():
    #print('update_recipe\n')
    #Counts number of recipes
    recipe_count = session.query(Recipe).count()
    #Checks for no recipes
    if recipe_count == 0:
        print()
        print('No recipes available. Please add a recipe.')
        return None
    #Prints the recipes available
    else:
        results = session.query(Recipe).all()
        #print('Which recipe would you like to update? Enter the ID.\n')
        for result in results:
            print('Recipe ID ' + str(result.id) + ': ' + result.name)
    #print(recipe)
    recipe_id = input('\nWhich recipe would you like to update? Enter the ID: ')
    #Prints recipe and asks user to choose the ingredient to update
    try:
        recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        print()
        print('*'*10 + ' RECIPE ' + '*'*10)
        print(recipe_to_edit)
        print()
        print('Which element would you like to edit?\n')
        print('1. Name')
        print('2. Ingredients')
        print('3. Cooking Time')
        print()
        element_to_edit = int(input('Enter the corresponding number. To go back to main menu type \'exit\': '))
        new_element_value = input('What is the new value? (Note: For ingredients, separate the ingredients by comma. ')
        #Logic for the different parts of the recipe
        if element_to_edit == 1:
            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.name: new_element_value})
            session.commit()
            print('*'*10 + ' RECIPE ' + '*'*10)
            print(recipe_to_edit)
            print()
        elif element_to_edit == 2:
            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: new_element_value})
            session.commit()
            print('*'*10 + ' RECIPE ' + '*'*10)
            print(recipe_to_edit)
            print() 
        elif element_to_edit == 3:
            session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.cooking_time: new_element_value})
            session.commit()
            print('*'*10 + ' RECIPE ' + '*'*10)
            print(recipe_to_edit)
            print()
        elif element_to_edit == 'exit':
            main_menu()
        else:
            print('Invalid input, please try again.')
            
    except:
        print('\nError: Invalid recipe ID')
        return None
    
        """  else:
        recipe_for_recalc_difficulty = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        print('recipe_to_edit: ', recipe_for_recalc_difficulty)
        print('name', recipe_for_recalc_difficulty.name)
        print('ingredients', recipe_for_recalc_difficulty.ingredients)
        print('cooking time', int(recipe_for_recalc_difficulty.cooking_time))
        Recipe.calc_difficulty(recipe_for_recalc_difficulty.name, recipe_for_recalc_difficulty.ingredients, int(recipe_for_recalc_difficulty.cooking_time)) """

def delete_recipe():
    #print('delete_recipe\n')

    recipe_count = session.query(Recipe).count()
    #Check for 0 recipes
    if recipe_count == 0:
        print()
        print('No recipes available. Please add a recipe.')
        return None
    #Displays list of recipes to be deleted
    else:
        results = session.query(Recipe).all()
        #print('Which recipe would you like to update? Enter the ID.\n')
        for result in results:
            print('Recipe ID ' + str(result.id) + ': ' + result.name)
    recipe_to_delete = ''
    try:
        recipe_id = input('\nWhich recipe would you like to delete? Enter the ID: ')
        #Handles the deletion
        if recipe_id.isnumeric():
            recipe_to_delete = session.query(Recipe).filter(Recipe.id == int(recipe_id)).one()
            confirmation = input('You want to delete ' + recipe_to_delete.name + '? Y or N: ')
            if confirmation == 'Y' or confirmation == 'y':
                session.delete(recipe_to_delete)
                session.commit()
                print('*'*10 + ' RECIPE DELETED ' + '*'*10)
            elif confirmation == 'N':
                main_menu()
            else: 
              print('Please try again.')
        else:
            print('\nlease enter a number.')
            return None

    finally:
        print(recipe_to_delete.name + ' was deleted')
        #print(recipe_to_delete)

#Main menu that loads when app is started
def main_menu():
    choice = ''
    while(choice != 'quit'):
        print()
        print('What would you like to do? Pick a choice!')
        print()
        print('1. Create a recipe')
        print('2. View all recipes')
        print('3. Search a recipe')
        print('4. Update a recipe')
        print('5. Delete a recipe')
        print()
        print('Type "quit" to exit.')
        print()
        choice = input("Your choice: ")

        if choice == '1':
            #print('add_recipe')
            create_recipe()

        elif choice == '2':
            #print('view_all_recipes')
            view_all_recipes()

        elif choice == '3':
            #print('search_recipe')
            search_recipe()

        elif choice == '4':
            #print('update_recipe')
            update_recipe()

        elif choice == '5':
            #print('delete_recipe')
            delete_recipe()
    
        else:
            print('Error: Please make a selection.')
            #main_menu()

#Starts app
main_menu()