from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def hello_world():
    app.logger.info("Hello to flask")
    return render_template("index.html")

@app.get("/<name>")
def hello_name(name = None):
    app.logger.info(f"Hello to {name}")
    return render_template("index_name.html", name=name)