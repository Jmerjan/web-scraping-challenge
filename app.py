from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo, pymongo
import scrape_mars
import time

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017"
mongo = PyMongo(app)

marsdb = mongo.db.marsdb
mars_data = scrape_mars.scrape()
marsdb.update_one({}, mars_data, upsert=True)


@app.route("/")
def index():
    data = mongo.db.marsdb.find_one()
    return render_template("index.html", marsdb=data)


@app.route("/scrape")
def scraper():
    marsdb = mongo.db.marsdb
    mars_data = scrape_mars.scrape()
    marsdb.update_many({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)


