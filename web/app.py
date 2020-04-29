from flask import Flask
from flask import render_template
import snaplist

app = Flask(__name__)

@app.route('/')
def main_page():
    return app.send_static_file('main.html')

@app.route('/<user_id>')
def user_page(user_id):
    snaps = snaplist.snapshots_list(user_id)
    return render_template('snaps.html', title=f"{user_id}'s snapshots", \
        user_id=user_id, snapshots=snaps)

@app.route('/<user_id>/<snapshot_id>')
def snapshot_page(user_id, snapshot_id):
    t_x = snaplist.translation_x(user_id, snapshot_id)
    t_y = snaplist.translation_y(user_id, snapshot_id)
    t_z = snaplist.translation_z(user_id, snapshot_id)
    r_x = snaplist.rotation_x(user_id, snapshot_id)
    r_y = snaplist.rotation_y(user_id, snapshot_id)
    r_z = snaplist.rotation_z(user_id, snapshot_id)
    r_w = snaplist.rotation_w(user_id, snapshot_id)
    col = snaplist.color_image(user_id, snapshot_id)
    dep = snaplist.depth_image(user_id, snapshot_id)
    hunger, thirst, exhaustion, happiness = \
        snaplist.feelings(user_id, snapshot_id)
    return render_template('snap.html', \
        title=f"{user_id}'s snapshot {snapshot_id}", translation_x=t_x, \
        translation_y=t_y, translation_z=t_z, rotation_x=r_x, \
        rotation_y=r_y, rotation_z=r_z, rotation_w=r_w, hunger=hunger, \
        thirst=thirst, exhaustion=exhaustion, happiness=happiness)

app.run(host='127.0.0.1', port=8000)
