import uuid            # Library for SessionToken
import requests

from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User

app = Flask(__name__)

@app.route("/", methods=["GET"])    # Index-Controller with method GET for SessionToken
def index():                        # Index-Function
    session_token = request.cookies.get("session_token")


    if session_token:
        user = User.fetch_one(query=["session_token", "==", session_token])
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])  # Login-Controller with method POST to receive form-input
def login():
    mias_password = str("wundervoll")   # Define password

    password = request.form.get("password")     # Get pw from input

    name = request.form.get("user-name")        # Get name from input
    email = request.form.get("user-email")      # Get email from input

    # create a User object with Name and Email
    user = User(name=name, email=email)
    user.create()  # save the object into database

    # save user's session token into a cookie
    session_token = str(uuid.uuid4())
    response = make_response(redirect(url_for('index')))
    response.set_cookie("session_token", session_token)

    # Check if the pw input is correct
    if mias_password != password:
        return "Uuups...Das Passwort ist nicht korrekt."

    # If pw is correct, show Lebenslauf.html and fill Jinja-variable name
    elif mias_password == password:
        return render_template("Lebenslauf.html", name=name)

@app.route("/relax", methods=["GET"])  # Controller for relax
def relax():
    return render_template("Relax.html")

@app.route("/wetter", methods=["GET"])  # Controller for wetter
def wetter():
    query = "Cologne, GER"
    unit = "metric"
    api_key = "4441df35f38b74f5fba48f33d0efb41a"

    url = "https://api.openweathermap.org/data/2.5/weather?q={0}&units={1}&appid={2}".format(query, unit, api_key)
    data = requests.get(url=url)

    return render_template("wetter.html", data=data.json())


if __name__ == '__main__':
    app.run(debug=False)