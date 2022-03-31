"""
playing bot for the prisoner dilemma

Launching the bot:
screen python3 bot.py /home/ofriard/prisoner_dilemma/src/prisoner_dilemma.db


"""

__version__ = "2021-05-13"

import sys
DB_FILE_NAME =  sys.argv[1]  #"prisoner_dilemma.db"

MIN_WAIT = 1  # seconds
MAX_WAIT = 7 # seconds

import computer_strategy

import sqlite3
import time
import random

def results_dict(s):
    if s == "":
        return {}
    else:
        return eval(s)

connection = sqlite3.connect(DB_FILE_NAME)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

while True:

    cursor.execute("SELECT room, player1, player2, session_number, results FROM games ")

    rows = cursor.fetchall()
    for row in rows:
        results = results_dict(row["results"])
        for session in results:
            # check if player has played
            if len(results[session]) == 1:
                print(f' room: {row["room"]}  player1: {row["player1"]}  results: {row["results"]}')
                computer_choice = computer_strategy.strategy[str(row["room"])]["strategy"][int(session) - 1]
                print(f"session: {session}   computer strategy: {computer_choice}")
                results[session][row["player2"]] = computer_choice

                cursor.execute("UPDATE games SET results = ? WHERE room = ?", (str(results), row["room"]))
                connection.commit()

    waiting_time = random.randrange(MIN_WAIT, MAX_WAIT)
    print(f"waiting {waiting_time} seconds")
    time.sleep(waiting_time)

