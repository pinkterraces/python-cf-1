import pickle

def display_recipe(recipe):
    print("************************")
    print("************************")
    print("Recipe: ", recipe.get('name'))
    print("Cooking Time: ", recipe.get('cooking_time'))
    print("Ingredients: ")
    ingredients = recipe.get("ingredients")
    for ingredient in ingredients:
        print(ingredient)
    print("Difficulty ", recipe.get('difficulty'))

def search_ingredient(data):
    #print("data: ", data)
    ingredients = data['ingredients_list']
    print("************************")
    print("All Ingredients: ")
    for index, ingredient in enumerate(ingredients):
      print(str(index) + ": " + ingredient)
    return ingredients

try:
    with open('combined_list.bin', 'rb') as my_file:
        data = pickle.load(my_file)
except:
    print("File could not be found")
else:
    search_ingredient(data)

try:
    selected_number = int(input("Enter the corresponding number for the ingredient you'd like to search: "))
    ingredients = data['ingredients_list']
    ingredient_searched = ingredients[selected_number]
    print("************************")
    print("You searched for:", ingredient_searched)
except:
    print("Incorrect exception")
else:
    #print(recipes_for_search)
    recipes = data['recipes_list']
    for recipe in recipes:
        if ingredient_searched in recipe['ingredients']:
            display_recipe(recipe)