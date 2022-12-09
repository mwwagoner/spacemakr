from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spacemakr.db"

db = SQLAlchemy()
db.init_app(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# with app.app_context():
#     db.create_all()

@app.before_first_request
def initialize_database():
    db.create_all()

@app.route('/')
def hello():
    return "Hello"

### DB Models

class Products(db.Model):
    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.Text, nullable=False)

    orders = db.relationship(
        'Orders',
        backref = 'products',
        lazy=True
    )

class ManufactureRuns(db.Model):
    runID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer, nullable=False)
    materialsCost = db.Column(db.Float, nullable=False)
    jobCost = db.Column(db.Float, nullable=False)
    status = db.Column(db.Text(9))
    timeToBuild = db.Column(db.Float, nullable=False)

    productID = db.Column(
        db.Integer,
        db.ForeignKey('products.productID'),
        nullable=False
    )

    orders = db.relationship(
        'Orders',
        backref = 'manufactureRuns',
        lazy=True
    )

class Orders(db.Model):
    orderID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    pricePerUnit = db.Column(db.Float)
    brokerFee = db.Column(db.Float)
    status = db.Column(db.Text(8))

    productID = db.Column(
        db.Integer,
        db.ForeignKey('products.productID'),
        nullable = False
    )
    
    runID = db.Column(
        db.Integer,
        db.ForeignKey('manufacture_runs.runID'),
        nullable = False
    )

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.Text(100), nullable=False)
    station = db.Column(db.Text(100), nullable=False)
    quantity = db.Column(db.Integer)

    runID = db.Column(
        db.Integer,
        db.ForeignKey('manufacture_runs.runID'),
        nullable=False
    )

class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.Text(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    runID = db.Column(
        db.Integer,
        db.ForeignKey('manufacture_runs.runID'),
        nullable=False
    )

#############

### Forms

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@app.route('/myform', methods=['GET', 'POST'])
def myform():
    form = MyForm()

    if form.validate_on_submit():
        return '<h1>Yay!</h1>'
        #redirect( url_for('hello') )

    return render_template('myform.html', form=form)

#############