from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

DB_USER = "newuser"
DB_PASSWORD = "123"
DB_HOST = "localhost"
DB_NAME = "web_data"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .models import User , Note , Item
    from .home import home
    from .market import market
    from .tasks import tasks
    from .auth import auth
    from .family import family
    from .posts import posts

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(market, url_prefix='/')
    app.register_blueprint(tasks, url_prefix='/')
    app.register_blueprint(family, url_prefix='/')
    app.register_blueprint(posts, url_prefix='/')
    

    return app
