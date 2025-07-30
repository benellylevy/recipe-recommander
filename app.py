import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from difflib import SequenceMatcher
from textblob import TextBlob

# Function to correct spelling mistakes in the input text
# Using TextBlob library to do the magic
def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())

app = Flask(__name__)

# Load API key from .env file - yes we’re doing it the proper way
load_dotenv()  # טוען את המפתח מהקובץ .env

API_KEY = os.getenv("SPOONACULAR_API_KEY")

# Cache for storing search results to avoid making repeated API calls
# This helps speed things up and save on API usage
query_cache = {}  # מחוץ לפונקציות - מטמון לתוצאות חיפושים כדי למנוע קריאות חוזרות ל-API

# Load favorite recipes from a JSON file if it exists
# This way we keep user favorites between sessions
favorites_file = 'favorites.json'
if os.path.exists(favorites_file):
    with open(favorites_file, 'r') as f:
        favorite_recipes = json.load(f)
else:
    favorite_recipes = []

# Function to do fuzzy matching between two strings (ingredients)
# This helps to compare ingredients even if they are slightly different or misspelled
def fuzzy_match(a, b):
    return SequenceMatcher(None, a, b).ratio() > 0.6

# Function to save a favorite recipe to the JSON file
# Adds the recipe only if it's not already saved
def save_favorite(recipe):
    if recipe not in favorite_recipes:
        favorite_recipes.append(recipe)
        with open(favorites_file, 'w') as f:
            json.dump(favorite_recipes, f, indent=2)

# Main route for the app - shows the search form and displays recipe results
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 🧾 Reading user input - up to three ingredients, cuisine type, diet, pantry items, and intolerances
        ing1 = request.form.get('ingredient1')
        ing2 = request.form.get('ingredient2')
        ing3 = request.form.get('ingredient3')

        selected_cuisine = request.form.get('cuisine')
        selected_diet = request.form.get('diet')
        pantry_items = request.form.getlist('pantry_items')
        intolerances = request.form.getlist('intolerances')

        # Combine all ingredients into one list after trimming spaces
        manual_ingredients = [ing1, ing2, ing3]
        manual_ingredients = [i.strip() for i in manual_ingredients if i and i.strip()]
        user_ingredients = manual_ingredients + pantry_items
        # Create a comma-separated string to send to the API
        ingredient_query = ','.join(manual_ingredients)

        # Calling the Spoonacular API to get recipes based on what the user typed
        url = 'https://api.spoonacular.com/recipes/complexSearch'
        params = {
            'includeIngredients': ingredient_query,
            'cuisine': selected_cuisine,
            'number': 10,
            'addRecipeInformation': True,
            'instructionsRequired': True,
            'apiKey': API_KEY
        }

        # If the user selected a diet filter, add it to the API parameters
        if selected_diet:
            params['diet'] = selected_diet
        # If there are any intolerances, add them as a parameter to filter out recipes
        if intolerances:
            params['intolerances'] = ','.join(intolerances)

        # Create a cache key based on the search parameters to speed up repeated queries
        query_key = '|'.join(sorted(manual_ingredients)) + f"|{selected_cuisine}|{selected_diet if selected_diet else 'no_diet'}|{','.join(intolerances)}"

        # Check if results are already in cache, otherwise call the API
        if query_key in query_cache:
            results = query_cache[query_key]
        else:
            response = requests.get(url, params=params)
            data = response.json()
            results = data.get('results', [])
            query_cache[query_key] = results

        # Build a list of recipes to display, including ingredients as returned by the API
        scored = []
        for recipe in results:
            scored.append({
                'title': recipe['title'],
                'image': recipe['image'],
                'sourceUrl': recipe['sourceUrl'],
                'extendedIngredients': recipe.get('extendedIngredients', []),
                'diets': recipe.get('diets', [])
            })

        # Render the results page with the list of recipes
        return render_template("index.html", recipes=scored)
    else:
        # If GET request, just show the search form without results
        return render_template('index.html', recipes=None)


# Route to show the favorites page - displays all saved favorite recipes
@app.route('/favorites')
def show_favorites():
    return render_template('favorites.html', favorites=favorite_recipes)


# Route to save a favorite recipe manually selected by the user
@app.route('/save_favorite', methods=['POST'])
def add_to_favorites():
    title = request.form.get('title')
    image = request.form.get('image')
    url = request.form.get('url')
    recipe = {
        'title': title,
        'image': image,
        'sourceUrl': url
    }
    save_favorite(recipe)  # Save the recipe to the favorites JSON file
    return '', 204  # Return empty response with 204 No Content status


# Route to check spelling of a single ingredient (POST JSON)
# Returns whether the spelling is correct and suggests a correction if not
@app.route('/check_spelling', methods=['POST'])
def check_spelling():
    data = request.get_json()
    ingredient = data.get('ingredient', '')
    if not ingredient:
        return jsonify({'correct': True})

    corrected = correct_spelling(ingredient)
    if corrected.strip().lower() == ingredient.strip().lower():
        return jsonify({'correct': True})
    else:
        return jsonify({'correct': False, 'suggestion': corrected})
    
if __name__ == '__main__':
    app.run(debug=True)  # הפעלת השרת במצב דיבאג
