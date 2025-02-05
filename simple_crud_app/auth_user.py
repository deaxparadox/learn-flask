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
from .database import db_session
from .models import User

bp = Blueprint("auth_user", __name__, url_prefix="/auth/user")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        
        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        
        if error is None:
            try:
                user = User(username, generate_password_hash(password))
                db_session.add(user)
                db_session.commit()
            except Exception as e:
                error = f"Vendor {username} is already registered"
            else:
                return redirect(url_for("auth_user.login"))
        flash(error)
        
    return render_template("auth/user/register.html", user_type="User")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db_session.query(User).where(User.username==username).one()
        
        # vendor_serializer = UserLoginSerializer(vendor.username, vendor.password)
        
        if not user.active:
            error ="Inactive vendor, contact administrator"
            flash(error)
            return redirect(url_for("auth_vendor.register"))
        
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = 'Incorrect pasword'
            
        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['user_type'] = 'user'
            return redirect(url_for('auth_user.update'))
        
        flash(error)
    return render_template("auth/user/login.html", user_type="User")

@bp.route("/update", methods=['GET', 'POST'])
def update():
    user_id = session.get("user_id", None)
    user_type = session.get("user_type", None)
    if not user_id or not user_type:
        return redirect(url_for("auth_vendor.login"))
    if request.method == "POST":
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        user = db_session.query(User).where(User.id==user_id).one()
        user.first_name = first_name
        user.last_name = last_name
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('auth_user.update', user_type='User'))
    return render_template("auth/user/update.html", user_type='User')


        
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_user.login"))

@bp.route('/delete')
def delete():
    user_id = session.get("user_id")
    user_type = session.get("user_type")
    # if not user_id or not user_type:
    #     return redirect(url_for("auth_user.login"))
    user = db_session.query(User).where(User.id==user_id).one()
    user.active = False
    # db_session.(user)
    db_session.commit()
    session.clear()
    g.user = None
    g.user_type = None
    return redirect(url_for("auth_user.register"))