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