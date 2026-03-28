from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    mood = "Happy"
    status = "Not Connected"
    companionMode = "ON"
    if request.method == 'GET':
        return render_template('index.html', dstatus=status, dmood = mood, dcomp = companionMode)
    if request.method == 'POST':
        mode = request.form['connection_mode']
        ip = request.form['ip']
        if mode == 'motor':
            ip="PM"+ip
        if mode == 'wifi':
            ip="PW"+ip
        print(ip)
        status = "Connected!"
        return render_template('index.html', dstatus = status, dmood = mood, dcomp = companionMode)

@app.route("/menu")
def menu():
    return render_template('commands.html')