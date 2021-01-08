from flask_cors import CORS
from flask import Flask, jsonify, request, redirect
from flask_pymongo import PyMongo
from bson import Binary, Code
from bson.json_util import dumps
from dotenv import load_dotenv
import os

#env. variables
load_dotenv()

# flask app with CORS open
app = Flask(__name__)
CORS(app)

# configuring mongo
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# setting collections
db_operations = mongo.db.quotes

# core random generation route


@app.route('/random-quote')
def read_with_filter():
    # grabs 1 random sample
    quote = db_operations.aggregate([{"$sample": {"size": 1}}])
    output = None
    for i in quote:
        output = dumps(i)
    return output

# could use being quotes/:author but grabs an author's quotes


@app.route('/quotes/')
def author_quotes():
    filt = {'author': request.args['author']}
    author_quotes = db_operations.find(filt)
    output = [{'text': quote['text'], 'author': quote['author']}
              for quote in author_quotes]
    return jsonify(output)


# debug needs to go off for prod
if __name__ == '__main__':
    app.run(debug=True)
