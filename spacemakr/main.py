from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField, DateField, FloatField
from wtforms.validators import DataRequired

import os

app = Flask(__name__)

# Give the app the URI for the sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spacemakr.db"

# Generate a secret key that is later used by csrf protection in the web forms as well as the session
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Tell flask_session to use the file system for session data
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "spacemakr/instance"

app.config["SESSION_PERMANENT"] = False

db = SQLAlchemy()
db.init_app(app)

# Tell flask_session which SQLAlchemy instance to use
# app.config["SESSION_SQLALCHEMY"] = db

""" 
Name of the table in the above DB that will hold the session data 
This table must be configured as:
id - INTEGER PK
session_id - TEXT
data - BLOB
expiry - INTEGER
"""
# app.config["SESSION_SQLALCHEMY_TABLE"] = "session_data"

# Create the session object and initialize the app with it
sess = Session()
sess.init_app(app)

# with app.app_context():
#     db.create_all()

@app.before_first_request
def initialize_database():
    db.create_all()

@app.route('/')
def index():
    return render_template('base.html')

### DB Models

class Products(db.Model):
    __tablename__ = 'products'
    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.Text, nullable=False, unique=True)

    orders = db.relationship(
        'Orders',
        backref = 'products',
        lazy=True
    )

    def __init__(self, productName):
        
        self.productName = productName

class ManufactureRuns(db.Model):
    __tablename__ = 'manufacture_runs'
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
    __tablename__ = 'orders'
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
    __tablename__ = 'location'
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
    __tablename__ = 'materials'
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

class ProductsAddForm(FlaskForm):
    product_id = HiddenField('Product id')
    product_name = StringField('Product name', validators=[DataRequired()])
    submit = SubmitField('Submit record')

class ManufactureAddForm(FlaskForm):
    run_id = HiddenField('Run id')
    date = DateField('Date')
    product_id = IntegerField('Product id', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    materials_cost = FloatField('Materials cost', validators=[DataRequired()])
    job_cost = FloatField('Job cost', validators=[DataRequired()])
    time_to_build = FloatField('Time to build')

# class MyForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])
#     age = IntegerField('age', validators=[DataRequired()])

# @app.route('/myform', methods=['GET', 'POST'])
# def myform():
#     form = MyForm()

#     if form.validate_on_submit():
#         name = form.name.data
#         age = form.age.data

#         # all_the_data = [name, age]

#         # return redirect( url_for('hello', ata=all_the_data) )
#         return redirect( url_for('hello', name=name, age=age) )
    

#     return render_template('myform.html', form=form)

#############

### Products

@app.route('/products')
def products():
    try:
        products = Products.query.all()
        return render_template('list.html', products=products)
    except Exception as e:
        # e holds a description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is borken.</h1>'
        return hed + error_text

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductsAddForm()

    if form.validate_on_submit():
        try:
            productName = form.product_name.data

            record = Products(productName)

            db.session.add(record)
            db.session.commit()
        except Exception as e:
            error_text = "<p>The error:<br>" + str(e) + "</p>"
            hed = '<h1>Something is borken.</h1>'
            return hed + error_text

        return redirect( url_for('products') )
    
    return render_template('productsform.html', form=form)
        
#############

### Manufacture Runs

@app.route('/add_manufacture', methods=['GET', 'POST'])
def add_manufacture():
    form = ManufactureAddForm()

    if form.validate_on_submit():
        try:
            date = form.date.data
            productID = form.product_id.data
            quantity = form.quantity.data
            materialsCost = form.materials_cost.data
            jobCost = form.job_cost.data
            timeToBuild = form.time_to_build.data

            return "Added"
        except Exception as e:
            error_text = "<p>The error:<br>" + str(e) + "</p>"
            hed = '<h1>Something is borken.</h1>'
            return hed + error_text
    
    return render_template('manufactureform.html', form=form)

#############

### Locations

@app.route('/locations')
def locations():
    try:
        locations = Location.query.all()
        return render_template('listlocations.html', locations=locations)
    except Exception as e:
        # e holds a description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is borken.</h1>'
        return hed + error_text

#############

# Test code to pass session variables between routes
# @app.route('/set')
# def set():
#     session['key'] = 'Kiss this'
#     return 'ok'

# @app.route('/get')
# def get():
#     return session.pop('key', 'not set')