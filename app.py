from boggle import Boggle
from flask import Flask, redirect, render_template, request, flash, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"


@app.route("/")
def homepage():
    """Show board."""
    # create new board
    new_board = boggle_game.make_board()

    # add board to session
    session['board'] = new_board
    highscore = session.get("highscore", 0)
    totalPlays = session.get("totalPlays", 0)
    return render_template("index.html", board=new_board, highscore=highscore, totalPlays=totalPlays)


@app.route("/word-check")
def check_word():
    """Check if word is in dictionary."""
    input = request.args["input"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, input)
    return jsonify({'result': response})


@app.route("/end-game", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    totalPlays = session.get("totalPlays", 0)
    # increase the amount of plays by user by 1
    session['totalPlays'] = totalPlays + 1
    session['highscore'] = max(score, highscore)
    return jsonify(newRecord=score > highscore)


@app.route("/reset-game", methods=["POST"])
def reset_game():
    """Reset the Game, session"""
    session['totalPlays'] = 0
    session['highscore'] = 0
    return redirect("/")
