#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template, redirect, session
from icecream import ic
from random import choice
from os import getenv

# Set output level
if getenv("VERBOSE") is not None: verbose = True
else: verbose = False
if getenv("DEBUG") is not None:
    debug = True
    verbose = True
else: debug = False

# Open the file and read each line
file_path = 'data/prompts.txt'
prompts = []
with open(file_path, 'r') as file:
    for line in file:
        prompts.append(line.strip())

def pickPrompt():
    # give prompt for players
    return choice(prompts)

games = {}
# Each game is a dict entry like:
# {"Game12":{"Players":[], "Prompt":"Fire ____"}}

# Players are like:
# {"Bob":{"Points":5, "Answer":"Fart"}}

app = Flask(__name__)
app.secret_key = "Setec Astronomy"  # or set a static secret key

@app.route('/', methods=['GET','POST'])
def index():
    return redirect('setup', code=302)

@app.route('/setup', methods=['GET','POST'])
def setup():
    return render_template('setup.html')

@app.route('/game', methods=['GET','POST'])
def game():
    if request.method == "GET": # really ought to get here by POST
        return redirect("setup", code=302)
    # set up the player/game
    if debug: ic(request.form)
    try:
        name = request.form['name']
        gameId = request.form['gameId']
    except Exception as ex:
        ic(f"Couldn't set player up the right way because {ex}")
        name = "Guest"
        gameId = "ThereCanBeOnlyOne"
    global games
    if gameId in games: # add player to game or
        games[gameId]["Players"][name] = {"Points":0, "Answer":""}
    else: # create a new game
        games[gameId] = {"Players":{name:{"Points":0, "Answer":""}}}
    if debug: ic(games)
    session['Name'] = name
    # session['Points'] = 0
    session['GameId'] = gameId
    return render_template('game.html', name=session["Name"], gameId=session["GameId"])

@app.route('/poll', methods=['POST'])
def handle_request():
    global games
    # Extract data sent by client
    if verbose:
        try:
            ic(session)
        except:
            pass
    data = request.json["payload"]
    if verbose: ic('Received data from client:', data)
    if data["Type"] == "Start": # new? get the setup info
        prompt = pickPrompt()
        if verbose: ic(f"Sending prompt {prompt}")
        return jsonify({"Type":"Prompt", "Prompt":prompt})
    elif data["Type"] == "Answer": # sending an answer? update the game
        games[session["gameId"]]["Player"]["Answer"] = data["Message"]
        return jsonify({"Update":"FIXME player answer"})
    else:
        return jsonify("Answer")

if __name__ == '__main__':
    app.run(debug=True)
