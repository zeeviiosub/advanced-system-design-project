import click
@click.group()
def main():
    pass

@main.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
def copy(src, dst):
    for fn in src:
        click.echo(f'move {fn} to folder {dst}')


@main.command()
@click.option('--name', envvar='NAME', prompt=True)
def hello(name):
    click.echo(f'Hello, {name}!')
if __name__ == '__main__':
    main()
