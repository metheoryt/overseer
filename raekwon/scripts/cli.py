# Skeleton of a CLI

import click

import raekwon


@click.command('raekwon')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(raekwon.has_legs)
