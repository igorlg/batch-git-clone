import os
import yaml


class GitRepos:
    def __init__(self):
        self._dict = dict()
        self._all_repos = list()
        self._symlinks = list()

    # def __str__(self):
    #     return str([str(repo) for repo in self])

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
                print('Creating Repo - Path: {} - Remote: {}'.format(path, v))
            else:
                self._all_repos.append(Repository(path, link=v))
                print('Creating Repo - Path: {} - Link: {}'.format(path, v))

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
            self._dict = yaml.load(f, Loader=yaml.FullLoader)
            self._walk(self._dict)

        return self


class Repository:
    def __init__(self, local, remote=None, link=None):
        self._local = os.path.realpath(local)
        self._remote = remote
        self._link = link

        assert not (remote is None and link is None), 'Repo must either have Remote or be Link'

    def __str__(self):
        if self.is_link:
            target = 'SymLink:{}'.format(self.link)
        else:
            target = 'Remote:{}'.format(self.remote)
        return 'Local:{},{}'.format(self.local, target)

    @property
    def local(self):
        return self._local

    @property
    def remote(self):
        return self._remote

    @property
    def link(self):
        return self._link

    # @property
    # def parent(self):
    #     return os.path.realpath(os.path.join(self.local, os.pardir))

    @property
    def is_link(self):
        return self.link is not None

    @property
    def is_repo(self):
        return self.remote is not None

    @property
    def local_exists(self):
        return os.path.exists(self.local)

    @property
    def link_exists(self):
        return os.path.isdir(self.link)
