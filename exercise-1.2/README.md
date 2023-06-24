Data sctructure...

recipe_1 = {
  'name': 'recipe_name', #string
  'cooking_time': cooking_time, #integer
  'ingredients': { #list 
    ingredient1: 'something', #string
    ingredient2: 'something else' #string
  } 
}

I've decided to use a dictionary for the data structure.
I believe that later I will want to be able to access values using a key, rather than accessing the values be index or sequentially in order. 
They're flexible, so it will be easier to add and remove items if needed.
They require unique keys, which willl be useful in identifying each recipe.
They offer fast lookup and retrieval of values.

For the all_recipes structure, I decided to use a list because the recipes should be able to be accessed sequentially.
It is also then mutable, and there are ways to easily add and remove recipes to or from the list.
