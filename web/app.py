from flask import Flask
from flask import render_template
import snaplist

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/<user_id>')
def user_page(user_id):
    snaps = snaplist.snapshots_list(user_id)
    return render_template('snaps.html', title=f"{user_id}'s snapshots", \
        user_id=user_id, snapshots=snaps)

@app.route('/<user_id>/<snapshot_id>')
def snapshot_page(user_id, snapshot_id):
    snap = snaplist.snapshot(user_id, snapshot_id)
    return render_template('snap.html', \
        title=f"{user_id}'s snapshot {snapshot_id}", user_id=user_id, \
        snapshot_id=snapshot_id)

app.run(host='127.0.0.1', port=8000)
