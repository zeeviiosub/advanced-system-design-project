import requests

host_ip = '127.0.0.1'
port = '9000'
URL = f'http://{host_ip}:{port}'

def snapshots_list(user_id):
    r = requests.get(f'{URL}/users/{user_id}/snapshots')
    return r.json()['snapshots']

def snapshot(user_id, snapshot_id):
    r = requests.get(f'{URL}/users/{user_id}/snapshots/{snapshot_id}')
    return r.json()['snapshot']

def pose(user_id, snapshot_id):
    r = requests.get(f'{URL}/users/{user_id}/snapshots/{snapshot_id}/pose')
    translation = r[0:3]
    rotation = r[3:7]
    return r.json()['result']

def depth_image(user_id, snapshot_id):
    r = requests.get(
        f'{URL}/users/{user_id}/snapshots/{snapshot_id}/depth_image')
    image = requests.get(r.json()['result'])
    return image.data
