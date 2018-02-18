from flask import Flask

from .views import views


def create_app(name=__name__, settings_override={}):
    app = Flask(name, template_folder='templates/')

    config = '{0}.app_config'.format(__name__)

    app.config.from_object(config)
    app.register_blueprint(views)

    return app
