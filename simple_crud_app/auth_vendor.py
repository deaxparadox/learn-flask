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
from .models import Vendor

bp = Blueprint("auth_vendor", __name__, url_prefix="/auth/vendor")


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
                vendor = Vendor(username, generate_password_hash(password))
                db_session.add(vendor)
                db_session.commit()
            except Exception as e:
                error = f"Vendor {username} is already registered"
            else:
                return redirect(url_for("auth_vendor.login"))
        flash(error)
        
    return render_template("auth/vendor/register.html", user_type="Vendor")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        vendor = db_session.query(Vendor).where(Vendor.username==username).one()
        
        # vendor_serializer = UserLoginSerializer(vendor.username, vendor.password)
        
        if vendor is None:
            error = "Incorrect username."
        elif not check_password_hash(vendor.password, password):
            error = 'Incorrect pasword'
            
        if error is None:
            session.clear()
            session['user_id'] = vendor.id
            session['user_type'] = 'vendor'
            return redirect(url_for('auth_vendor.update'))
        
        flash(error)
    return render_template("auth/vendor/login.html", user_type="Vendor")

@bp.route("/update", methods=['GET', 'POST'])
def update():
    user = session.get("user_id", None)
    user_type = session.get("user_type", None)
    if not user or not user_type:
        return redirect(url_for("auth_vendor.login"))
    if request.method == "POST":
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        vendor = db_session.query(Vendor).where(Vendor.id==user).all()[0]
        vendor.first_name = first_name
        vendor.last_name = last_name
        db_session.add(vendor)
        db_session.commit()
        return redirect(url_for('auth_vendor.update'))
    return render_template("auth/vendor/update.html")


        
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_vendor.login"))

@bp.route('/delete')
def delete():
    user_id = session.get("user_id")
    user_type = session.get("user_type")
    # if not user_id or not user_type:
    #     return redirect(url_for("auth_user.login"))
    user = db_session.query(Vendor).where(Vendor.id==user_id).one()
    user.active = False
    # db_session.(user)
    db_session.commit()
    session.clear()
    g.user = None
    g.user_type = None
    return redirect(url_for("auth_user.register"))