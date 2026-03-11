from flask import Flask, render_template, request, redirect, jsonify
import json
import random
import threading
import time
import os

app = Flask(__name__)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ---------- JSON Helpers ----------
def load_json(file):
    path = os.path.join(DATA_DIR, file)
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    path = os.path.join(DATA_DIR, file)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ---------- Simulation Thread ----------
def simulate():
    while True:
        time.sleep(5)
        buses = load_json("buses.json")
        for b in buses:
            if random.random() > 0.7:
                delays = [0, 5, 10, 15]
                b["delay"] = random.choice(delays)
        save_json("buses.json", buses)
        
        temples = load_json("temples.json")
        crowds = ["Low", "Medium", "High"]
        for t in temples:
            if random.random() > 0.6:
                t["crowd"] = random.choice(crowds)
        save_json("temples.json", temples)

threading.Thread(target=simulate, daemon=True).start()

# ---------- Routes ----------
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_user():
    mobile = request.form["mobile"]
    password = request.form["password"]
    users = load_json("users.json")
    for u in users:
        if u["mobile"] == mobile and u["password"] == password:
            return redirect("/dashboard")
    return "<h3>Login Failed</h3><a href='/'>Try Again</a>"

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    users = load_json("users.json")
    users.append({
        "mobile": request.form["mobile"],
        "password": request.form["password"]
    })
    save_json("users.json", users)
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/buses")
def buses():
    return render_template("buses.html", buses=load_json("buses.json"))

@app.route("/temples")
def temples():
    return render_template("temples.html", temples=load_json("temples.json"))

@app.route("/hotels", methods=["GET", "POST"])
def hotels():
    hotels = load_json("hotels.json")
    if request.method == "POST":
        budget = int(request.form["budget"])
        hotels = [h for h in hotels if int(h["price"]) <= budget]
    return render_template("hotels.html", hotels=hotels)

@app.route("/hotel_booking", methods=["GET", "POST"])
def hotel_booking():
    hotels = load_json("hotels.json")
    if request.method == "POST" and "budget" in request.form:
        budget = int(request.form["budget"])
        hotels = [h for h in hotels if int(h["price"]) <= budget]
    return render_template("hotel_booking.html", hotels=hotels)

@app.route("/book_hotel", methods=["POST"])
def book_hotel():
    name = request.form["name"]
    return f"<h3>Hotel {name} booked!</h3><a href='/dashboard'>Back</a>"

@app.route("/commuters")
def commuters():
    return render_template("commuters.html", commuters=load_json("commuters.json"))

@app.route("/alerts")
def alerts():
    return render_template("alerts.html", alerts=load_json("alerts.json"))

@app.route("/route", methods=["GET", "POST"])
def route():
    result = None
    if request.method == "POST":
        start, end = request.form["start"], request.form["end"]
        result = f"Take Bus 101 from {start} to {end} (45 mins)"
    return render_template("route.html", route=result)

@app.route("/darshan", methods=["GET", "POST"])
def darshan():
    if request.method == "POST":
        return f"<h3>Pass booked for {request.form['temple']} on {request.form['date']}</h3><a href='/dashboard'>Back</a>"
    return render_template("darshan.html")

@app.route("/bus_pass", methods=["GET", "POST"])
def bus_pass():
    if request.method == "POST":
        return f"<h3>Bus pass issued for {request.form['name']} ({request.form['duration']})</h3><a href='/dashboard'>Back</a>"
    return render_template("bus_pass.html")

@app.route("/api/buses")
def api_buses():
    return jsonify(load_json("buses.json"))

@app.route("/api/temples")
def api_temples():
    return jsonify(load_json("temples.json"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
