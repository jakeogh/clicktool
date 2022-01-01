#!/usr/bin/env python3
# -*- coding: utf8 -*-

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  #      Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement
# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning
# pylint: disable=C0413  # TEMP isort issue [wrong-import-position] Import "from pathlib import Path" should be placed at the top of the module [C0413]

from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click

signal(SIGPIPE, SIG_DFL)

# https://stackoverflow.com/questions/40182157/python-click-shared-options-and-flags-between-commands
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


click_global_options = [
    click.option('-v', "--verbose", count=True),
    click.option('--verbose-inf', is_flag=True),      # replaces debug
]
