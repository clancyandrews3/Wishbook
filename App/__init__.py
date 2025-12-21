from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)               # Initialize flask application
app.config.from_object(Config)      # Setup configuration from config.py file

login = LoginManager(app)           # Used for managing login functionality
login.login_view = 'login'          # Sets endpoint for login rerouting

db = SQLAlchemy(app)                # Initialize db from flask db system
migrate = Migrate(app, db)          # Setup migration functionality

from App import routes, models

