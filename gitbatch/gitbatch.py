# -*- coding: utf-8 -*-


"""distro.distro: provides entry point main()."""

__version__ = '0.0.1'

import argparse

import os

from multiprocessing import cpu_count
from joblib import Parallel, delayed
from subprocess import Popen, PIPE

from gitbatch.repos import GitRepos


def version():
    return 'v' + __version__


def main():
    """Main execution wrapper. Parsers CLI arguments, loads data, calls the search method and displays the results"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repos-file', type=str, default='./_repos.yaml', help='Path to Repositories File')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Display actions that would be performed')
    parser.add_argument('-v', '--version', action='store_true', help='Show version')
    parser.add_argument('action', nargs='?', help='Action {clone|pull|fetch|check}')
    args = parser.parse_args()

    if args.version:
        print(version())
        exit(0)

    assert args.action[0] in ['clone', 'pull', 'fetch', 'check'], 'Invalid action "{}"'.format(args.action[0])
    assert os.access(args.repos_file, os.R_OK), 'Unable to read repos file "{}"'.format(args.repos_file)

    repos = GitRepos().from_yaml(args.repos_file)

    if args.action[0] == 'clone':
        Parallel(n_jobs=cpu_count())(delayed(r.clone)(None) for r in repos.items() if not r.is_link)
        for r in repos.items():
            if r.is_link:
                r.link()
    elif args.action[0] == 'pull':
        Parallel(n_jobs=cpu_count())(delayed(r.pull)(None) for r in repos.items() if not r.is_link)
    elif args.action[0] == 'fetch':
        Parallel(n_jobs=cpu_count())(delayed(r.fetch)(None) for r in repos.items() if not r.is_link)
    elif args.action[0] == 'check':
        print('check: NOT IMPLEMENTED YET')


def git(commands, path=None):
    try:
        cmd = ['git'] + commands
    except:
        cmd = ['git'] + [commands]

    run = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=path)
    run.wait()

    err = [l.strip() for l in run.stderr]
    if run.returncode == 0:
        out = [l.strip() for l in run.stdout]
    else:
        out = []
    return out, err, run.returncode
