import gradio as gr
import random
import copy

# Game state
class Game:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.status = "Slide tiles to start!"
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
            self.update_status()

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

    def update_status(self):
        over, message = self.is_game_over()
        self.status = message if over else f"Score: {self.score} - Keep playing!"

# Display as HTML with numbers
def board_to_html(board):
    html = "<table style='font-size: 24px; text-align: center; border-collapse: collapse;'>"
    tile_styles = {
        0: "#cdc1b4", 2: "#d4c2a8", 4: "#c9b38a", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
        256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
    }
    for row in board:
        html += "<tr>"
        for cell in row:
            bg = tile_styles.get(cell, "#cdc1b4")
            text = str(cell) if cell != 0 else ""
            html += f"<td style='width: 80px; height: 80px; background-color: {bg}; border: 2px solid #bbb;'>{text}</td>"
        html += "</tr>"
    html += "</table>"
    return html

# Game instance
game = Game()

# Gradio interface
def update_game(direction=None):
    if direction:
        game.move(direction)
    return board_to_html(game.board), game.status

def reset_game():
    global game
    game = Game()
    return board_to_html(game.board), game.status

with gr.Blocks(title="2048") as demo:
    gr.Markdown("# 2048")
    gr.Markdown("Slide tiles to merge numbers and reach 2048!")
    board_output = gr.HTML(value=board_to_html(game.board))
    status_output = gr.Textbox(value=game.status, label="Status")
    with gr.Row():
        gr.Button("⬆️ Up").click(fn=lambda: update_game("up"), outputs=[board_output, status_output])
        gr.Button("⬇️ Down").click(fn=lambda: update_game("down"), outputs=[board_output, status_output])
        gr.Button("⬅️ Left").click(fn=lambda: update_game("left"), outputs=[board_output, status_output])
        gr.Button("➡️ Right").click(fn=lambda: update_game("right"), outputs=[board_output, status_output])
    gr.Button("Reset Game").click(fn=reset_game, outputs=[board_output, status_output])

demo.launch()