# zahash-simple-api.herokuapp.com

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from simple_api import routes
