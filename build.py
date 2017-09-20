#!/usr/bin/env python3
import sys

try:
    from clinner.run import Main
except ImportError:
    import importlib
    import pip
    import site

    print('Installing Clinner')
    pip.main(['install', '-qq', '--user', 'clinner'])

    importlib.reload(site)
    from clinner.run import Main


class Build(Main):
    commands = (
        'clinner.run.commands.pytest.pytest',
        'clinner.run.commands.prospector.prospector',
        'clinner.run.commands.sphinx.sphinx',
        'clinner.run.commands.tox.tox',
        'clinner.run.commands.dist.dist',
    )


def main():
    return Build().run()


if __name__ == '__main__':
    sys.exit(main())
