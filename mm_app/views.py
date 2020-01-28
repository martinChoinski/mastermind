import json
from flask import Flask, render_template, redirect, request
from random import randint
from . import app

secret = []

@app.route("/")
def home():
    return render_template("mm.html")

@app.route("/start", methods=['POST'])
def start():
    n_pegs = int(request.form["number_of_pegs"])
    n_colors = int(request.form["number_of_colors"])
    
    secret.clear()
    for i in range(n_pegs):
        n = randint(0, n_colors-1)
        secret.append(n)

    return f'secret colors = {secret}'

@app.route("/guess", methods=['POST'])
def guess():
    peg = json.loads(request.form["pegs"])
    secret_peg = secret.copy()
    result = []

    if(len(secret_peg) != 4) :
        print(f'corupt secret_peg array length = {len(secret_peg)}')

    if(len(peg) != 4) :
        print(f'corupt posted peg array length = {len(peg)}')

    
    for i in range(len(peg)):
        if peg[i] == secret_peg[i] :
            result.append(1)
            peg[i] = -1
            secret_peg[i] = -2

    for i in range(len(peg)):
        for j in range(len(secret_peg)):
            if peg[i] == secret_peg[j] :
                result.append(0)
                peg[i] = -1
                secret_peg[j] = -2
                break

    return json.dumps(result)
