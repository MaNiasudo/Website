from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KEY'

    from .home import home
    from .market import market
    from .tasks import tasks

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(market, url_prefix='/')
    app.register_blueprint(tasks, url_prefix='/')

    return app