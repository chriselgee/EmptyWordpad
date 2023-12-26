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

games = {}

# Open the file and read each line into prompts
file_path = 'data/prompts.txt'
prompts = []
with open(file_path, 'r') as file:
    for line in file:
        prompts.append(line.strip())

def pickPrompt():
    # give prompt for players
    return choice(prompts)

def genUpdate(gameId, sanitized=True):
    # generate an update to push to players, w/o others' prompts if the round isn't over
    global games
    update = []
    # ic(games, gameId, sanitized)
    for i in range(len(games[gameId]["Players"])):
        ic(games[gameId]["Players"])
        player = games[gameId]["Players"][i]
        update.append(player)
        if sanitized:
            update[i]["Prompt"] = "Entered"
    if verbose: ic(update)
    return update

# Each game is a dict entry like:
# {"Game12":{"Players":[], "Prompt":"Fire ____"}}

# Players are like:
# ["Name":"Bob", "Points":5, "Answer":"Fart"}]

app = Flask(__name__)
app.secret_key = "Setec Astronomy"  # or set a static secret key

@app.route('/', methods=['GET','POST'])
def index():
    return redirect('setup', code=302)

@app.route('/setup', methods=['GET','POST'])
def setup():
    session.clear()
    return render_template('setup.html')

@app.route('/game', methods=['GET','POST'])
def game():
    # set up a game
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
    if not gameId in games: # create game if it doesn't exist
        games[gameId] = {"Players":[], "Prompt":""}
    # add player to game
    games[gameId]["Players"].append({"Name":name,"Points":0, "Answer":""})
    if debug: ic(games)
    session['Name'] = name
    # session['Points'] = 0
    session['GameId'] = gameId
    return render_template('game.html', name=session["Name"], gameId=session["GameId"])

@app.route('/poll', methods=['POST'])
def handle_request():
    # respond to regular poll requests from clients
    global games
    if verbose:
        try:
            ic(session)
        except:
            pass
    # Extract data sent by client
    data = request.json["payload"]
    if verbose: ic('Received data from client:', data)
    if data["Type"] == "Start": # new? get the setup info
        if games[session["GameId"]]["Prompt"] == "": # no prompt? gen one
            prompt = pickPrompt()
            games[session["GameId"]]["Prompt"] = prompt
        else: # otherwise send the one that's already been selected
            prompt = games[session["GameId"]]["Prompt"]
        if verbose: ic(f"Sending prompt {prompt}")
        return jsonify({"Type":"Prompt", "Prompt":prompt})
    elif data["Type"] == "Answer": # player is sending an answer? update the game
        games[session["GameId"]]["Player"]["Answer"] = data["Message"]
        return jsonify({"Received":{"Player":session["Name", "Answer":data["Message"]]}})
    else: # otherwise just send an update
        update = {"Type":"Update"}
        update["Update"] = genUpdate(session["GameId"], sanitized=True)
        if debug:
            ic(update)
        return update

if __name__ == '__main__':
    app.run(debug=True)
