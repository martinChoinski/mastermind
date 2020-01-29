import json
from flask import Flask, render_template, redirect, request
from random import randint
from . import app

#use unique game_id and dict to make var session safe 
game_id = 0 
games = {}

@app.route("/")
def home():
    return render_template("mm.html")

@app.route("/start", methods=['POST'])
def start():
    n_pegs = int(request.form["number_of_pegs"])
    n_colors = int(request.form["number_of_colors"])
    global  game_id
    game_id += 3     
    secret = []
    for i in range(n_pegs):
        n = randint(0, n_colors-1)
        secret.append(n)
    
    games[game_id] = secret

    return json.dumps(game_id)

@app.route("/end", methods=['POST'])
def end():
    remove_id = int(request.form["game_id"])
    del games[remove_id]

    return json.dumps(remove_id)

@app.route("/check", methods=['POST'])
def check():
    check_id = int(request.form["game_id"])
    if(check_id in games) :
        return f'game = {check_id}; secret colors = {games[check_id]}'
    else :
        return f'game[{check_id}] not in dictionary'


@app.route("/guess", methods=['POST'])
def guess():
    peg = json.loads(request.form["pegs"])
    post_id = int(request.form["game_id"])
    secret = games[post_id].copy()
    result = []

    if(len(secret) != 4) :
        print(f'corrupt secret master array length = {len(secret)}')

    if(len(peg) != 4) :
        print(f'corrupt posted peg array length = {len(peg)}')

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
