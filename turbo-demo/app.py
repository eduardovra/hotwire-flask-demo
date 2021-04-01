from flask import Flask, render_template, request, redirect, url_for, abort
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

frame_items = {
    'frame-a': set(),
    'frame-b': set(),
}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', frame_items=frame_items)

@app.route('/actions/append', methods=['POST'])
def action_append():
    element = request.form
    target = element['target-id']
    item = element['item-id']
    if target not in frame_items:
        abort(404)

    frame_items[target].add(item)

    if turbo.can_stream():
        return turbo.stream(
            turbo.append(
                render_template('_frame_item.html', item=item), target=target
            )
        )

    return redirect(url_for('index'))
