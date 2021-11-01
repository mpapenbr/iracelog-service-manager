"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -miracelog_service_manager` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``iracelog_service_manager.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``iracelog_service_manager.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import click
import configparser
import os
import autobahn
import urllib3

from iracelog_service_manager import __version__

@click.group()
@click.option('--url', help='url of the crossbar server', envvar="RACELOG_URL", show_default=True)
@click.option('--realm', help='crossbar realm for racelogger ', envvar="RACELOG_REALM", show_default=True)
@click.option('--user', help='user name to access crossbar realm', envvar="RACELOG_USER", required=True)
@click.option('--password', help='user password  to access crossbar realm', envvar="RACELOG_PASSWORD", required=True)
@click.version_option(__version__)
def main(names):
    pass
 
@main.command()
def manager():
  pass   