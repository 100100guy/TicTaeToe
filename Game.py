import tkinter as tk
from tkinter import *

# Create a tkinter window
home_screen = tk.Tk()
hasEnded = False

# Variable to keep track of the current player (X or O)
current_player = "X"
# 2D list to store buttons
labels = [[None for _ in range(3)] for _ in range(3)]


##################################################################### Human Players ###################################################################
# Function to open the Tic Tac Toe game page
def open_tic_tac_toe():
    global hasEnded
    global current_player

    home_screen.withdraw()  # Hide the homepage window
    game_screen = tk.Toplevel()  # Create a new window for the game
    game_screen.title("Tic Tac Toe")

    # Rest of your Tic Tac Toe game code goes here (from global current_player to game_screen.mainloop())
    def gameOverCheck():
        global hasEnded
        # row check
        for i in range(3):
            if labels[i][0]["text"] != "":
                if labels[i][0]["text"] == labels[i][1]["text"] == labels[i][2]["text"]:
                    hasEnded = True
                    header_label.config(text=f"Winner: {labels[i][0]['text']}")
                    return

        # column check
        for i in range(3):
            if labels[0][i]["text"] != "":
                if labels[0][i]["text"] == labels[1][i]["text"] == labels[2][i]["text"]:
                    hasEnded = True
                    header_label.config(text=f"Winner: {labels[0][i]['text']}")
                    return

        # diagonal check
        if labels[0][0]["text"] != "":
            if labels[0][0]["text"] == labels[1][1]["text"] == labels[2][2]["text"]:
                hasEnded = True
                header_label.config(text=f"Winner: {labels[0][0]['text']}")
                return

        if labels[0][2]["text"] != "":
            if labels[0][2]["text"] == labels[1][1]["text"] == labels[2][0]["text"]:
                hasEnded = True
                header_label.config(text=f"Winner: {labels[0][2]['text']}")
                return
        flag = 0
        for i in range(3):
            for j in range(3):
                if labels[i][j]["text"] == "":
                    flag = 1
        if flag == 0:
            header_label.config(text=f"Draw")
            return

    # Function to handle button clicks
    def buttonClick(row, col):
        global current_player
        global hasEnded
        if hasEnded == False:
            # Check if the button is empty (text is "")
            if labels[row][col]["text"] == "":
                # Set the text of the button to the current player
                labels[row][col]["text"] = current_player

                labels[row][col]["font"] = ("Helvetica", 24)  # Customize the font size
                if current_player == "X":
                    labels[row][col]["fg"] = "blue"  # Customize the color for 'X'
                else:
                    labels[row][col]["fg"] = "red"  # Customize the color for 'O'

                gameOverCheck()
                # Toggle the current player for the next turn
                current_player = "O" if current_player == "X" else "X"

    def resetAll():
        global current_player
        global hasEnded
        for i in range(3):
            for j in range(3):
                labels[i][j]["text"] = ""
        current_player = "X"
        hasEnded = False
        header_label.config(text="Tic Tac Toe")

    # Create a label at the top of the board
    header_label = tk.Label(game_screen, text="Tic Tac Toe", font=("Helvetica", 16))
    header_label.grid(row=0, column=0, columnspan=3)
    reset = tk.Button(game_screen, text="Reset", command=resetAll)
    reset.grid(row=0, column=0)
    # Create buttons and assign the buttonClick function to them
    for i in range(3):
        for j in range(3):
            labels[i][j] = tk.Button(
                game_screen,
                text="",
                width=12,
                height=6,
                font=("Helvetica", 24),
                bg="white",
                command=lambda row=i, col=j: buttonClick(row, col),
            )
            labels[i][j].grid(row=i + 1, column=j)

    game_screen.title("Tic Tac Toe")

    def on_closing_game_screen():
        exit(0)

    game_screen.protocol("WM_DELETE_WINDOW", on_closing_game_screen)

    game_screen.mainloop()
    # You can add a "Back" button in the Tic Tac Toe game page to return to the homepage if needed.


##################################################################### AI ###################################################################

# Variable to keep track of the current player (X or O)
current_player2 = "X"

hasEnded2 = False
labels2 = [[None for _ in range(3)] for _ in range(3)]


def open_tic_tac_toe_ai():
    global hasEnded2
    global current_player2
    global labels2

    home_screen.withdraw()  # Hide the homepage window
    game_screen_ai = tk.Toplevel()  # Create a new window for the game
    game_screen_ai.title("Tic Tac Toe")

    def is_winner(board, player):
        # Check rows, columns, and diagonals for a win
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] == player:
                return True

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] == player:
                return True

        if all(board[i][i] == player for i in range(3)) or all(
            board[i][2 - i] == player for i in range(3)
        ):
            return True

        return False

    def is_full(board):
        # Check if the board is full
        return all(board[row][col] != "" for row in range(3) for col in range(3))

    def evaluate(board):
        # Check for a win or a tie and return a score
        # Positive score for AI win, negative for human win, 0 for a tie
        if is_winner(board, "0"):
            return 1
        elif is_winner(board, "X"):
            return -1
        elif is_full(board):
            return 0
        else:
            return None

    def minimax(board, depth, alpha, beta, is_maximizer):
        # Base case: return the evaluation score if the game is over
        score = evaluate(board)
        if score is not None:
            return score

        if is_maximizer:
            best_score = -float("inf")
            for move in available_moves(board):
                board[move[0]][move[1]] = "0"
                score = minimax(board, depth + 1, alpha, beta, False)
                board[move[0]][move[1]] = ""  # Undo the move
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Prune the rest of the subtree
            return best_score
        else:
            best_score = float("inf")
            for move in available_moves(board):
                board[move[0]][move[1]] = "X"
                score = minimax(board, depth + 1, alpha, beta, True)
                board[move[0]][move[1]] = ""  # Undo the move
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Prune the rest of the subtree
            return best_score

    def find_best_move(board):
        best_move = None
        best_score = -float("inf")
        alpha = -float("inf")
        beta = float("inf")

        for move in available_moves(board):
            board[move[0]][move[1]] = "0"
            score = minimax(board, 0, alpha, beta, False)
            board[move[0]][move[1]] = ""  # Undo the move
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def available_moves(board):
        # Return a list of available moves (empty cells)
        moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    moves.append((i, j))

        return moves

    def gameOverCheck():
        global hasEnded2
        global labels2
        # row check
        for i in range(3):
            if labels2[i][0]["text"] != "":
                if (
                    labels2[i][0]["text"]
                    == labels2[i][1]["text"]
                    == labels2[i][2]["text"]
                ):
                    hasEnded2 = True
                    header_label.config(text=f"Winner: {labels2[i][0]['text']}")
                    return

        # column check
        for i in range(3):
            if labels2[0][i]["text"] != "":
                if (
                    labels2[0][i]["text"]
                    == labels2[1][i]["text"]
                    == labels2[2][i]["text"]
                ):
                    hasEnded2 = True
                    header_label.config(text=f"Winner: {labels2[0][i]['text']}")
                    return

        # diagonal check
        if labels2[0][0]["text"] != "":
            if labels2[0][0]["text"] == labels2[1][1]["text"] == labels2[2][2]["text"]:
                hasEnded2 = True
                header_label.config(text=f"Winner: {labels2[0][0]['text']}")
                return

        if labels2[0][2]["text"] != "":
            if labels2[0][2]["text"] == labels2[1][1]["text"] == labels2[2][0]["text"]:
                hasEnded2 = True
                header_label.config(text=f"Winner: {labels2[0][2]['text']}")
                return
        flag = 0
        for i in range(3):
            for j in range(3):
                if labels2[i][j]["text"] == "":
                    flag = 1
        if flag == 0:
            header_label.config(text=f"Draw")
            return

    # Function to handle button clicks
    def buttonClick(row, col):
        global current_player2
        global hasEnded2
        if hasEnded2 == False:
            # Check if the button is empty (text is "")
            if labels2[row][col]["text"] == "":
                # Set the text of the button to the current player
                labels2[row][col]["text"] = "X"

                board = [["" for _ in range(3)] for _ in range(3)]
                for i in range(3):
                    for j in range(3):
                        board[i][j] = labels2[i][j]["text"]

                move = find_best_move(board)
                if move is not None:  # Check if a valid move was found
                    labels2[move[0]][move[1]]["text"] = "0"

                gameOverCheck()

    def resetAll():
        global current_player2
        global hasEnded2
        global labels2
        for i in range(3):
            for j in range(3):
                labels2[i][j]["text"] = ""
        current_player2 = "X"
        hasEnded2 = False
        header_label.config(text="Tic Tac Toe")

    # Create a 2D list to store buttons
    labels2 = [[None for _ in range(3)] for _ in range(3)]

    # Create a label at the top of the board
    header_label = tk.Label(game_screen_ai, text="Tic Tac Toe", font=("Helvetica", 16))
    header_label.grid(row=0, column=0, columnspan=3)

    reset = tk.Button(game_screen_ai, text="Reset", command=resetAll)
    reset.grid(row=0, column=0)

    # Create buttons and assign the buttonClick function to them
    for i in range(3):
        for j in range(3):
            labels2[i][j] = tk.Button(
                game_screen_ai,
                text="",
                width=12,
                height=6,
                font=("Helvetica", 24),
                bg="white",
                command=lambda row=i, col=j: buttonClick(row, col),
            )
            labels2[i][j].grid(row=i + 1, column=j)

    def on_closing_game_screen():
        exit(0)

    game_screen_ai.protocol("WM_DELETE_WINDOW", on_closing_game_screen)

    game_screen_ai.title("Tic Tac Toe")
    game_screen_ai.mainloop()


# Create a label for the homepage
homepage_label = tk.Label(
    home_screen, text="Welcome to Tic Tac Toe", font=("Helvetica", 16)
)
homepage_label.pack(pady=20)

# Create a button to start the game
start_button = tk.Button(home_screen, text="Start Game", command=open_tic_tac_toe)
start_button.pack()

# Create a button to start the game
start_button_ai = tk.Button(
    home_screen, text="Start Game AI", command=open_tic_tac_toe_ai
)
start_button_ai.pack()

home_screen.title("Homepage")
home_screen.mainloop()
