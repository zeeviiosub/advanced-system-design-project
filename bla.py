import click

@click.group()
def main():
    pass

@main.command()
@click.argument('x', type=int, nargs=1)
@click.argument('ys', type=int, nargs=-1)
@click.option('-m', '--multiply', is_flag=True)
def add(x, ys, multiply):
    result = x
    if multiply:
        for y in ys:
            result = result * y
    else:
        for y in ys:
            result = result + y
    click.echo(result)

@main.command()
@click.option('--name', envvar='NAME', prompt=True)
def hello(name):
    click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    main()
