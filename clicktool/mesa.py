#!/usr/bin/env python3

import sys

import click
from portagetool import get_use_flags_for_package

try:
    MESA_FLAGS = get_use_flags_for_package(package="media-libs/mesa")
except click.ClickException as e:
    # sanctioned handler: hit in practice on hosts without mesa installed
    # (the netboot image builds with USE=-X). The choices degrade to exactly
    # the option defaults below, which must stay expressible or click rejects
    # them at invocation.
    print(
        f"clicktool.mesa: media-libs/mesa unavailable ({e.message}); "
        "mesa USE choices restricted to defaults",
        file=sys.stderr,
    )
    MESA_FLAGS = ["video_cards_intel", "llvm"]
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
