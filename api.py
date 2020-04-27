import click
import flask
import redis
import protocol

app = flask.Flask(__name__)

@click.group()
def main():
    pass

@main.command()
def get_users():
    handle_users()

@app.route('/users')
def handle_users():
    try:
        request = flask.request.json
        r = redis.Redis()
        users = r.hgetall('username')
        users_json = []
        for key in users:
            users_json.append(int(key.decode('utf8')))
        return flask.jsonify({'user': users_json, 'error': None})
    except Exception as error:
        return flask.jsonify({'user': None, 'error': str(error)})

@app.route('/users/<user_id>')
def handle_user_id(user_id):
    try:
        request = flask.request.json
        r = redis.Redis()
        username = r.hget('username', user_id).decode('utf8')
        birthday = float(r.hget('birthday', user_id).decode('utf8'))
        gender = r.hget('gender', user_id).decode('utf8')
        user = { 'user_id': user_id,
                 'username': username,
                 'birthday': birthday,
                 'gender': gender }
        return flask.jsonify({'user': user, 'error': None})
    except Exception as error:
        return flask.jsonify({'user': None, 'error': error})

@app.route('/users/<user_id>/snapshots')
def handle_snapshots(user_id):
    try:
        request = flask.request.json
        r = redis.Redis()
        snapshots = r.hgetall(f'{user_id}.snapshot')
        snapshots_json = {}
        for key in snapshots:
            snapshots_json[int(key.decode('utf8'))] = \
                float(snapshots[key].decode('utf8'))
        return flask.jsonify({'snapshots': snapshots_json, 'error': None})
    except Exception as error:
        return flask.jsonify({'snapshots': None, 'error': error})

@app.route('/users/<user_id>/snapshots/<snapshot_id>')
def handle_snapshot_id(user_id, snapshot_id):
    try:
        request = flask.request.json
        r = redis.Redis()
        snapshot = r.hget(f'{user_id}.snapshot', snapshot_id)\
            .decode('utf8').split(' ')
        return flask.jsonify({'snapshot': snapshot, 'error': None})
    except Exception as error:
        return flask.jsonify({'snapshot': None, 'error': error})

@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>')
def handle_result_name(user_id, snapshot_id, result_name):
    try:
        request = flask.request.json
        r = redis.Redis()
        data = r.hget(f'{user_id}.{result_name}', snapshot_id)\
            .decode('utf8')
        if result_name == 'pose':
            trans_x, trans_y, trans_z, rot_x, rot_y, rot_z, rot_w = \
                data.split(' ')
            trans_x = float(trans_x)
            trans_y = float(trans_y)
            trans_z = float(trans_z)
            rot_x = float(rot_x)
            rot_y = float(rot_y)
            rot_z = float(rot_z)
            rot_w = float(rot_w)
            result = (trans_x, trans_y, trans_z, rot_x, rot_y, rot_z, \
                rot_w)
        elif result_name == 'color-image':
            result = data
        elif result_name == 'depth-image':
            result = data
        elif result_name == 'feelings':
            hunger, thirst, exhaustion, happiness = data.split(' ')
            hunger = float(hunger)
            thirst = float(thirst)
            exhaustion = float(exhaustion)
            happiness = float(happiness)
            result = (hunger, thirst, exhaustion, happiness)
        return flask.jsonify({'result': result, 'error': None})
    except Exception as error:
        return flask.jsonify({'result': None, 'error': error})
            
app.run(host='127.0.0.1', port=9000)
