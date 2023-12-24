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
    return redirect('game', code=302)

@app.route('/game', methods=['GET','POST'])
def game():
    return render_template('game.html')

@app.route('/poll', methods=['POST'])
def handle_request():
    # Extract data sent by client
    data = request.json
    ic('Received data from client:', data)

    # Process the data (your game logic here)

    # Prepare your response data
    response_data = {
        'status': 'success',
        'message': 'Data processed',
        # Add other data you want to send back
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
