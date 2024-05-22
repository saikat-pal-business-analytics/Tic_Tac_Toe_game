import random
import streamlit as st

# Initialize the game state
if "board" not in st.session_state:
    st.session_state.board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    st.session_state.currentPlayer = "X"
    st.session_state.winner = None
    st.session_state.gameRunning = True

board = st.session_state.board
currentPlayer = st.session_state.currentPlayer
winner = st.session_state.winner
gameRunning = st.session_state.gameRunning


# Game board
def printBoard(board):
    board_html = f"""
    <div style="display: grid; grid-template-columns: repeat(3, 100px); gap: 5px; justify-content: center;">
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[0]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[3]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[6]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[1]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[4]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[7]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[2]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[5]}</div>
        <div style="background: white; border: 2px solid black; text-align: center; line-height: 100px; font-size: 24px; color: black;">{board[8]}</div>
    </div>
    """
    st.markdown(board_html, unsafe_allow_html=True)


# Take player input
def playerInput(board, position):
    global currentPlayer
    if board[position] == "-":
        board[position] = currentPlayer
    else:
        st.warning("Oops! That spot is already taken.")


# Check for win or tie
def checkHorizontal(board):
    global winner
    if board[0] == board[1] == board[2] and board[0] != "-":
        winner = board[0]
        return True
    elif board[3] == board[4] == board[5] and board[3] != "-":
        winner = board[3]
        return True
    elif board[6] == board[7] == board[8] and board[6] != "-":
        winner = board[6]
        return True
    return False


def checkRow(board):
    global winner
    if board[0] == board[3] == board[6] and board[0] != "-":
        winner = board[0]
        return True
    elif board[1] == board[4] == board[7] and board[1] != "-":
        winner = board[1]
        return True
    elif board[2] == board[5] == board[8] and board[2] != "-":
        winner = board[2]
        return True
    return False


def checkDiag(board):
    global winner
    if board[0] == board[4] == board[8] and board[0] != "-":
        winner = board[0]
        return True
    elif board[2] == board[4] == board[6] and board[2] != "-":
        winner = board[2]
        return True
    return False


def checkIfWin(board):
    global gameRunning
    if checkHorizontal(board) or checkRow(board) or checkDiag(board):
        printBoard(board)
        st.success(f"The winner is {winner}!", icon="✅")
        gameRunning = False


def checkIfTie(board):
    global gameRunning
    if "-" not in board and winner is None:
        printBoard(board)
        st.info("It is a tie!", icon="ℹ️")
        gameRunning = False


def switchPlayer():
    global currentPlayer
    if currentPlayer == "X":
        currentPlayer = "O"
    else:
        currentPlayer = "X"


def computer(board):
    global currentPlayer
    while currentPlayer == "O" and gameRunning:
        position = random.randint(0, 8)
        if board[position] == "-":
            board[position] = "O"
            switchPlayer()
            break


# Streamlit UI
st.title("Tic-Tac-Toe")

# Apply background color to the app
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

printBoard(board)

if gameRunning:
    # Convert 1-9 horizontal to vertical-wise selection
    position_mapping = {
        1: 0, 2: 3, 3: 6,
        4: 1, 5: 4, 6: 7,
        7: 2, 8: 5, 9: 8
    }

    # Display selection options horizontally
    position = st.radio(
        "Select a spot:",
        options=list(range(1, 10)),
        format_func=lambda x: f"{x}",
        horizontal=True,
        key="position"
    )

    if st.button("Make Move"):
        mapped_position = position_mapping[position]
        playerInput(board, mapped_position)
        checkIfWin(board)
        checkIfTie(board)
        switchPlayer()
        computer(board)
        checkIfWin(board)
        checkIfTie(board)

    st.session_state.board = board
    st.session_state.currentPlayer = currentPlayer
    st.session_state.winner = winner
    st.session_state.gameRunning = gameRunning

# Add a button to refresh the game
if st.button("Restart Game", key="restart"):
    st.session_state.board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    st.session_state.currentPlayer = "X"
    st.session_state.winner = None
    st.session_state.gameRunning = True
    st.experimental_rerun()
