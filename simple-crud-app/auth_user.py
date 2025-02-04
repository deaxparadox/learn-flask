import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from sqlalchemy import text
from .serializer import UserCreateSerializer, UserLoginSerializer
from .db import get_db

bp = Blueprint("auth_user", __name__, url_prefix="/auth/user")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        
        if error is None:
            try:
                db.execute(
                    text(
                        "INSERT INTO user (username, password) VALUES ('%s', '%s')" %
                        (username, generate_password_hash(password))
                   )
                )
                db.commit()
            except Exception as e:
                print(e)
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth_vendor.login"))
        flash(error)
        
    return render_template("auth/user/register.html", user_type="User")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            text("SELECT * FROM user WHERE username = '%s'" % username)
        ).fetchone()
        
        user_serializer = UserLoginSerializer(*user)
        
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user_serializer.password, password):
            error = 'Incorrect pasword'
            
        if error is None:
            session.clear()
            session['user_id'] = user_serializer.id
            return redirect(url_for('hello'))
        
        flash(error)
    return render_template("auth/user/login.html", user_type="User")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    print(user_id)
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            text("SELECT * FROM user WHERE id = %s;" % user_id)
        ).fetchone()
        
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_user.login"))

