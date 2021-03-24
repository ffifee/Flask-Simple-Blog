import os

from flask import Flask


def create_app(test_config=None):
    # Kreira i konfigurira app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Ucitaj instance konfiguraciju, ukoliko postoji, kad ne testiramo
        app.config.from_pyfile('config.py', silent=True)
    else:
        # ucitaj test konfiguraciju ukoliko je proslijedena
        app.config.from_mapping(test_config)

    # Utvrdi da folder instance postoji
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Jednostavna stranica koja kaze hello

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
