# Skeleton of a CLI

import click

import ovs


@click.command('ovs')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(ovs.has_legs)
