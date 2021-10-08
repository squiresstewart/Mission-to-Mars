from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define routes
# mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection
# in our database, which we will create when we convert our Jupyter scraping
# code to Python Script. We will also assign that path to themars variable for use later.
# return render_template("index.html" tells Flask to return an HTML template using an index.html file
# , mars=mars) tells Python to use the "mars" collection in MongoDB.

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# the next function will set up our scraping route. This route will be the "button" of the web application
# @app.route(“/scrape”) defines the route that Flask will be using. This route, “/scrape”, will run the
# function that we create just beneath it. The next lines allow us to access the database,
# scrape new data using our scraping.py script, update the database, and return a message when successful.

@app.route("/scrape")
def scrape():
   # assign a new variable that points to our Mongo database: mars = mongo.db.mars
   mars = mongo.db.mars
   # Next line creates a new variable to hold the newly scraped data: mars_data = scraping.scrape_all().
   # In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
   mars_data = scraping.scrape_all()
   # we need to update the database using .update() with the new data.
   # Syntax .update(query_parameter, data, options)
   # step 1: add an empty JSON object with {} in place of the query_parameter.
   # step 2: use the data we have stored in mars_data.
   # step 3 the option we'll include is upsert=True. This indicates to Mongo to
   # create a new document if one doesn't already exist, and new data will always be saved
   mars.update({}, mars_data, upsert=True)
   # step 4 : add a redirect after successfully scraping the data: return redirect('/', code=302).
   # This will navigate our page back to / where we can see the updated content.
   return redirect('/', code=302)

# to tell Flask to run:
if __name__ == "__main__":
   app.run()
