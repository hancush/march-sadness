from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from .views import views

def create_app(name=__name__, settings_override={}):
    app = Flask(name)
    config = '{0}.app_config'.format(__name__)
    app.config.from_object(config)

    for k,v in settings_override.items():
        app.config[k] = v

    app.register_blueprint(views)

    return app
