from flask import Flask, render_template, request, redirect, url_for, abort
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

frame_items: dict = {
    "frame-a": set(),
    "frame-b": set(),
}


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", frame_items=frame_items)


@app.route("/actions/append", methods=["POST"])
def action_append():
    element = request.form
    target = element["target-id"]
    item = element["item-id"]
    if target not in frame_items or item in frame_items[target]:
        abort(404)

    frame_items[target].add(item)

    if turbo.can_stream():
        return turbo.stream(
            turbo.append(render_template("_frame_item.html", item=item), target=target)
        )

    return redirect(url_for("index"))

@app.route("/actions/prepend", methods=["POST"])
def action_prepend():
    element = request.form
    target = element["target-id"]
    item = element["item-id"]
    if target not in frame_items or item in frame_items[target]:
        abort(404)

    frame_items[target].add(item)

    if turbo.can_stream():
        return turbo.stream(
            turbo.prepend(render_template("_frame_item.html", item=item), target=target)
        )

    return redirect(url_for("index"))

@app.route("/actions/replace", methods=["POST"])
def action_replace():
    element = request.form
    item = element["item-id"]
    new_item = element["new-item-id"]
    frame = None

    for target, items in frame_items.items():
        if item in items:
            frame_items[target].remove(item)
            frame = target

    if not frame:
        abort(404)

    frame_items[frame].add(new_item)

    if turbo.can_stream():
        return turbo.stream(
            turbo.replace(render_template("_frame_item.html", item=new_item), target=item)
        )

    return redirect(url_for("index"))

@app.route("/actions/update", methods=["POST"])
def action_update():
    element = request.form
    item = element["item-id"]
    new_item = element["new-item-id"]
    frame = None

    for target, items in frame_items.items():
        if item in items:
            frame_items[target].remove(item)
            frame = target

    if not frame:
        abort(404)

    frame_items[frame].add(new_item)

    if turbo.can_stream():
        return turbo.stream(
            turbo.update(render_template("_frame_item.html", item=new_item), target=item)
        )

    return redirect(url_for("index"))

@app.route("/actions/remove", methods=["POST"])
def action_remove():
    element = request.form
    item = element["item-id"]

    for target, items in frame_items.items():
        if item in items:
            frame_items[target].remove(item)

    if turbo.can_stream():
        return turbo.stream(turbo.remove(target=item))

    return redirect(url_for("index"))
