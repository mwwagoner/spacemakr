from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spacemakr.db"

db.init_app(app)

class Products(db.Model):
    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

app.route('/hello')
def hello():
    return "Hello"