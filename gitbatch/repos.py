import os
import yaml


class GitRepos:
    def __init__(self):
        self._dict = dict()
        self._all_repos = list()
        self._symlinks = list()

    def __str__(self):
        return '\n'.join([str(repo) for repo in self])

    def __iter__(self):
        for repo in self.all:
            yield repo

    def _walk(self, repos_dict, depth=0, parent=None):
        if parent is None:
            parent = list()
        for k, v in sorted(repos_dict.items(), key=lambda x: x[0]):
            if v is None:
                continue

            if isinstance(v, dict):
                self._walk(v, depth + 1, parent + [k])
                continue

            path = '/'.join(parent + [k])
            if v.startswith('git@') or v.startswith('https://'):
                self._all_repos.append(Repository(path, remote=v))
            else:
                self._all_repos.append(Repository(path, link=v))

    @property
    def dict(self):
        return self._dict

    @property
    def all(self):
        return self._all_repos

    @property
    def repos(self):
        return [r for r in self.all if r.is_repo]

    @property
    def links(self):
        return [r for r in self.all if r.is_link]

    def from_yaml(self, file):
        with open(file, 'r') as f:
            self._dict = yaml.load(f)
            self._walk(self._dict)
            return self


class Repository:
    def __init__(self, local, remote=None, link=None):
        self._local = local
        self._remote = remote
        self._link = link

        assert not (remote is None and link is None), 'Repo must either have Remote or be Link'

    def __str__(self):
        if self.is_link:
            target = 'SymLink: {}'.format(self.link)
        else:
            target = 'Remote: {}'.format(self.remote)
        return 'Local: {} - {}'.format(self.local, target)

    @property
    def local(self):
        return self._local

    @property
    def remote(self):
        return self._remote

    @property
    def link(self):
        return self._link

    @property
    def is_link(self):
        return self._link is not None

    @property
    def is_repo(self):
        return self._remote is not None

    @property
    def local_exists(self):
        return os.path.isdir(self._local)

    @property
    def link_exists(self):
        return os.path.isdir(self._link)


class RepositoryTask:
    def __init__(self, repo, action):
        self.repo = repo
        self.action = action
        self.output = ''
        self.executed = False

    def __call__(self, *args, **kwargs):
        if self.executed:
            self.output = 'Task already executed. Skipping'
        elif self.action == 'clone':
            self.output = 'Running CLONE on {}'.format(self.repo.local)
        elif self.action == 'pull':
            self.output = 'Running PULL on {}'.format(self.repo.local)
        elif self.action == 'fetch':
            self.output = 'Running FETCH on {}'.format(self.repo.local)
        elif self.action == 'link':
            self.output = 'Running LINK on {}'.format(self.repo.local)
        return self

    def __str__(self):
        return '{} on {}'.format(self.action, self.repo.local)
