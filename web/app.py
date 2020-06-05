from flask import Flask
from flask import render_template
import web.utils
import datetime

app = Flask(__name__)

@app.route('/')
def main_page():
    users = web.utils.users_list()
    return render_template(
        'main.html',
        users=users
        )

@app.route('/<user_id>')
def user_page(user_id):
    user = web.utils.user(user_id)
    username = user['username']
    birth_date = user['birth_date']
    gender = user['gender']
    snaps = web.utils.snapshots_list(user_id)
    return render_template(
        'snaps.html',
        title=f"{username}'s snapshots",
        user_id=user_id,
        snapshots=snaps,
        username=username,
        birth_date=str(datetime.datetime.fromtimestamp(birth_date)),
        gender=gender
        )

@app.route('/<user_id>/<snapshot_id>')
def snapshot_page(user_id, snapshot_id):
    username = web.utils.user(user_id)['username']
    pose = web.utils.pose(user_id, snapshot_id)
    feelings = web.utils.feelings(user_id, snapshot_id)
    color_image = web.utils.color_image(user_id, snapshot_id)
    depth_image = web.utils.depth_image(user_id, snapshot_id)
    return render_template(
        'snap.html',
        title=f"{username}'s snapshot {snapshot_id}",
        user_id=user_id,
        pose=pose,
        feelings=feelings,
        color_image=color_image,
        depth_image=depth_image
        )

app.run(host='127.0.0.1', port=8080)
