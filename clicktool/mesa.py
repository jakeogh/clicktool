#!/usr/bin/env python3
# -*- coding: utf8 -*-

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
