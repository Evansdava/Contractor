from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import os

app = Flask(__name__)


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/my_app_db')
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()

collection = db.collection


@app.route('/')
def index():
    """Return homepage"""
    return render_template('index.html')


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
    collection.insert_one(listing)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
