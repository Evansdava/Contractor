from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/my_app_db')
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()
listings = db.listings


@app.route('/')
def index():
    """Return homepage"""
    return render_template('index.html', listings=listings.find())


@app.route('/new')
def new_listing():
    """Return new listing creation page"""
    return render_template('new_listing.html')


@app.route('/new', methods=['POST'])
def create_listing():
    """Allow the user to create a new listing"""
    listing = {
        'name': request.form.get('name'),
        'price': request.form.get('price')
    }
    listings.insert_one(listing)
    return redirect(url_for('index'))


@app.route('/listings/<listing_id>')
def listings_show(listing_id):
    """Show a single listing."""
    listing = listings.find_one({'_id': ObjectId(listing_id)})
    return render_template('listings_show.html', listing=listing)


if __name__ == '__main__':
    app.run(debug=True)
