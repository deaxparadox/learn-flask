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
    return render_template("index.html")
