# -*- coding: utf-8 -*-


"""gitbatch.gitbatch: provides entry point main()."""

__version__ = '0.0.1'

import os
import click

from multiprocessing import cpu_count

from gitbatch.config import Config
from gitbatch.repos import GitRepos
from gitbatch.parallel import ConsumerManager
from gitbatch.tasks import RepositoryTask


# from pyfiglet import Figlet
# f = Figlet(font='slant')
# print(f.renderText('GitBatch'))


def repo_task(config):
    # TODO: DRY this code...
    repos = GitRepos().from_yaml(config.repos_file)
    worker = ConsumerManager(num_consumers=config.parallel).start()
    return repos, worker


@click.group()
@click.option('-r', '--repos-file', envvar='GITBATCH_REPOS_FILE',
              default=lambda: os.path.join(os.getcwd(), '_repos.yml'),
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help='Path to Repository definition file')
@click.option('-p', '--parallel', envvar='GITBATCH_PARALLEL',
              default=min(cpu_count() * 2, 10),
              type=click.IntRange(min=0, max=10),
              help='Level of Parallelism. 1 or 0 runs in series')
@click.option('-d', '--dry-run', envvar='GITBATCH_DRY_RUN', default=False,
              help='Print actions instead of performing them')
@click.option('-s', '--silent', envvar='GITBATCH_SILENT', default=False,
              help='Supress outputs')
@click.pass_context
def cli(ctx, repos_file, parallel, dry_run, silent):
    """Main execution wrapper. Parsers CLI arguments, loads data, calls the search method and displays the results"""

    ctx.obj = Config(repos_file=repos_file,
                     parallel=parallel,
                     dry_run=dry_run,
                     silent=silent,
                     )


@cli.command()
@click.pass_obj
def clone(config):
    """Git CLONE on all repositories defined in the Repos file"""

    repos, worker = repo_task(config)
    results = worker\
        .add([RepositoryTask(repo=r, action='clone', silent=config.silent) for r in repos.repos])\
        .done_adding()\
        .wait()

    # Create SymLinks after all Clone jobs have completed...
    results = results + [RepositoryTask(repo=r, action='link', silent=config.silent)() for r in repos.links]

    for r in results:
        click.echo(r)


@cli.command()
@click.pass_obj
def pull(config):
    """Run Git PULL on all repositories"""

    repos, worker = repo_task(config)
    results = worker\
        .add([RepositoryTask(repo=r, action='pull', silent=config.silent) for r in repos.repos])\
        .done_adding()\
        .wait()

    for r in results:
        click.echo(r)


@cli.command()
@click.pass_obj
def fetch(config):
    """Run Git FETCH on all repositories"""

    repos, worker = repo_task(config)
    results = worker\
        .add([RepositoryTask(repo=r, action='fetch', silent=config.silent) for r in repos.repos])\
        .done_adding()\
        .wait()

    for r in results:
        click.echo(r)


@cli.command()
@click.pass_obj
def doctor(_):
    """Check if repos defined exist locally"""

    click.echo('doctor: NOT IMPLEMENTED YET')
    click.echo('')
    exit(1)


@cli.command()
@click.argument('url')
@click.argument('path')
@click.pass_obj
def add(config, url, path):
    """Add Repository URL or SymLink to repos file"""

    path = path.replace('.', '/')
    click.echo('add: NOT IMPLEMENTED YET')
    click.echo('')
    click.echo('Adding URL            {}'.format(url))
    click.echo('       to path        {}'.format(path))
    click.echo('       on Repos file  {}'.format(config.repos_file))
    exit(1)


@cli.command()
@click.argument('path')
@click.pass_obj
def remove(config, path):
    """Remove repository from repos file. This won't touch the local files"""

    click.echo('check: NOT IMPLEMENTED YET')
    click.echo('')
    click.echo('Removing path             {}'.format(path))
    click.echo('         from Repos file  {}'.format(config.repos_file))
    exit(1)


@cli.command()
def version():
    """Display gitbatch version"""
    click.echo('v' + __version__)
    exit(0)
