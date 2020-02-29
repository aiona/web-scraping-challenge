from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from jinja2 import Template
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    #Find one record of data from MongoDB
    mars_dict = mongo.db.collection.find_one()
    print(mars_dict)

    #Return template and data
    return render_template("index.html", mars_info=mars_dict)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    #Run the scrape function
    news = scrape_mars.scrapeNews()
    print(news)
    mars_data = scrape_mars.scrape()

    #Update the Mongo database using update and upsert=True
    mongo.db.collection.update_one({}, mars_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


