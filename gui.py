import web.app
import click

def run_server(host, port, api_host, api_port):
    web.app.run_server(host, port, api_host, api_port)

@click.group()
def main():
    pass

@main.command()
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=8080)
@click.option('--api-host', '-H', default='127.0.0.1')
@click.option('--api-port', '-P', default=5000)
def run_server(host, port, api_host, api_port):
    web.app.run_server(host, port, api_host, api_port)

if __name__ == '__main__':
    main()
