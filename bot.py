"""
playing bot
"""

MIN_WAIT = 5
MAX_WAIT = 23

import computer_strategy

import sqlite3
import time
import random

def results_dict(s):
    if s == "":
        return {}
    else:
        return eval(s)

connection = sqlite3.connect("prisoner_dilemma.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

while True:

    cursor.execute("SELECT room, player1, player2, session_number, results FROM games ")

    rows = cursor.fetchall()
    for row in rows:
        print(row["room"], row["player1"], row["results"])
        print(row["results"])
        results = results_dict(row["results"])
        print(results)
        for session in results:
            if len(results[session]) == 1:
                print(computer_strategy.strategy[row["room"]])
                print(session, computer_strategy.strategy[row["room"]]["strategy"][int(session)])
                results[session][row["player2"]] = computer_strategy.strategy[row["room"]]["strategy"][int(session)]

                cursor.execute("UPDATE games SET results = ? WHERE room = ?", (str(results), row["room"]))
                connection.commit()

    time.sleep(random.randrange(MIN_WAIT, MAX_WAIT))