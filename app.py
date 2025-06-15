# 2048 Game - A Flask-based implementation
# Copyright (c) 2025 Rahul Raval
# Licensed under the MIT License. See LICENSE file in the project root for details.
from flask import Flask, render_template, request, jsonify
import random
import copy
import json
import os
from datetime import datetime

app = Flask(__name__)

# Add custom strftime filter to Jinja2 environment
@app.template_filter('strftime')
def strftime_filter(value, format_string):
    if value == 'now':
        dt = datetime.now()
        if format_string == '%s':
            return str(int(dt.timestamp()))  # Convert to Unix timestamp
        return dt.strftime(format_string)
    if format_string == '%s':
        return str(int(value.timestamp()))  # Convert to Unix timestamp
    return value.strftime(format_string)

class Game:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = random.choice([2, 4])

    def slide_and_merge(self, line):
        tiles = [x for x in line if x != 0]
        merged = []
        score_add = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged.append(tiles[i] * 2)
                score_add += tiles[i] * 2
                i += 2
            else:
                merged.append(tiles[i])
                i += 1
        return merged + [0] * (4 - len(merged)), score_add

    def move(self, direction):
        old_board = copy.deepcopy(self.board)
        score_add = 0
        if direction == "left":
            for i in range(4):
                self.board[i], add = self.slide_and_merge(self.board[i])
                score_add += add
        elif direction == "right":
            for i in range(4):
                self.board[i] = self.slide_and_merge(self.board[i][::-1])[0][::-1]
                score_add += self.slide_and_merge(self.board[i][::-1])[1]
        elif direction == "up":
            self.board = [list(row) for row in zip(*self.board)]
            for i in range(4):
                self.board[i], add = self.slide_and_merge(self.board[i])
                score_add += add
            self.board = [list(row) for row in zip(*self.board)]
        elif direction == "down":
            self.board = [list(row) for row in zip(*self.board)]
            for i in range(4):
                self.board[i] = self.slide_and_merge(self.board[i][::-1])[0][::-1]
                score_add += self.slide_and_merge(self.board[i][::-1])[1]
            self.board = [list(row) for row in zip(*self.board)]

        if self.board != old_board:
            self.score += score_add
            self.add_tile()
        return self.board, self.score

    def is_game_over(self):
        if any(2048 in row for row in self.board):
            return True, "You hit 2048! Victory!"
        if not any(0 in row for row in self.board):
            for i in range(4):
                for j in range(4):
                    if (i < 3 and self.board[i][j] == self.board[i+1][j]) or \
                       (j < 3 and self.board[i][j] == self.board[i][j+1]):
                        return False, ""
            return True, "No more moves! Game over."
        return False, ""

# Global game instance
game = Game()

# High score management
def load_high_scores():
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            return json.load(f)
    return []

def save_high_score(score):
    scores = load_high_scores()
    scores.append({"score": score, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]  # Keep top 5 scores
    with open("high_scores.json", "w") as f:
        json.dump(scores, f)
    return scores

@app.route("/")
def index():
    current_time = datetime.now().strftime("%I:%M %p IST on %A, %B %d, %Y")
    print("Initial board:", game.board)  # Debug log
    return render_template("index.html", board=game.board, score=game.score, current_time=current_time)

@app.route("/move/<direction>", methods=["POST"])
def move(direction):
    global game
    game.move(direction)
    over, message = game.is_game_over()
    if over:
        save_high_score(game.score)
        game = Game()  # Reset game on game over
    return jsonify({"board": game.board, "score": game.score, "status": message if over else f"Score: {game.score}"})

@app.route("/reset", methods=["POST"])
def reset():
    global game
    game = Game()
    return jsonify({"board": game.board, "score": game.score, "status": "Slide tiles to start!"})

@app.route("/high_scores", methods=["GET"])
def get_high_scores():
    return jsonify(load_high_scores())

if __name__ == "__main__":
    app.run(debug=True)