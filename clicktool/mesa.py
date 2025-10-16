#!/usr/bin/env python3
# -*- coding: utf8 -*-

# pylint: disable=C0413  # TEMP isort issue [wrong-import-position] Import "from pathlib import Path" should be placed at the top of the module [C0413]

from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click

signal(SIGPIPE, SIG_DFL)

# from asserttool import ic
from portagetool import get_use_flags_for_package

MESA_FLAGS = get_use_flags_for_package(
    package="media-libs/mesa",
)

MESA_FLAGS.append(
    "video_cards_panfrost"
)  # https://github.com/Jannik2099/gentoo-pinebookpro/blob/master/mesa

click_mesa_options = [
    click.option(
        "--mesa-use-enable",
        is_flag=False,
        required=False,
        type=click.Choice(MESA_FLAGS),
        default=["video_cards_intel"],
        multiple=True,
    ),
    click.option(
        "--mesa-use-disable",
        is_flag=False,
        required=False,
        type=click.Choice(MESA_FLAGS),
        default=["llvm"],
        multiple=True,
    ),
]
