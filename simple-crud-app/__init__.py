import os
from flask import (
    Flask, g, 
    redirect, url_for, 
    render_template, session
)
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

from . import settings
    
from . import auth_user, auth_vendor, index
from .db import init_app, get_db


# app factory function
def create_app(test_config=None):
    # creat and configure the app
    app = Flask(
        __name__, 
        instance_relative_config=True
    )
    app.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config it passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    init_app(app)
    
    @app.before_request
    def check_user_login_type():
        user_id = session.get("user_id")
        user_type = session.get("user_type")
        print(user_id, user_type)

        if not user_id and not user_type:
            g.user = None
            g.user_type = None
        else:
            g.user = get_db().execute(
                text("SELECT * FROM %s WHERE id = %s;" % (user_type, user_id))
            ).fetchone()
            g.user_type = user_type

    app.register_blueprint(index.bp)
    app.register_blueprint(auth_user.bp)
    app.register_blueprint(auth_vendor.bp)


    return app