from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///currency_check.db"

db = SQLAlchemy(app)

from currency_check.models import models
from currency_check import views
