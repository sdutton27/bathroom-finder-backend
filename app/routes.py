from flask import render_template
from app import app

@app.route('/')
def homePage():
    return render_template('index.html')