#!/usr/bin/env python

import argparse
from search import search, SearchError
from . import __version__
from . import __doc__


def search_action(args):
    try:
        result = search(**args.__dict__)
        if result.len == 0:
            print 'No records found, try new search criteria.'
            if (len(result.suggestions) > 0):
                print 'Did you mean: %s?'%', '.join(result.suggestions)
        else:
            print 'Displaying %d to %d of %d.' %(result.start, result.end, result.total)
            for line in result.lines:
                print line
    except SearchError as error:
        if args.verbose:
            print error.trace
        print error.error_message


def get_action(args):
    print 'Coming soon!'


class AdvancedAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if hasattr(namespace, 'advanced'):
            attrs = getattr(namespace, 'advanced')
        else:
            attrs = {}
        attrs[self.dest] = values
        setattr(namespace, 'advanced', attrs)


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def __init__(self, prog):
        super(HelpFormatter, self).__init__(prog, indent_increment=2, max_help_position=40, width=100)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=HelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s '+__version__)

    subparsers = parser.add_subparsers(title='Subcommands')

    search = subparsers.add_parser('search', formatter_class=HelpFormatter, description='Search the Maven Central Repository.')
    search.add_argument('query', nargs='?', default=None,
        help='query')
    search.add_argument('-v --verbose', action='store_true', dest='verbose',
        help='print extra details and errors')
    search.add_argument('-m --max', metavar='maximum', type=int, default=20, dest='maximum',
        help='limits the number of results returned by the server')
    search.add_argument('--core', metavar='core', dest='core',
        help='core')
    search.add_argument('-s --start', metavar='start', type=int, default=0, dest='start',
        help='search result index to start at')
    search.add_argument('-f --format', metavar='format', default='{i:>3}. {id} [{latestVersion}]', dest='format',
        help="result conversion format")

    advanced = search.add_argument_group('advanced', 'Advanced Search arguments')
    advanced.add_argument('-a --artifact', metavar='artifactId', dest='a', action=AdvancedAction,
        help='search by artifactId')
    advanced.add_argument('-g --group', metavar='groupId', dest='g', action=AdvancedAction,
        help='search by groupId')
    advanced.add_argument('-r --revision', metavar='version', dest='v', action=AdvancedAction,
        help='search by version')
    advanced.add_argument('-p --packaging', metavar='packaging', dest='p', action=AdvancedAction,
        help='search by packaging')
    advanced.add_argument('-l --classifier', metavar='classifier', dest='l', action=AdvancedAction,
        help='search by classifier')
    advanced.add_argument('-q --fqc', metavar='fqc', dest='fc', action=AdvancedAction,
        help='search by fully-qualified classname')
    advanced.add_argument('-c --cn', metavar='classname', dest='c', action=AdvancedAction,
        help='search by classname')
    advanced.add_argument('-1 --sha', metavar='SHA-1', dest='1', action=AdvancedAction,
        help='search by SHA-1 checksum')

    search.set_defaults(func=search_action)

    get = subparsers.add_parser('get')
    get.set_defaults(func=get_action)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
