recipes_list = []
ingredients_list = []

def take_recipe():
    name = str(input("What is the name of your recipe? "))
    cooking_time = int(input("How many minutes does your recipe take to make? "))
    number_of_ingredients = int(input("How many ingredients does your recipe have? "))

    ingredients = []

    for number_of_ingredients in range(0, number_of_ingredients):
        ingredient = str(input("Enter an ingredient: "))
        ingredients.append(ingredient)
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ingredients}
    recipes_list.append(recipe)

    for recipe in recipes_list:
      if cooking_time < 10 and len(ingredients) < 4:
          difficulty = "Easy"
      elif cooking_time < 10 and len(ingredients) >= 4:
          difficulty = "Medium"
      elif cooking_time >= 10 and len(ingredients) < 4:
          difficulty = "Intermediate"
      elif cooking_time >= 10 and len(ingredients) >= 4:
          difficulty = "Hard"
      recipe["difficulty"] = difficulty
    #return recipe

n = int(input("How many recipes would you like to enter? "))

for n in range(0, n):
    take_recipe()

print("************************")
for recipe in recipes_list:
    print("************************")
    print("Recipe: ", recipe.get('name'))
    print("Cooking Time: ", recipe.get('cooking_time'))
    print("Ingredients: ")
    ingredients = recipe.get("ingredients")
    for ingredient in ingredients:
        print(ingredient)
    print("Difficulty ", recipe.get('difficulty'))

print("************************")
print("All Ingredients: ")
for ingredient in ingredients_list:
    print(ingredient)