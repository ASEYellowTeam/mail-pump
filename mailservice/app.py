import os
from flask import Flask
from mailservice.database import db
from mailservice.views import blueprints


def create_app():
    app = Flask(__name__)

    # App
    # TODO: What the hell! Are they needed? And why we use 'A SECRET KEY'?
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mail-service.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress pytest warning

    # Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        blueprint.app = app

    # Init database
    db.init_app(app)
    db.create_all(app=app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5003, debug=True)
