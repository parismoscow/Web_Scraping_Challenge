import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

sys.setrecursionlimit(2000)
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mission_to_mars'
mongo = PyMongo(app)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_facts_data = scrape_mars.scrape()
    mars.update({}, mars_facts_data, upsert=True)
    return redirect('/', code=302)


@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


if __name__ == "__main__":
    app.run(debug=True)
