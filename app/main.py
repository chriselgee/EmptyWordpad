#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template, redirect, session
from icecream import ic
from random import choice, shuffle
from os import getenv

# Set output level
if getenv("VERBOSE") is not None: verbose = True
else: verbose = False
if getenv("DEBUG") is not None:
    debug = True
    verbose = True
else: debug = False

games = {}

def getPrompts():
    # Open the file and read each line into prompts
    file_path = 'data/prompts.txt'
    prompts = []
    with open(file_path, 'r') as file:
        for line in file:
            prompts.append(line.strip())
    shuffle(prompts) # randomize order
    if verbose: ic(f"Returning {len(prompts)} prompts")
    return prompts

def genUpdate(gameId, sanitized=True):
    # generate an update to push to players, w/o others' prompts if the round isn't over
    global games
    update = []
    # ic(games, gameId, sanitized)
    for i in range(len(games[gameId]["Players"])):
        ic(games[gameId]["Players"])
        player = games[gameId]["Players"][i]
        update.append(player)
        if sanitized: # blank out answers entered
            update[i]["Answer"] = "Entered"
        if player["Answer"] == "": # show Pending if there's no answer yet
            update[i]["Answer"] = "Pending"
    if verbose: ic(update)
    return update

def calcScore(gameId):
    # calculate scores for the end of a round
    global games
    if not games[gameId]["Scored"]:
        return None # don't add points if it's already been done
    else:
        games[gameId]["Scored"] = True
        matches = {} # count up matching answers
        pointIncreases = {} # track what matches
        for player in games[gameId]["Players"]: # cycle through players, checking answers
            if player["Answer"].lower().strip() in matches: # increment if answer's already been seen
                matches[player["Answer"].lower().strip()] += 1
            else: # otherwise add it to the collection
                matches[player["Answer"].lower().strip()] = 1
        for answer in matches:
            if matches[answer] == 2: # 3 points for single match
                for i in range(len(games[gameId]["Players"])):
                    if games[gameId]["Players"][i]["Answer"].lower() == answer:
                        games[gameId]["Players"][i]["Points"] += 3
                        pointIncreases[games[gameId]["Players"][i]["Name"]] = "+3"
            if matches[answer] > 2: # 1 point for multi match
                for i in range(len(games[gameId]["Players"])):
                    if games[gameId]["Players"][i]["Answer"].lower() == answer:
                        games[gameId]["Players"][i]["Points"] += 1
                        pointIncreases[games[gameId]["Players"][i]["Name"]] = "+1"
        if verbose: ic(pointIncreases)
        return pointIncreases # send back a dict of score increases

def checkIfRoundDone(gameId):
    # checks if everyone has an answer
    roundOver = True
    for i in range(len(games[gameId]["Players"])):
        if games[gameId]["Players"][i]["Answer"] == "":
            roundOver = False
    if verbose: ic(roundOver)
    return roundOver

def checkIfWinner(gameId):
    # check if someone has 25 points
    winners = []
    for i in range(len(games[gameId]["Players"])):
        if games[gameId]["Players"][i]["Points"] >= 25:
            winners.append(games[gameId]["Players"][i]["Name"])
    if verbose: ic(winners)
    return winners # returns empty list if no winners

# Each game is a dict entry like:
# {"Game12":{"Players":[], "Prompt":"Fire ____", "Locked":True, "Available":[], "Scored":False}}

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
        games[gameId] = {"Players":[], "Prompt":"", "Locked":False, "Available":getPrompts(), "Scored":False}
    # add player to game
    games[gameId]["Players"].append({"Name":name,"Points":0, "Answer":""})
    if debug: ic(games)
    session['Name'] = name
    # session['Points'] = 0
    session['GameId'] = gameId
    return render_template('game.html', name=session["Name"], gameId=session["GameId"])

@app.route('/fail', methods=['GET','POST'])
def fail():
    session.clear()
    return render_template('fail.html', message="Sadness")

@app.route('/poll', methods=['POST'])
def handle_request():
    # respond to regular poll requests from clients
    global games
    if debug:
        try:
            ic(session)
        except:
            ic("Couldn't ic(session)")
    # Extract data sent by client
    data = request.json["payload"]
    if debug: ic('Received data from client:', data)
    if data["Type"] == "Start": # new? get the setup info
        if games[session["GameId"]]["Prompt"] == "": # no prompt? gen one
            prompt = games[session["GameId"]]["Available"].pop()
            games[session["GameId"]]["Prompt"] = prompt
        else: # otherwise send the one that's already been selected
            prompt = games[session["GameId"]]["Prompt"]
        if verbose: ic(f"Sending prompt {prompt}")
        return jsonify({"Type":"Prompt", "Prompt":prompt})
    elif data["Type"] == "Answer": # player is sending an answer? update the game
        for i in range(len(games[session["GameId"]]["Players"])):
            if games[session["GameId"]]["Players"][i]["Name"] == session["Name"]: # find the right player to update
                games[session["GameId"]]["Players"][i]["Answer"] = data["Message"] # update
        games[session["GameId"]]["Locked"] = True # don't allow more players in
        if verbose: ic({"Received":{"Player":session["Name"], "Answer":data["Message"]}})
        return {"Received":{"Player":session["Name"], "Answer":data["Message"]}}
    else: # otherwise just send an update
        update = {"Type":"Update"}
        if checkIfRoundDone(session["GameId"]):
            update["Update"] = genUpdate(session["GameId"], sanitized=False)
            calcScore(session["GameId"])
        else:
            update["Update"] = genUpdate(session["GameId"], sanitized=True)
        if debug: ic(update)
        return update

if __name__ == '__main__':
    app.run(debug=True)
