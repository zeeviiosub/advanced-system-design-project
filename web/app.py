from flask import Flask
from flask import render_template
import utils

app = Flask(__name__)

@app.route('/')
def main_page():
    users = utils.users_list()
    return render_template(
        'main.html',
        users=users
        )

@app.route('/<user_id>')
def user_page(user_id):
    snaps = utils.snapshots_list(user_id)
    return render_template('snaps.html', title=f"{user_id}'s snapshots", \
        user_id=user_id, snapshots=snaps)

@app.route('/<user_id>/<snapshot_id>')
def snapshot_page(user_id, snapshot_id):
    pose = utils.pose(user_id, snapshot_id)
    feelings = utils.feelings(user_id, snapshot_id)
    color_image = utils.color_image(user_id, snapshot_id)
    depth_image = utils.depth_image(user_id, snapshot_id)
    return render_template(
        'snap.html',
        title=f"{user_id}'s snapshot {snapshot_id}",
        pose=pose,
        feelings=feelings,
        color_image=color_image,
        depth_image=depth_image
        )

app.run(host='127.0.0.1', port=7000)
