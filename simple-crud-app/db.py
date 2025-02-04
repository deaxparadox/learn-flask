from sqlalchemy import create_engine, text
from datetime import datetime
import pymysql

import click
from flask import current_app, g


engine = create_engine('mysql+pymysql://paradox:796300@localhost:3306/flask', echo=True)



def get_db():
    if "db" not in g:
        g.db = engine.connect()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()
        

def init_db():
    with current_app.open_resource("schema.sql") as f:
        with get_db() as db:
            # query = text(f.read().decode('utf-8'))
            db.execute(text("DROP TABLE IF EXISTS user;"))
            db.execute(text("DROP TABLE IF EXISTS vendor;"))
            db.execute(text('''CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name varchar(50),
                last_name VARCHAR(50)
            );'''))
            db.execute(text('''CREATE TABLE vendor (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name varchar(50),
                last_name VARCHAR(50)
            );'''))
            
            db.commit()
        
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_data():
    with get_db() as db:
        db.execute(text("INSERT INTO user(username, password) VALUES ('testuser1', '136900');"))
        db.execute(text("INSERT INTO vendor (username, password) VALUES ('testvendor1', '136900');"))
        db.commit()

@click.command("init-test-data")
def init_test_data():
    """Generate testuser1 and testvendor1"""
    init_data()
    click.echo("Populated test data")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_test_data)