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

import inspect
import os
import sys
import time
from math import inf
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import ByteString
from typing import Generator
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import click
import sh
from getdents import dirs

signal(SIGPIPE, SIG_DFL)

# https://stackoverflow.com/questions/40182157/python-click-shared-options-and-flags-between-commands
def click_add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


click_global_options = [
    click.option("-v", "--verbose", count=True),
    click.option("--dict", "dict_input", is_flag=True),
    click.option("--verbose-inf", is_flag=True),  # replaces debug
]


ARCH_LIST = [
    os.fsdecode(dent.name)
    for dent in dirs(
        "/var/db/repos/gentoo/profiles/arch",
        max_depth=0,
        verbose=False,
    )
]


click_arch_select = [
    click.option(
        "--arch",
        is_flag=False,
        required=True,
        type=click.Choice(ARCH_LIST),
        multiple=False,
    ),
]


def _v(
    *,
    ctx,
    verbose: Union[bool, float, int],
    verbose_inf: bool,
):

    ctx.ensure_object(dict)
    if verbose_inf:
        verbose = inf
        return verbose

    if verbose:
        stack_depth = len(inspect.stack()) - 1
        verbose += stack_depth

    if verbose:
        ctx.obj[
            "verbose"
        ] = verbose  # make sure ctx has the 'verbose' key set correctly
    try:
        verbose = ctx.obj[
            "verbose"
        ]  # KeyError if verbose is False, otherwise obtain current verbose level in the ctx
    except KeyError:
        ctx.obj["verbose"] = verbose  # disable verbose

    return verbose


def tv(
    *,
    ctx,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
) -> tuple[bool, int]:

    # if sys.stdout.isatty():
    #    assert not ipython
    ctx.ensure_object(dict)
    verbose = _v(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )
    tty = sys.stdout.isatty()

    return tty, verbose
