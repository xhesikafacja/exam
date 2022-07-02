from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name="recipes"
    def __init__(self, db_data):
        self.id = db_data['id']
        self.location = db_data['location']
        self.description = db_data['description']
        self.date_made = db_data['date_made']
        self.numberOf = db_data['numberOf']
        self.user_id = db_data['user_id']
        self.creator= db_data['creator']
        self.dontTrust = db_data['dontTrust']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.users_who_liked = []
        self.users_who_likedFullName = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (location, description, date_made, numberOf, creator,  user_id) VALUES (%(location)s, %(description)s, %(date_made)s, %(numberOf)s, %(user_fullname)s , %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(recipe_id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        return  cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET location=%(location)s, description =  %(description)s, date_made=%(date_made)s, numberOf=%(numberOf)s WHERE recipes.id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def updateLike(cls, data):
        query = "UPDATE recipes SET dontTrust=%(dontTrust)s WHERE recipes.id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_all(cls):
        query= "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_recipes= []
        for row in results:
            all_recipes.append(row)
        return all_recipes
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['location'])<1:
            flash('Location is required!', "recipe")
            is_valid=False
        if len(recipe['description'])<1:
            flash('Enter what happened!', "recipe")
            is_valid=False
        if recipe['date_made'] == "":
            flash('Please enter a date', "recipe")
            is_valid=False
        if int(recipe['numberOf'], 10) < 1:
            flash('Number of Sasquatches should be bigger than 1', "recipe")
            is_valid=False
        return is_valid
    
    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (recipes_id,users_id) VALUES (%(recipe_id)s,%(user_id)s);"
        return connectToMySQL('recipes').query_db(query,data)



    @classmethod
    def getUsersWhoLiked(cls, data):
        query = "SELECT * FROM likes LEFT JOIN recipes ON likes.recipes_id = recipes.id LEFT JOIN users ON likes.users_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        myRecipe = Recipe.get_one(data)
        for row in results:
            myRecipe.users_who_liked.append(row['email'])
            myRecipe.users_who_likedFullName.append(row['first_name'] + ' ' + row['last_name'])
        myRecipe.dontTrust=len(myRecipe.users_who_liked)
        return myRecipe