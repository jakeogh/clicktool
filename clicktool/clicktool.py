#!/usr/bin/env python3
# -*- coding: utf8 -*-
# disable: byte-vector-replacer


from __future__ import annotations

import os
import sys
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from globalverbose.globalverbose import GlobalVerbose
    from icecream import IceCreamDebugger

signal(SIGPIPE, SIG_DFL)

# https://github.com/pallets/click/issues/2313
CONTEXT_SETTINGS = dict(
    show_default=True,
    max_content_width=272,
)


def validate_slice(slice_syntax: str):
    assert isinstance(slice_syntax, str)
    assert slice_syntax.startswith("[")
    assert slice_syntax.endswith("]")
    for c in slice_syntax[1:-1]:
        if c not in [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "-",
            ":",
        ]:
            raise ValueError(slice_syntax)
    return slice_syntax


def click_validate_slice(
    ctx,
    param,
    value,
):
    # ic(param, value)
    if value is not None:
        validate_slice(value)
        return value


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
