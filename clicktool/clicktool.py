#!/usr/bin/env python3
# -*- coding: utf8 -*-

# flake8: noqa           # flake8 has no per file settings :(
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

import os
import sys
import time
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
import sh

signal(SIGPIPE, SIG_DFL)
from pathlib import Path
from typing import ByteString
from typing import Generator
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from asserttool import eprint
from asserttool import ic
from asserttool import nevd
from asserttool import validate_slice
from asserttool import verify
from enumerate_input import enumerate_input
from portagetool import get_use_flags_for_package
from retry_on_exception import retry_on_exception

MESA_FLAGS = get_use_flags_for_package(package='media-libs/mesa',
                                       verbose=False,
                                       debug=False,)
MESA_FLAGS.append('video_cards_panfrost')  # https://github.com/Jannik2099/gentoo-pinebookpro/blob/master/mesa


# https://stackoverflow.com/questions/40182157/python-click-shared-options-and-flags-between-commands
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


click_mesa_options = [
    click.option('--mesa-use-enable', is_flag=False, required=False, type=click.Choice(MESA_FLAGS), default=["gallium"], multiple=True),
    click.option('--mesa-use-disable', is_flag=False, required=False, type=click.Choice(MESA_FLAGS), default=["osmesa", 'llvm'], multiple=True),
]


#@click.group()
#@click.option('--verbose', is_flag=True)
#@click.option('--debug', is_flag=True)
#@click.pass_context
#def cli(ctx,
#        verbose: bool,
#        debug: bool,
#        ):
#
#    null, end, verbose, debug = nevd(ctx=ctx,
#                                     printn=False,
#                                     ipython=False,
#                                     verbose=verbose,
#                                     debug=debug,)


@click.command()
@click.argument("paths", type=str, nargs=-1)
@click.argument("sysskel",
                type=click.Path(exists=False,
                                dir_okay=True,
                                file_okay=False,
                                allow_dash=False,
                                path_type=Path,),
                nargs=1,
                required=True,)
@click.argument("slice_syntax", type=validate_slice, nargs=1)
#@click.option('--add', is_flag=True)
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--simulate', is_flag=True)
@click.option('--ipython', is_flag=True)
#@click.option("--progress", is_flag=True)
@click.pass_context
def cli(ctx,
        paths: Optional[tuple[str]],
        sysskel: Path,
        slice_syntax: str,
        verbose: bool,
        debug: bool,
        simulate: bool,
        ipython: bool,
        ):

    null, end, verbose, debug = nevd(ctx=ctx,
                                     printn=False,
                                     ipython=False,
                                     verbose=verbose,
                                     debug=debug,)


