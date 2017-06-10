from __future__ import absolute_import
from __future__ import print_function

from myserver.command import FlowerCommand
from myserver.utils import bugreport


def main():
    try:
        flower = FlowerCommand()
        flower.execute_from_commandline()
    except:
        import sys
        print(bugreport(app=flower.app), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
