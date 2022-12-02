from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spacemakr.db"

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return "Hello"
