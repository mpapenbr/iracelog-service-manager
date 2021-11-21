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

import asyncio
import configparser
import os
import ssl
from logging import config

import autobahn
import certifi
import click
import txaio
from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.asyncio.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

from iracelog_service_manager import __version__
from iracelog_service_manager.manager.archive.archiver_main import ArchiverManager
from iracelog_service_manager.manager.overall import ProviderManager


@click.group()
@click.pass_context
@click.option('--url', help='url of the crossbar server', envvar="RACELOG_URL", show_default=True)
@click.option('--realm', help='crossbar realm for racelogger ', envvar="RACELOG_REALM", show_default=True)
@click.option('--user', help='user name to access crossbar realm', envvar="RACELOG_USER", required=True)
@click.option('--password', help='user password  to access crossbar realm', envvar="RACELOG_PASSWORD", required=True)
@click.version_option(__version__)
def main(ctx,url,realm,user,password):
    ctx.ensure_object(dict)
    ctx.obj['url'] = url
    ctx.obj['realm'] = realm
    ctx.obj['user'] = user
    ctx.obj['password'] = password
    pass
 
@main.command()
@click.pass_context
@click.option('--verbose', "-v", help='set verbosity level', count=True)
def manager(ctx, verbose):
    """init and start the crossbar clients manager"""
    click.echo(f"In manager url={ctx.obj['url']}")
    extra={'user':ctx.obj['user'], 'password': ctx.obj['password']}
    if ctx.obj['url'].startswith("wss://"):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
    else:
        ssl_context = None

    levels = ['info', 'debug', 'trace']
    ctx.obj['logLevel'] = levels[min(verbose,len(levels)-1)]
    txaio.start_logging(level=ctx.obj['logLevel'])
    config.fileConfig('logging.conf')
    runner = ApplicationRunner(url=ctx.obj['url'], realm=ctx.obj['realm'], extra=extra, ssl=ssl_context)
    # runner.run(ProviderManager, log_level=ctx.obj['logLevel'])
    runner.run(ProviderManager)

@main.command()
@click.pass_context
@click.option('--verbose', "-v", help='set verbosity level', count=True)
def archiver(ctx, verbose):
    """init and start the crossbar clients archiver and manager"""
    click.echo(f"In archiver url={ctx.obj['url']}")
    extra={'user':ctx.obj['user'], 'password': ctx.obj['password']}
    if ctx.obj['url'].startswith("wss://"):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
    else:
        ssl_context = None

    levels = ['info', 'debug', 'trace']
    ctx.obj['logLevel'] = levels[min(verbose,len(levels)-1)]
    txaio.start_logging(level=ctx.obj['logLevel'])
    config.fileConfig('logging.conf')
    runner = ApplicationRunner(url=ctx.obj['url'], realm=ctx.obj['realm'], extra=extra, ssl=ssl_context)
    # runner.run(ProviderManager, log_level=ctx.obj['logLevel'])
    runner.run(ArchiverManager)