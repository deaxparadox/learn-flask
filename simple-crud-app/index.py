from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
    url_for
)

bp = Blueprint("index", __name__, url_prefix="/")

@bp.get("")
def hello():
    user_type = session.get("user_type")
    user_id = session.get("user_id")
    if user_id and user_type:
        if user_type == 'vendor':
            return redirect(url_for("auth_vendor.update"))
        return redirect(url_for("auth_user.update"))
    return render_template("index.html")
