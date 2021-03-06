from flask import Flask, render_template
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)
sequence = 0

@app.route("/", methods=["GET",])
def index():
    global sequence
    return render_template("index.html", counter=sequence)

@app.route("/add-image", methods=["POST",])
def add_image():
    global sequence
    sequence += 1
    html = render_template("_image.html", seq=sequence)

    if turbo.can_stream():
        return turbo.stream([
            turbo.append(html, target="images"),
            turbo.update(sequence, target="counter"),
        ])

    return html
