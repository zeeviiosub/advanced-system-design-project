import click
import flask
import redis
import json
from urllib.parse import urlparse

app = flask.Flask(__name__)

@click.group()
def main():
    pass

@app.route('/users')
def handle_users():
    try:
        request = flask.request.json
        r = redis.Redis(host=redis_host)
        users = r.hgetall('user')
        users_json = {}
        for key in users:
            users_json[key.decode('utf8')] = json.loads(users[key].decode('utf8'))['username']
        return flask.jsonify({'user': users_json, 'error': None})
    except Exception as error:
        return flask.jsonify({'user': None, 'error': str(error)})

@app.route('/users/<user_id>')
def handle_user_id(user_id):
    try:
        request = flask.request.json
        r = redis.Redis(host=redis_host)
        user = json.loads(r.hget('user', user_id).decode('utf8'))
        return flask.jsonify({'user': user, 'error': None})
    except Exception as error:
        return flask.jsonify({'user': None, 'error': error})

@app.route('/users/<user_id>/snapshots')
def handle_snapshots(user_id):
    try:
        request = flask.request.json
        r = redis.Redis(host=redis_host)
        snapshots = json.loads(r.hget('snapshots', user_id).decode('utf8'))
        snapshots_json = {}
        for key in snapshots:
            snapshots_json[key] = key
        return flask.jsonify({'snapshots': snapshots_json, 'error': None})
    except Exception as error:
        return flask.jsonify({'snapshots': None, 'error': error})

@app.route('/users/<user_id>/snapshots/<snapshot_id>')
def handle_snapshot_id(user_id, snapshot_id):
    try:
        request = flask.request.json
        r = redis.Redis(host=redis_host)
        fields = json.loads(r.hget(f'{user_id}.fields', snapshot_id).decode('utf8'))
        snapshot = {'id': snapshot_id,
                    'datetime': snapshot_id,
                    'fields': fields}
        return flask.jsonify({'snapshot': snapshot, 'error': None})
    except Exception as error:
        return flask.jsonify({'snapshot': None, 'error': error})

@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>')
def handle_result_name(user_id, snapshot_id, result_name):
    try:
        request = flask.request.json
        r = redis.Redis(host=redis_host)
        data = r.hget(f'{user_id}.{result_name}', snapshot_id)\
            .decode('utf8')
        result = json.loads(data)
        return flask.jsonify({'result': result, 'error': None})
    except Exception as error:
        return flask.jsonify({'result': None, 'error': error})

def run_api_server(host, port, database):
    global redis_host
    redis_host = database
    app.run(host=host, port=port)

@main.command()
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=5000)
@click.option('--database', '-d', default='127.0.0.1')
def run_server(host, port, database):
    run_api_server(host, port, database)

if __name__ == '__main__':
    main()
