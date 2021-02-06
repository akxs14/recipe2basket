from flask import Flask, jsonify
import json
from flask import render_template, request
import requests
from bs4 import BeautifulSoup

recipes_list={}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello lista!'

@app.route('/add_recipe', methods=['GET'])
def add_recipe():
    return render_template("add_list.html")


@app.route('/list_recipes', methods=['GET'])
def list_recipes():
    return render_template("shopping_list.html", shopping_list=recipes_list)


@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    form_data = request.form
    response = requests.get(url=form_data["recipe_link"])
    results_soup = BeautifulSoup(response.content, 'html.parser')

    ingredient_list = results_soup.find('div', attrs={"class": "ingredients-list"})
    ingredients = [ingr.text for ingr in ingredient_list.find_all("li")]
    recipe = results_soup.find('title').text.split("|")[0]

    recipes_list[recipe] = ingredients

    return render_template("shopping_list.html", shopping_list=recipes_list)


@app.route('/shopping_list', methods=['GET'])
def shopping_list():
    all_ingredients = recipes_list.values()
    basket = {}

    for recipe_ingredients in all_ingredients:

        for item in recipe_ingredients:
            if item.split(" ")[2] == "g":
                print("split")
                quantity_grams = item.split(" ")[1]
                food = " ".join(item.split(" ")[3:])

                if food in basket:
                    basket[food] += quantity_grams
                else:
                    basket[food] = quantity_grams

            elif "spoon " in item.split(" ")[2]:
                food = " ".join(item.split(" ")[3:])    

                if food in basket:
                    basket[food] += 30
                else:
                    basket[food] = 30

            else:
                basket[item] = ""

    return str(basket)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")