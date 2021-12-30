# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api, apidoc, Resource, reqparse
from flask_cors import CORS

# import models
# from apis.delivery import deliveryfreq
# from apis.auth import Auth

import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    import models
    from apis.delivery import deliveryfreq
    from apis.auth import Auth
    app.config.from_object(config)  # config 에서 가져온 파일을 사용합니다.

    db.init_app(app)  # SQLAlchemy 객체를 app 객체와 이어줍니다.
    Migrate().init_app(app, db)

    app.secret_key = "secret"
    app.config['SESSION_TYPE'] = 'filesystem'

    CORS(app)

    # from . import models
    from apis.delivery import deliveryfreq
    api = Api(app)
    api.add_namespace(deliveryfreq)
    api.add_namespace(Auth, '/auth')

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0', debug=True, port=3333)
