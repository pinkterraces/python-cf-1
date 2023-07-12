import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

cursor = conn.cursor()



cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')
cursor.execute('USE task_database')
#cursor.execute("DROP TABLE Recipes")
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(15)
)''')

""" print("**********") 
cursor.execute("DESCRIBE Recipes")
result_describe = cursor.fetchall()
for row in result_describe:
    print(row) """

#Prints all recipes on program load
""" print("**********")
cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")
results = cursor.fetchall()
for row in results:
    print("ID: ", row[0])
    print("Name: ", row[1])
    print("Ingredients: ", row[2])
    print("Cooking Time (mins): ", row[3])
    print("Difficulty:", row[4])
    print("----------") """

def main_menu(conn, cursor):

    def calc_difficulty(cooking_time, length):
            #cooking_time = recipe['cooking_time']
            #ingredients = recipe['ingredients']
            if cooking_time < 10 and length < 4:
                difficulty = "Easy"
            elif cooking_time < 10 and length >= 4:
                difficulty = "Medium"
            elif cooking_time >= 10 and length < 4:
                difficulty = "Intermediate"
            elif cooking_time >= 10 and length >= 4:
                difficulty = "Hard"
            return difficulty 

    def add_recipe(conn, cursor):
    
        recipe_id = None
        name = str(input("What is the name of your recipe? "))
        cooking_time = int(input("How many minutes does your recipe take to make? "))
        number_of_ingredients = int(input("How many ingredients does your recipe have? "))

        ingredients = []

        for number_of_ingredients in range(0, number_of_ingredients):
            ingredient = str(input("Enter an ingredient: "))
            ingredients.append(ingredient)

        recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ", ".join(ingredients), "difficulty": calc_difficulty(cooking_time, len(ingredients))}

        ingredients_string = ", ".join(ingredients)
        sql = 'INSERT INTO Recipes (id, name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s, %s)'
        val = (recipe_id, name, ingredients_string, cooking_time, calc_difficulty(cooking_time, len(ingredients)))
        #print(val)
        cursor.execute(sql, val)
        conn.commit()
        print("***** RECIPE CREATED *****")
        return recipe
    
    def search_recipe(conn, cursor):
        print('Searched')
        cursor.execute('SELECT ingredients FROM Recipes')
        results = cursor.fetchall()
        all_ingredients = []
        for recipe_ingredients_list in results:
            for recipe_ingredients in recipe_ingredients_list:
                recipe_ingredient_split = recipe_ingredients.split(", ")
                all_ingredients.extend(recipe_ingredient_split)
        no_duplicates_result = []
        for item in all_ingredients:
              if item not in no_duplicates_result:
                  no_duplicates_result.append(item)

        choice = ''
        while(choice != 'quit'):
            print('Which ingredient would you like to search for? ')
            for index, item in enumerate(no_duplicates_result):
                print(str(index) + ": " + item)
           
            choice = int(input("Your choice: "))
            search_ingredient = no_duplicates_result[choice]
            print("choice", search_ingredient)

            query = 'SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE ' + '"%' + search_ingredient + '%"'
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print("**********")
                print("ID: ", row[0])
                print("Name: ", row[1])
                print("Ingredients: ", row[2])
                print("Cooking Time (mins): ", row[3])
                print("Difficulty:", row[4])
                print("**********")
            main_menu(conn, cursor)
    
    def update_recipe(conn, cursor):
        print("**********")
        cursor.execute("SELECT id, name FROM Recipes")
        results = cursor.fetchall()
        for row in results:
            id = str(row[0])
            name = str(row[1])
            print(id + '. ' + name)
        choice = ''
        
        while choice != 'quit':
            choice = int(input("Which recipe would you like to update? Enter the corresponding number: "))
            
            query = 'SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = ' + '"' + str(choice) + '"'
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print("**********")

                #print("ID: ", row[0])
                #print("Name: ", row[1])
                print("1. Ingredients: ", row[2])
                #for index, ingredient in enumerate(stringified_ingredients):
                    #print(str(index) + ": " + ingredient)
                print("2. Cooking Time (mins): ", row[3])
                print("3. Difficulty:", row[4])
                print("**********")

            choice = int(input("Which part of the recipe would you like to update? Enter the corresponding number: ")) 

            if choice == 1:
                number_of_ingredients = int(input("How many ingredients does your recipe have? "))
                
                ingredients = []

                for number_of_ingredients in range(0, number_of_ingredients):
                    ingredient = str(input("Enter an ingredient: "))
                    ingredients.append(ingredient)
                stringified_ingredients = ', '.join(str(item) for item in ingredients)
                cursor.execute('UPDATE Recipes SET ingredients = "' + str(stringified_ingredients) + '" WHERE id = ' + str(row[0]))
                recalculated_difficulty = calc_difficulty(row[3], len(ingredients))
                cursor.execute('UPDATE Recipes SET difficulty = "' + str(recalculated_difficulty) + '" WHERE id = ' + str(row[0]))
                conn.commit()
                print("***** RECIPE UPDATED *****")
                cursor.execute('SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = ' + str(row[0]))
                results = cursor.fetchall()
                for row in results:
                    print("ID: ", row[0])
                    print("Name: ", row[1])
                    print("Ingredients: ", row[2])
                    print("Cooking Time (mins): ", row[3])
                    print("Difficulty:", row[4])
                    print("**********")
                    main_menu(conn, cursor)

            elif choice == 2:
                ingredients = len(row[2].split(', '))
                new_cooking_time = int(input("How long does it take to make this recipe? "))
                cursor.execute('UPDATE Recipes SET cooking_time = ' + str(new_cooking_time) + ' WHERE id = ' + str(row[0]))
                recalculated_difficulty = calc_difficulty(new_cooking_time, ingredients)
                cursor.execute('UPDATE Recipes SET difficulty = "' + str(recalculated_difficulty) + '" WHERE id = ' + str(row[0]))
                conn.commit()
                print("***** RECIPE UPDATED *****")
                cursor.execute('SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = ' + str(row[0]))
                results = cursor.fetchall()
                for row in results:
                    print("ID: ", row[0])
                    print("Name: ", row[1])
                    print("Ingredients: ", row[2])
                    print("Cooking Time (mins): ", row[3])
                    print("Difficulty:", row[4])
                    print("**********")
                    main_menu(conn, cursor)

            elif choice == 3:
                new_difficulty = input("What is the difficulty of this recipe? ")
                if new_difficulty == 'Easy':
                    cursor.execute('UPDATE Recipes SET difficulty = "' + str(new_difficulty) + '" WHERE id = ' + str(row[0]))
                    conn.commit()
                    print("***** RECIPE UPDATED *****")
                    cursor.execute('SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = ' + str(row[0]))
                    results = cursor.fetchall()
                    for row in results:
                        print("ID: ", row[0])
                        print("Name: ", row[1])
                        print("Ingredients: ", row[2])
                        print("Cooking Time (mins): ", row[3])
                        print("Difficulty:", row[4])
                        print("**********")
                        main_menu(conn, cursor)
                elif new_difficulty == 'Medium':
                    cursor.execute('UPDATE Recipes SET difficulty = "' + str(new_difficulty) + '" WHERE id = ' + str(row[0]))
                    conn.commit()
                    print("***** RECIPE UPDATE *****")
                    cursor.execute('SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = ' + str(row[0]))
                    results = cursor.fetchall()
                    for row in results:
                        print("ID: ", row[0])
                        print("Name: ", row[1])
                        print("Ingredients: ", row[2])
                        print("Cooking Time (mins): ", row[3])
                        print("Difficulty:", row[4])
                        print("**********")
                        main_menu(conn, cursor)
                elif new_difficulty == 'Intermediate':
                    cursor.execute('UPDATE Recipes SET difficulty = "' + str(new_difficulty) + '" WHERE id = ' + str(row[0]))
                    conn.commit()
                    print("***** RECIPE UPDATED *****")
                    cursor.execute('SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = ' + str(row[0]))
                    results = cursor.fetchall()
                    for row in results:
                        print("ID: ", row[0])
                        print("Name: ", row[1])
                        print("Ingredients: ", row[2])
                        print("Cooking Time (mins): ", row[3])
                        print("Difficulty:", row[4])
                        print("**********")
                        main_menu(conn, cursor)
                elif new_difficulty == 'Hard':
                    cursor.execute('UPDATE Recipes SET difficulty = "' + str(new_difficulty) + '" WHERE id = ' + str(row[0]))
                    conn.commit()
                    print("***** RECIPE UPDATED *****")
                    cursor.execute('SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = ' + str(row[0]))
                    results = cursor.fetchall()
                    for row in results:
                        print("ID: ", row[0])
                        print("Name: ", row[1])
                        print("Ingredients: ", row[2])
                        print("Cooking Time (mins): ", row[3])
                        print("Difficulty:", row[4])
                        print("**********")
                        main_menu(conn, cursor)
                else:
                    print('Please enter Easy, Medium, Intermediate or Hard')

    def delete_recipe(conn, cursor):
        print("**********")
        cursor.execute("SELECT id, name FROM Recipes")
        results = cursor.fetchall()
        for row in results:
            id = str(row[0])
            name = str(row[1])
            print(id + '. ' + name)
        #cursor.execute('DELETE FROM Recipe WHERE item_id = ' + row[0])
        recipe_to_delete = input('Which recipe would you like to delete? Enter the corresponding number: ')
        #print(recipe_to_delete)
        cursor.execute('DELETE FROM Recipes WHERE id = %s', (recipe_to_delete,))
        conn.commit()
        print("***** RECIPE DELETED *****")

        """  confirm = ''
        
        while confirm != 'Y' or confirm != 'Y' or confirm != 'N' or confirm != 'n' or confirm != 'quit':
            confirm = input('Are you sure you wish to proceed? This can\'t be undone. Type Y or N: ')
            if confirm == 'Y' or confirm == 'y':
                cursor.execute('DELETE FROM Recipes WHERE id = %s', (recipe_to_delete,))
                conn.commit()
                print("***** RECIPE DELETED *****")
                main_menu(conn, cursor)
            elif confirm == 'N' or confirm == 'n':
                #print('Go Back')
                confirm == 'quit'
                main_menu(conn, cursor)
            elif confirm == 'quit':
                main_menu(conn, cursor)
            else:
                print('Please try again, type Y or N and press enter.')
                delete_recipe(conn, cursor)
        main_menu(conn, cursor) """
  

    choice = ''
    while(choice != 'quit'):
        print('What would you like to do? Pick a choice!')
        print('1. Create a recipe')
        print('2. Search a recipe')
        print('3. Update a recipe')
        print('4. Delete a recipe')
        choice = input("Your choice: ")

        if choice == '1':
          #recipe_name = print(input('What is the name of your recipe? '))
          add_recipe(conn, cursor)

        elif choice == '2':
          search_recipe(conn, cursor)

        elif choice == '3':
          update_recipe(conn, cursor)

        elif choice == '4':
          delete_recipe(conn, cursor)
    

main_menu(conn, cursor)