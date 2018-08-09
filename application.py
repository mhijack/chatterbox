import gevent.monkey
gevent.monkey.patch_all()

import os

from flask import Flask, render_template, request, session, redirect, flash
from flask_socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# list of all channels
channel_list = ["general"]
channels = [{
    "name": "general",
    "users": []
}]
users_list = ["jack"]


@app.route("/")
def index():
    """If user visits for the first time, prompt to enter a username
       and save user's session, redirect to chat room.
       Otherwise redirect user to chat room."""
    try:
        if (session["username"]):
            return redirect("/chat")
    except:
        return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    if (username in users_list):
        flash("Username exists.")
        return redirect("/")
    else:
        session["username"] = username
        users_list.append(username)
        return redirect("/chat")


@app.route("/chat", methods=["GET"])
def chat():
    if (session["username"]):
        return render_template("chat.html", channel_list=channel_list, users_list=users_list)
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/channel/<channel>")
def channel(channel):
    for channel_obj in channels:
        if (channel_obj["name"] == channel):
            channel_info = channel_obj
    if (session["username"] not in channel_obj["users"]):
        channel_obj["users"].append(session["username"])
    return render_template("channel.html", channel_info=channel_info)


@socketio.on("create room")
def create_room(room):
    if (room["name"] not in channel_list):
        channel_list.append(room["name"])
        channels.append({
            "name": room["name"],
            "users": [session["username"]]
        })
        print(channels)
    emit("room created", {"name": room["name"]}, broadcast=True)
    return redirect("/channel/"+room["name"])


if (__name__ == '__main__'):
    socketio.run(app)
