import redis
import subprocess
import json

def test_cli_get_users():
    r = redis.Redis()
    r.hset('user', 200639318, json.dumps({'user_id': 200639318,
                                          'username': 'Zeevi Iosub',
                                          'birth_date': 578091600,
                                          'gender': 'm'}))
    subprocess.run('python api.py &', shell=True)
    completed_process = subprocess.run('python -m apicli get-users', shell=True, capture_output=True)
    print(completed_process.stdout)
    data = json.loads(completed_process.stdout)
    assert data['user']['200639318'] == 'Zeevi Iosub'
    assert data['error'] == None
    r.hdel('user', 200639318)

def test_cli_get_user():
    r = redis.Redis()
    r.hset('user', 200639318, json.dumps({'user_id': 200639318,
                                          'username': 'Zeevi Iosub',
                                          'birth_date': 578091600,
                                          'gender': 'm'}))
    subprocess.run('python api.py &', shell=True)
    completed_process = subprocess.run('python -m apicli get-user 200639318', shell=True, capture_output=True)
    data = json.loads(completed_process.stdout)
    assert data['user']['user_id'] == 200639318
    assert data['user']['username'] == 'Zeevi Iosub'
    assert data['user']['birth_date'] == 578091600
    assert data['user']['gender'] == 'm'
    assert data['error'] == None
    r.hdel('user', 200639318)

def test_cli_get_snapshots():
    r = redis.Redis()
    r.hset('snapshots', 200639318, json.dumps({'1': 1, '2': 2}))
    process = subprocess.run('python api.py &', shell=True)
    completed_process = subprocess.run('python -m apicli get-snapshots 200639318', shell=True, capture_output=True)
    data = json.loads(completed_process.stdout)
    assert data['snapshots']['1'] == 1
    assert data['snapshots']['2'] == 2
    assert data['error'] == None
    r.hdel('snapshots', 2000639318)

def test_cli_get_snapshot():
    r = redis.Redis()
    r.hset('200639318.fields', 1, json.dumps(['field1', 'field2']))
    process = subprocess.run('python api.py &', shell=True)
    completed_process = subprocess.run('python -m apicli get-snapshot 200639318 1', shell=True, capture_output=True)
    data = json.loads(completed_process.stdout)
    assert data['snapshot']['id'] == '1'
    assert data['snapshot']['datetime'] == 1
    assert 'field1' in data['snapshot']['fields']
    assert 'field2' in data['snapshot']['fields']
    assert len(data['snapshot']['fields']) == 2
    assert data['error'] == None
    r.hdel('200639318.fields', 1)

def test_cli_get_result():
    r = redis.Redis()
    r.hset('200639318.pose', 1, json.dumps({'translation': (1,2,3), 'rotation': (5,6,7,8)}))
    process = subprocess.run('python api.py &', shell=True)
    completed_process = subprocess.run('python -m apicli get-result 200639318 1 pose', shell=True, capture_output=True)
    data = json.loads(completed_process.stdout)
    assert data['result']['translation'] == [1,2,3]
    assert data['result']['rotation'] == [5,6,7,8]
    assert data['error'] == None
    r.hdel('200639318.pose', 1)
