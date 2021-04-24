from flask import Flask, render_template, redirect, url_for, request
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)
users = []

@app.route("/", methods=["GET",])
def index():
    global users

    context = {'username': {}, 'password': {}}
    return render_template("index.html", users=users, **context)

@app.route("/signup", methods=["POST",])
def signup():
    global users

    # Validade form
    data = {field: {'value': value}
            for field, value in request.form.items()}

    if turbo.can_stream():
        stream = []

        if data['username'] in users:
            stream.append(
                turbo.replace(
                    
                )
            )

    users.insert(0, data)

    # hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

    #return render_template("index.html", users=users, **data)

    # Everything is fine
    return redirect(url_for("index"))
