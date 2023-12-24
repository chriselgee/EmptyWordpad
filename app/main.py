#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template, redirect
from icecream import ic
from random import choice

file_path = 'data/prompts.txt'
prompts = []

# Open the file and read each line
with open(file_path, 'r') as file:
    for line in file:
        prompts.append(line.strip())

def pickPrompt():
    return choice(prompts)

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return redirect('setup', code=302)

@app.route('/setup', methods=['GET','POST'])
def setup():
    return render_template('setup.html')

@app.route('/game', methods=['GET','POST'])
def game():
    return render_template('game.html')

@app.route('/poll', methods=['POST'])
def handle_request():
    # Extract data sent by client
    data = request.json["payload"]
    if request.method == "POST":
        if "name" in request.form:
            name = request.form['name']
    ic('Received data from client:', data)

    if data["Type"] == "Start":
        prompt = pickPrompt()
        ic(f"Sending prompt {prompt}")
        return jsonify({"Type":"Prompt", "Prompt":prompt})
    elif data["Type"] == "Answer":
        return jsonify("Answer")
    else:
        return jsonify("Answer")

if __name__ == '__main__':
    app.run(debug=True)
