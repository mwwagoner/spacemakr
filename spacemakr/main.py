from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spacemakr.db"

db = SQLAlchemy()
db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.before_first_request
def initialize_database():
    db.create_all()

@app.route('/')
def hello():
    return "Hello"

class Products(db.Model):
    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.Text, nullable=False)

    orders = db.relationship(
        'Orders',
        backref = 'products',
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
        db.ForeignKey(),
        nullable = False
    )

class ManufactureRuns(db.Model):
    runID = db.Column(db.Integer, primary_key=True)
    date = db._Column(db.Date)
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

class Location(db.Model):
    system = db.Column(db.Text(100), nullable=False)
    station = db.Column(db.Text(100), nullable=False)
    quantity = db.Column(db.Integer)

    runID = db.Column(
        db.Integer,
        db.ForeignKey('manufactureRuns.runID'),
        lazy=True
    )