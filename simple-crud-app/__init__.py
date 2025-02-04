import os
from flask import (
    Flask, g, 
    redirect, url_for, 
    render_template, session
)
from sqlalchemy import text

# app factory function
def create_app(test_config=None):
    # creat and configure the app
    app = Flask(
        __name__, 
        instance_relative_config=True
    )

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
    
    
    # a simple page that says hello
    @app.route("/")
    def hello():
        user_type = session.get("user_type")
        user_id = session.get("user_id")
        if user_id and user_type:
            if user_type == 'vendor':
                return redirect(url_for("auth_vendor.update"))
            return redirect(url_for("auth_user.update"))
        return render_template("index.html")
    
    from .db import init_app, get_db
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
    
    from . import auth_user, auth_vendor
    app.register_blueprint(auth_user.bp)
    app.register_blueprint(auth_vendor.bp)

    return app