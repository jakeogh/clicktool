#!/usr/bin/env python3

import click
from portagetool import get_use_flags_for_package

MESA_FLAGS = get_use_flags_for_package(package="media-libs/mesa")
# https://github.com/Jannik2099/gentoo-pinebookpro/blob/master/mesa
MESA_FLAGS.append("video_cards_panfrost")

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
