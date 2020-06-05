import requests

host_ip = '127.0.0.1'
port = '5000'
URL = f'http://{host_ip}:{port}'

def users_list():
    r = requests.get(f'{URL}/users')
    return r.json()['user']

def user(user_id):
    r = requests.get(f'{URL}/users/{user_id}')
    return r.json()['user']

def snapshots_list(user_id):
    r = requests.get(f'{URL}/users/{user_id}/snapshots')
    return r.json()['snapshots']

def snapshot(user_id, snapshot_id):
    r = requests.get(f'{URL}/users/{user_id}/snapshots/{snapshot_id}')
    return r.json()['snapshot']

def result(user_id, snapshot_id, result):
    r = requests.get(f'{URL}/users/{user_id}/snapshots/{snapshot_id}/{result}')
    try:
        return r.json()['result']
    except Exception:
        return ''

def pose(user_id, snapshot_id):
    return result(user_id, snapshot_id, 'pose')


def depth_image(user_id, snapshot_id):
    return result(user_id, snapshot_id, 'depth_image')

def color_image(user_id, snapshot_id):
    return result(user_id, snapshot_id, 'color_image')

def feelings(user_id, snapshot_id):
    return result(user_id, snapshot_id, 'feelings')

