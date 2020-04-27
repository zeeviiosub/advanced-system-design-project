import requests
def snapshots_list(user_id):
    r = requests.get(f'http://127.0.0.1:9000/users/{user_id}/snapshots')
    return r.json()['snapshots']
