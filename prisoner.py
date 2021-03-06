"""
Prisoner's dilemma web service

proof-of-concept for a Flask web service allowing playing to the prisoner's dilemma


Copyright 2021 Olivier Friard


  "Prisoner's dilemma web service" is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  any later version.

  "Prisoner's dilemma web service" is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not see <http://www.gnu.org/licenses/>.

"""

suffix="/prisoner"

from flask import Flask, render_template, Markup, redirect, request
app = Flask(__name__, static_folder='static', static_url_path=f'{suffix}/static')

app.debug = True

import sqlite3

actions_list = {"C": "cooperate", "D": "defect"}

def payoff(current_player, other_player):
    if current_player == "C" and other_player == "C":
        return 3
    if current_player == "C" and other_player == "D":
        return 1
    if current_player == "D" and other_player == "C":
        return 4
    if current_player == "D" and other_player == "D":
        return 2
    return 0


def results_dict(s):
    if s == "":
        return {}
    else:
        return eval(s)


@app.route(f'{suffix}/action/<player_action>/<player_id>/<room_id>/<session_idx>')
def action(player_action, player_id, room_id, session_idx):

    if player_action not in actions_list:
        return f"action {player_action} not found"

    connection = sqlite3.connect("prisoner_dilemma.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(("SELECT room, player1, player2, session_number, results "
                    "FROM games WHERE room = ?"),
                   (room_id, ))
    row = cursor.fetchone()

    results = results_dict(row["results"])

    if session_idx not in results:
        results[session_idx] = {}

    results[session_idx][player_id] = player_action
    cursor.execute("UPDATE games SET results = ? WHERE room = ?",
                   (str(results), room_id))
    connection.commit()

    if len(results[session_idx]) < 2:
        wait = True
        content = ""
    else:
        wait = False
        opponent = row["player1"] if row["player1"] != player_id else row["player2"]
        opponent_action = results[session_idx][opponent]
        gain = payoff(player_action, opponent_action)
        content = (f'You chose to {actions_list[player_action]} and the other partecipant chose to {actions_list[opponent_action]}.<br>'
                    f"As a result, you earned {gain} points. "
                    )
    return render_template("results.html",
                            wait=wait,
                            player_id=player_id,
                            room_id=room_id,
                            content=Markup(content),
                            suffix=suffix
                            )


@app.route(f'{suffix}/room/<player_id>/<room_id>')
def room(player_id, room_id):
    """
    let play a session of room room_id
    """

    connection = sqlite3.connect("prisoner_dilemma.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(("SELECT room, player1, player2, session_number, show_picture, results "
                    "FROM games WHERE room = ?"),
                   (room_id, ))
    row = cursor.fetchone()

    results = results_dict(row["results"])

    # find 1st playable session
    for session_idx in [str(x) for x in range(1, row["session_number"] + 1)]:
        if (session_idx not in results) or (len(results.get(session_idx, {})) < 2):
            break
    else:
        return f'all {row["session_number"]} played'

    if session_idx not in results:
        results[session_idx] = {}

    if player_id in results[session_idx]:
        return redirect(f"{suffix}/action/{results[session_idx][player_id]}/{player_id}/{room_id}/{session_idx}")
    else:
        opponent = row["player1"] if row["player1"] != player_id else row["player2"]
        if row["show_picture"]:


            picture = (f'<img id="imageID" src="{app.static_url_path}/pictures/{opponent}.jpg">\n'
                       f'<script src="{app.static_url_path}/hide_image.js"></script>')

            # picture = f'<img id="imageID" src="{app.static_url_path}/pictures/{opponent}.jpg">\n'


            hide_image = f'<script>window.onload = function() {{ hide_image("imageID", {row["show_picture"] * 1000}); }}</script>'

            # hide_image = ""

        else:
            picture = ""
            hide_image = ""

        return render_template("room.html",
                           room_id=room_id,
                           session_idx=session_idx,
                           player_id=player_id,
                           opponent=opponent,
                           hide_image=Markup(hide_image),
                           picture=Markup(picture),
                           suffix=suffix
                           )


@app.route(f'{suffix}/rooms/<player_id>')
def rooms(player_id):
    """
    list all the rooms for the player player_id
    """
    connection = sqlite3.connect("prisoner_dilemma.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(("SELECT room, player1, player2, session_number, results "
                    "FROM games WHERE player1 = ? OR player2 = ?"),
                   (player_id, player_id,))
    rows = cursor.fetchall()

    content = ""
    for row in rows:
        results = results_dict(row["results"])
        # check number of played sessions
        played = len([x for x in results if len(results[x]) == 2])
        # check if opponent is waiting
        opponent_is_waiting = "Yes" if len([x for x in results if len(results[x]) == 1 and player_id not in results[x]]) else "No"


        to_be_played = row["session_number"] - played
        content += (f'<tr><td><a href="{suffix}/room/{player_id}/{row["room"]}">room #{row["room"]}</a></td>'
                    f'<td>{row["session_number"]}</td><td>{played}</td><td>{to_be_played}</td>'
                    f'<td>{opponent_is_waiting}</td>'
                    '</tr>'
                    )

    if rows:
        return render_template("rooms.html",
                               player_id=player_id,
                               content=Markup(content),
                               suffix=suffix)
    else:
        content += "No more games to play"
        return render_template("rooms.html",
                               player_id=player_id,
                               content=Markup(content),
                               suffix=suffix)


@app.route(f'{suffix}/player_id', methods=("POST", "GET"))
def func_player_id():
    if request.method == "POST":
        player_id = request.form["player_id"]

        connection = sqlite3.connect("prisoner_dilemma.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM players WHERE id = ?",
                       (player_id, ))
        row = cursor.fetchone()
        if not row:
            return f"Player {player_id} not found"

    return redirect(f"{suffix}/rooms/{player_id}")

    '''
    return render_template("player.html",
                           player_id=player_id
                         )
    '''


@app.route(f'{suffix}/admin')
def admin():
    """
    administration page
    """

    connection = sqlite3.connect("prisoner_dilemma.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    rows = cursor.execute("SELECT id, name FROM players").fetchall()

    content = '<table class="table"><thead><tr><th>Players</th><th>Pictures</th><th>URL FOR rooms list</th></tr><thead>'
    for row in rows:
        content += f'<tr><td>{row["name"]}</td><td><img width="120px" src="{app.static_url_path}/pictures/{row["id"]}.jpg"></td><td>{row["id"]}</td></tr>'

    return render_template("admin.html",
                           content = Markup(content),
                           suffix=suffix)


@app.route(f'{suffix}/monitor')
def monitor():
    """
    monitor all games/sessions
    """

    connection = sqlite3.connect("prisoner_dilemma.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    rows = cursor.execute("SELECT room, player1, player2, session_number, show_picture, results FROM games").fetchall()

    content = f""
    for row in rows:

        results = results_dict(row['results'])
        n_played = sum([1 for x in results if len(results[x]) == 2])
        # pay off
        payoff_p1 = 0
        payoff_p2 = 0
        for x in results:
            if len(results[x]) == 2:
                payoff_p1 += payoff(results[x][row["player1"]], results[x][row["player2"]])
                payoff_p2 += payoff(results[x][row["player2"]], results[x][row["player1"]])

        content += (f"Room #{row['room']} "
                    f"Number of sessions: {row['session_number']}  (played: {n_played}) "
                    f"Show picture of player: {row['show_picture']} s"
                   )

        content += '<table class="table">'
        content += '<thead><tr><th>Players</th><th>Points</th><th colspan="25">Sessions</th></tr></thead>'


        content += f'<tr><td>{row["player1"]}</td><td>{payoff_p1}</td><td>' + ("</td><td>".join([results[x][row['player1']] for x in results if row['player1'] in results[x]])) + "</td></tr>"
        content += f'<tr><td>{row["player2"]}</td><td>{payoff_p2}</td><td>' + ("</td><td>".join([results[x][row['player2']] for x in results if row['player2'] in results[x]])) + "</td></tr>"

        content += '</table>'

    return render_template("monitor.html",
                           content = Markup(content),
                           suffix=suffix)

@app.route(suffix + '/')
@app.route(suffix)
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)