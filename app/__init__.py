from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from .auth import auth
from .config import Config
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__,
                template_folder='./templates/',
                static_folder='./static/'
                )
    bootstrap = Bootstrap5(app)

    # Trae todas las configuraciones declaradas en el archivo config
    app.config.from_object(Config)
    login_manager.init_app(app)
    app.register_blueprint(auth)
    return app
