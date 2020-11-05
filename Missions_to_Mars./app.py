from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import EJ_scrape
# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route('/')
def home():


    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=destination_data)


# Run the scrape function
@app.route("/scrape")
def scrape():
    #Run the scrape function
    #-------hemisphere_image_urls
    mars_data = EJ_scrape.scrape_info()

     # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
