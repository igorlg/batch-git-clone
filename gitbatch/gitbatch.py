# -*- coding: utf-8 -*-


"""distro.distro: provides entry point main()."""

__version__ = '0.0.1'

import os
import argparse

from gitbatch.repos import GitRepos
from gitbatch.repos import RepositoryTask
from gitbatch.parallel import ConsumerManager


def version():
    return 'v' + __version__


def main():
    """Main execution wrapper. Parsers CLI arguments, loads data, calls the search method and displays the results"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repos-file', type=str, default='./_repos.yaml', help='Path to Repositories File')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Display actions that would be performed')
    parser.add_argument('-v', '--version', action='store_true', help='Show version')
    parser.add_argument('action', help='Action {clone|pull|fetch|check}')
    args = parser.parse_args()

    if args.version:
        print(version())
        exit(0)

    assert args.action in ['clone', 'pull', 'fetch', 'check'], 'Invalid action "{}"'.format(args.action[0])
    assert os.access(args.repos_file, os.R_OK), 'Unable to read repos file "{}"'.format(args.repos_file)

    repos = GitRepos().from_yaml(args.repos_file)

    if args.action in ['clone', 'pull', 'fetch']:
        parallel = ConsumerManager().start()

        if args.action == 'clone':
            parallel.add([RepositoryTask(r, 'clone') for r in repos.repos])
            parallel.add([RepositoryTask(r, 'link') for r in repos.links])
        elif args.action == 'pull':
            parallel.add([RepositoryTask(r, 'pull') for r in repos.repos])
        elif args.action == 'fetch':
            parallel.add([RepositoryTask(r, 'fetch') for r in repos.repos])

        results = parallel.done_adding().wait()
        for r in results:
            print(r.output)
    else:
        if args.action == 'check':
            print('check: NOT IMPLEMENTED YET')
