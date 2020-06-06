import requests
import click

default_host = '127.0.0.1'
default_port = '5000'

@click.group()
def main():
    pass

@main.command()
@click.option('--host', default=default_host)
@click.option('--port', default=default_port)
def get_users(host=default_host, port=default_port):
    r = requests.get(f'http://{host}:{port}/users')
    click.echo(r.text)

@main.command()
@click.argument('user_id')
@click.option('--host', default=default_host)
@click.option('--port', default=default_port)
def get_user(user_id, host=default_host, port=default_port):
    r = requests.get(f'http://{host}:{port}/users/{user_id}')
    click.echo(r.text)

@main.command()
@click.argument('user_id')
@click.option('--host', default=default_host)
@click.option('--port', default=default_port)
def get_snapshots(user_id, host=default_host, port=default_port):
    r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
    click.echo(r.text)

@main.command()
@click.argument('user_id')
@click.argument('snapshot_id')
@click.option('--host', default=default_host)
@click.option('--port', default=default_port)
def get_snapshot(user_id, snapshot_id, host=default_host, \
    port=default_port):
    r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots' + \
        f'/{snapshot_id}')
    click.echo(r.text)

@main.command()
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('result_name')
@click.option('--host', default=default_host)
@click.option('--port', default=default_port)
@click.option('--save', default=None)
def get_result(user_id, snapshot_id, result_name, host=default_host, \
    port=default_port, save=None):
    r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots' + \
        f'/{snapshot_id}/{result_name}')
    click.echo(r.text)
    if save:
        with open(save, 'w') as file:
            file.write(r.text)

if __name__ == '__main__':
    main()
