#!/usr/bin/env python3
# -*- coding: utf8 -*-
# disable: byte-vector-replacer

# pylint: disable=useless-suppression             # [I0021]
# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement

from __future__ import annotations

import os
import sys
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
from globalverbose.globalverbose import GlobalVerbose
from icecream import IceCreamDebugger

signal(SIGPIPE, SIG_DFL)

# https://github.com/pallets/click/issues/2313
CONTEXT_SETTINGS = dict(
    show_default=True,
    max_content_width=272,
)


# https://stackoverflow.com/questions/40182157/python-click-shared-options-and-flags-between-commands
def click_add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


click_global_options = [
    click.option("--verbose", is_flag=True),
    click.option("--dict", "dict_output", is_flag=True),
    click.option("--verbose-inf", is_flag=True),  # replaces debug
]

try:
    ARCH_LIST = [
        d
        for d in os.listdir("/var/db/repos/gentoo/profiles/arch")
        # os.fsdecode(dent.name)
        # for dent in dirs(
        #    "/var/db/repos/gentoo/profiles/arch",
        #    max_depth=0,
        #    verbose=False,
        # )
    ]
except FileNotFoundError:  # not gentoo
    ARCH_LIST = []


click_arch_select = [
    click.option(
        "--arch",
        is_flag=False,
        required=True,
        type=click.Choice(ARCH_LIST),
        multiple=False,
    ),
]


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36"

click_user_agent = [
    click.option(
        "--user-agent",
        type=str,
        default=USER_AGENT,
    )
]


click_cookies = [
    click.option(
        "--cookies",
        type=click.Choice(["chrome", "firefox", "opera", "edge", "chromium", "brave"]),
    )
]


def _v(
    *,
    ctx,
    verbose_inf: bool,
    verbose: bool = False,
) -> bool:
    ctx.ensure_object(dict)
    try:
        if ctx.obj["verbose"]:
            verbose = True
    except KeyError:
        pass
    if verbose_inf:
        verbose = True
    ctx.obj["verbose"] = verbose  # make sure ctx has the 'verbose' key set correctly
    return verbose


def tv(
    *,
    ctx,
    verbose_inf: bool,
    verbose: bool = False,
) -> tuple[bool, bool]:
    # if sys.stdout.isatty():
    #    assert not ipython
    verbose = _v(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )
    tty = sys.stdout.isatty()

    return tty, verbose


def tvicgvd(
    *,
    ctx,
    ic: IceCreamDebugger,
    gvd: GlobalVerbose,
    verbose_inf: bool,
    verbose: bool = False,
) -> tuple[bool, bool]:
    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    if not verbose:
        ic.disable()
    else:
        ic.enable()

    if verbose_inf:
        gvd.enable()

    return tty, verbose
