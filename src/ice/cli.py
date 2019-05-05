"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mice` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``ice.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``ice.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import datetime

import luigi
from luigi import build

from ice.tasks.dashboard import ExecuteDashboard

config = luigi.configuration.get_config()
parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
                    help="A name of something.")


def main(args=None):
    args = parser.parse_args(args=args)
    print(args.names)
    date = datetime.date.today()
    print(date)
    build([

        ExecuteDashboard(run_date=date)

    ], local_scheduler=False)

