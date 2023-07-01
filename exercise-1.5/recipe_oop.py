class Recipe(object):
    
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.cooking_time = None
        self.ingredients = []
        self.difficulty = ""

    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
    
    def get_cooking_time(self):
        return self.cooking_time
    
    def update_all_ingredients(self, ingredients):
      for ingredient in ingredients:
        if ingredient not in ingredients:
            self.all_ingredients.append(ingredient)

    def add_ingredients(self, ingredient):
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)
        #self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calc_difficulty(self):
        cooking_time = self.cooking_time
        ingredients = self.ingredients
        if cooking_time < 10 and len(ingredients) < 4:         
            difficulty = "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
          difficulty = "Intermediate"
        elif cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = "Hard"
        self.difficulty = difficulty
        return difficulty
  
    def set_difficulty(self):
        self.calc_difficulty()

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def __str__(self):
        output = "\nRecipe Name: " + str(self.name) + \
        "\nCooking Time: " + str(self.cooking_time) + \
        "\nIngredients: " + ', '.join(self.ingredients) + \
        "\nDifficulty: " + str(self.difficulty)
        return output

def recipe_search(data, search_term):
    printed_recipes = []
    for recipe in data:
        if recipe.search_ingredient(search_term):
            printed_recipes.append(recipe)
        if recipe not in printed_recipes:
          print(recipe)

#Tea
tea = Recipe("Tea")
tea.add_ingredients("Tea leaves")
tea.add_ingredients("Sugar")
tea.add_ingredients("Water")
tea.set_cooking_time(5)
tea.set_difficulty()

#Coffee
coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Beans")
coffee.add_ingredients("Sugar")
coffee.add_ingredients("Water")
coffee.set_cooking_time(5)
coffee.set_difficulty()

#Cake
cake = Recipe("Cake")
cake.add_ingredients("Sugar")
cake.add_ingredients("Butter")
cake.add_ingredients("Eggs")
cake.add_ingredients("Vanilla Essence")
cake.add_ingredients("Flour")
cake.add_ingredients("Baking Powder")
cake.add_ingredients("Milk")
cake.set_cooking_time(50)
cake.set_difficulty()

#Banana Smoothie
banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas")
banana_smoothie.add_ingredients("Milk")
banana_smoothie.add_ingredients("Peanut Butter")
banana_smoothie.add_ingredients("Sugar")
banana_smoothie.add_ingredients("Ice Cubes")
banana_smoothie.set_cooking_time(5)
banana_smoothie.set_difficulty()

recipes_list = [tea, coffee, cake, banana_smoothie]

""" print(tea),
print(coffee),
print(cake),
print(banana_smoothie) """

search_terms = ["Water", "Sugar", "Bananas"]
for ingredient in search_terms:
  recipe_search(recipes_list, ingredient)