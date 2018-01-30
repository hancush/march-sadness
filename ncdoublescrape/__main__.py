import argparse
import importlib
import logging
import sys


logger = logging.getLogger()

COMMAND_MODULES = (
    'ncdoublescrape.scrape',
)

def main():
    parser = argparse.ArgumentParser('ncds', description='A janky NCAA scraper')
    subparsers = parser.add_subparsers(dest='subcommand')

    subcommands = {}

    for module in COMMAND_MODULES:
        try:
            command = importlib.import_module(module).Command(subparsers)
        except ImportError as e:
            logger.error('exception "%s" prevented loading of %s module', e, module)
        else:
            subcommands[command.name] = command

    args, other = parser.parse_known_args()

    if not args.subcommand:
        parser.print_help()
    else:
        try:
            subcommands[args.subcommand].handle(args, other)
        except Exception as e:
            logger.critical(str(e))
            sys.exit(1)


if __name__ == '__main__':
    main()