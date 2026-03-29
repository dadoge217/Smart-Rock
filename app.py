from flask import Flask, render_template, request
import werkzeug
from commandCenter.brain import export

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    mood = export()
    status = "Not Connected"
    companionMode = "ON"
    if request.method == 'GET':
        return render_template('index.html', dstatus=status, dmood = mood, dcomp = companionMode)
    if request.method == 'POST':
        try:
            mood = export()
            mode = request.form['connection_mode']
            ip = request.form['ip']
            if mode == 'motor':
                ip="PM"+ip
            if mode == 'wifi':
                ip="PW"+ip
            print(ip)
            status = "Connected!"
        except werkzeug.exceptions.BadRequestKeyError:
            print("bad")
        return render_template('index.html', dstatus = status, dmood = mood, dcomp = companionMode)

@app.route("/menu")
def menu():
    return render_template('commands.html')