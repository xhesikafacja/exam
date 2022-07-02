from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session['user_id']
    }
    return render_template('new_recipe.html', user= User.get_by_id(data))

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "location": request.form["location"],
        "description": request.form["description"],
        "numberOf": int(request.form["numberOf"]),
        "date_made": request.form["date_made"],
        "user_id": session["user_id"],
        "user_fullname": session["full_name"],
    }
    Recipe.save(data)
    return redirect('/dashboard')


#@app.route('/destroy/recipe/<int:id>')
#def destroy_recipe(id):
 #   if 'user_id' not in session:
    #     return redirect('/logout')
    # data = {
    #     "id": id
    # }
    # clickedRecipe = Recipe.get_one(data)
    # print(clickedRecipe)
    # if clickedRecipe['user_id'] == session['user_id']:
    #     Recipe.destroy(data)
    #     return redirect ('/dashboard')
    # return redirect('/dashboard')


@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/')


@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "recipe_id": id
    }
    userData = {
        "user_id": session['user_id']
    }
    clickedRecipe = Recipe.getUsersWhoLiked(data)
    print(clickedRecipe)
    return render_template('show_recipe.html', recipe = clickedRecipe, user=User.get_by_id(userData))



@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "recipe_id": id
    }
    userData = {
        "user_id": session['user_id']
    }
    return render_template('edit_recipe.html', edit = Recipe.get_one(data), user=User.get_by_id(userData))



@app.route('/update/recipe/', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    
    data = {
        "location": request.form["location"],
        "description": request.form["description"],
        "numberOf": int(request.form["numberOf"]),
        "date_made": request.form["date_made"],
        "recipe_id": request.form["id"],
    }
    Recipe.update(data)
    return redirect('/dashboard')


@app.route('/recipe/<int:id>/like', methods=['GET','PUT'])
def like_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'recipe_id': id,
        'user_id': session['user_id']
    }
    Recipe.addLike(data)
    updatedRecipe = Recipe.getUsersWhoLiked(data)
    updatedData = {
        'recipe_id': id,
        'dontTrust': updatedRecipe.dontTrust
    }

    Recipe.updateLike(updatedData)
    return render_template('show_recipe.html', recipe=updatedRecipe,  user=User.get_by_id(data))

@app.route('/recipe/<int:id>/unlike', methods=['GET','PUT'])
def unlike_recipe(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'recipe_id': id,
        'user_id': session['user_id'],
    }
    User.unLike(data)
    updatedRecipe = Recipe.getUsersWhoLiked(data)
    updatedData = {
        'recipe_id': id,
        'dontTrust': updatedRecipe.dontTrust
    }
    Recipe.updateLike(updatedData)
    return render_template('show_recipe.html', recipe=updatedRecipe,  user=User.get_by_id(data))
