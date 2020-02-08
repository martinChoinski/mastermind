import os, sqlite3
from . import app    

DATABASE=os.path.join(app.instance_path, 'mm.sqlite')

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    db=connect_db()
    with app.open_resource('schema.sql') as f:
         db.executescript(f.read().decode('utf8'))

def new_game(game,ip) :
    db = connect_db()
    cur = db.cursor()
    sql = "INSERT INTO games (ip,game) VALUES(?,?)"
    cur.execute(sql,(str(ip),str(game)))
    game_id = cur.lastrowid
    db.commit()
    db.close()
    return game_id

def get_game(game_id) :
    db = connect_db()
    cur = db.cursor()
    sql = "SELECT game FROM games WHERE id = ?"
    # print(f'game_id = {str(game_id)}')
    cur.execute(sql,(str(game_id),))
    row = cur.fetchone()
    db.close()
    return row[0]

def end_game(game_id) :
    db = connect_db()
    cur = db.cursor()
    sql = "DELETE FROM games WHERE id = ?"
    cur.execute(sql,(str(game_id),))
    db.commit()
    db.close()
    return game_id

