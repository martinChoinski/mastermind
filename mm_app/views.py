from flask import Flask, render_template
from . import app

@app.route("/")
def home():
    return render_template("mm.html")

@app.route("/guess", methods=['POST'])
def home():
    return render_template("mm.html")
