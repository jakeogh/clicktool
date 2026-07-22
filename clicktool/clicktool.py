#!/usr/bin/env python3

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

_SLICE_CHARS = set("0123456789-:")


def validate_slice(slice_syntax: str) -> str:
    assert slice_syntax.startswith("[")
    assert slice_syntax.endswith("]")
    for c in slice_syntax[1:-1]:
        if c not in _SLICE_CHARS:
            raise ValueError(slice_syntax)
    return slice_syntax


def click_add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


click_global_options = [
    click.option("--verbose", is_flag=True),
    click.option("--dict", "dict_output", is_flag=True),
    click.option("--verbose-inf", is_flag=True),
]

ARCH_LIST = sorted(os.listdir("/var/db/repos/gentoo/profiles/arch"))

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
    ctx: click.Context,
    verbose_inf: bool,
    verbose: bool = False,
) -> bool:
    ctx.ensure_object(dict)
    if ctx.obj.get("verbose"):
        verbose = True
    if verbose_inf:
        verbose = True
    ctx.obj["verbose"] = verbose
    return verbose


def tv(
    *,
    ctx: click.Context,
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
    ctx: click.Context,
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
    if verbose:
        ic.enable()
    else:
        ic.disable()
    if verbose_inf:
        gvd.enable()
    return tty, verbose
