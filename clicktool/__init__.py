from .clicktool import click_arch_select
from .clicktool import click_add_options


#
## https://stackoverflow.com/questions/40182157/python-click-shared-options-and-flags-between-commands
#def add_options(options):
#    def _add_options(func):
#        for option in reversed(options):
#            func = option(func)
#        return func
#    return _add_options
#
#
#click_global_options = [
#    click.option('-v', "--verbose", count=True),
#    click.option('--verbose-inf', is_flag=True),      # replaces debug
#]
