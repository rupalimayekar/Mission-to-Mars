
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

mongo = PyMongo(app)

@app.route('/')
def index():
    # Get the data from the mongo db
    data = mongo.db.mars.find_one()
    
    print(data)

    # Render an index.html template with the data
    return render_template("index.html", mars_data=data)


@app.route('/scrape')
def scrape_mars_data():
    # 1. find the collection that you are going to insert scraped data to and set it to a variable.
    data = scrape()

    # 2. scrape your url here, and set it to a variable. Hint: You will be calling a function from scrape.py.
    mars_db = mongo.db.mars

    # 3. update your database with your new data.
    mars_db.update({}, data, upsert=True)

    # 4. redirect your url back to the route.
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
