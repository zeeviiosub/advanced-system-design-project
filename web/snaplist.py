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
    return r.json()['result']

def translation_x(user_id, snapshot_id):
    return pose(user_id, snapshot_id)[0]

def translation_y(user_id, snapshot_id):
    return pose(user_id, snapshot_id)[1]

def translation_z(user_id, snapshot_id):
    return pose(user_id, snapshot_id)[2]

def rotation_x(user_id, snapshot_id):
    return pose(user_id, snapshot_id)[3]

def rotation_y(user_id, snapshot_id):
    return pose(user_id, snapshot_id)[4]

def rotation_z(user_id, snapshot_id):
    return pose(user_id, snapshot_id)[5]

def rotation_w(user_id, snapshot_id):
    return pose(user_id, snapshot_id)[6]

def depth_image(user_id, snapshot_id):
    r = requests.get(
        f'{URL}/users/{user_id}/snapshots/{snapshot_id}/depth-image')
    return r.json()['result']

def color_image(user_id, snapshot_id):
    r = requests.get(
        f'{URL}/users/{user_id}/snapshots/{snapshot_id}/color-image')
    return r.json()['result']

def feelings(user_id, snapshot_id):
    r = requests.get(
        f'{URL}/users/{user_id}/snapshots/{snapshot_id}/feelings')
    return r.json()['result']

def hunger(user_id, snapshot_id):
    return feelings(user_id, snapshot_id)[0]

def thirst(user_id, snapshot_id):
    return feelings(user_id, snapshot_id)[1]

def exhaustion(user_id, snapshot_id):
    return feelings(user_id, snapshot_id)[2]

def happiness(user_id, snapshot_id):
    return feelings(user_id, snapshot_id)[3]
