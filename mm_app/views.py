import json
from flask import Flask, render_template, redirect, request
from random import randint
from . import app
from .db import new_game, get_game, end_game


@app.route("/")
def home():
    return render_template("mm.html")

@app.route("/start", methods=['POST'])
def start():
    n_pegs = int(request.form["number_of_pegs"])
    n_colors = int(request.form["number_of_colors"])

    secret = []
    for i in range(n_pegs):
        n = randint(0, n_colors-1)
        secret.append(n)

    game_id = new_game(secret,request.remote_addr)

    return json.dumps(game_id)

@app.route("/end", methods=['POST'])
def end():
    game_id = int(request.form["game_id"])
    end_game(game_id)

    return json.dumps(game_id)


@app.route("/guess", methods=['POST'])
def guess():
    peg = json.loads(request.form["pegs"])
    game_id = int(request.form["game_id"])
    # print(f'game_id = {game_id}')
    secret = json.loads(get_game(game_id))
    result = []

    for i in range(len(peg)):
        if peg[i] == secret[i] :
            result.append(1)
            peg[i] = -1
            secret[i] = -2

    for i in range(len(peg)):
        for j in range(len(secret)):
            if peg[i] == secret[j] :
                result.append(0)
                peg[i] = -1
                secret[j] = -2
                break

    return json.dumps(result)


