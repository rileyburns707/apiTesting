"""
main.py
-------
This is a basic flask application. The application stores drinks (non-alcoholic sry)
"""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__) 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
db = SQLAlchemy(app)

class Drink(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(120))

  def __repr__(self):
    # this will be invoked whenever we try to print out the drink in a list
    return f"{self.name} - {self.description}"

@app.route('/')  # endpoint
def index():
  """
  This is the main page
  """
  return "Hello world"

@app.route('/drinks')
def get_drinks():
  """
  This function gets all the rows of drinks from the database
  and saves them into a list of dictionaries
  """
  drinks = Drink.query.all()

  output = []
  for drink in drinks:
    # the end goal is a list of dictionaries
    drink_data = {'name': drink.name, 'description': drink.description}
    output.append(drink_data)

  return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):
  """
  This function creates a route tha allows the data to be filtered 
  by their id. Changing the id in the url will change the data
  being retrieved.
  """
  drink = Drink.query.get_or_404(id)  # gets a drink object
  return {'name': drink.name, 'description': drink.description}  # need to call jsonify if not working with a dictionary 

@app.route('/drinks', methods=['POST'])
def add_drink():
  """
  This function adds a drink to the database
  """
  drink = Drink(name=request.json['name'], description=request.json['description'])
  db.session.add(drink)
  db.session.commit()
  return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
  drink = Drink.query.get(id)
  if drink is None:
    return {"error": "not found"}
  db.session.delete(drink)
  db.session.commit()
  return {"message": "all good baby, drink deleted"}