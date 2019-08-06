import os
import yaml


class GitRepos:
    def __init__(self):
        self._repos = dict()
        self._symlinks = dict()
        self._dict = dict()

    def __iter__(self):
        for repo, path in self.repos.items():
            yield repo, path
        for link, path in self.symlinks.items():
            yield link, path

    def __str__(self):
        out = ['Repos:']
        for repo, path in self.repos.items():
            out.append('{}: {}'.format(repo, path))
        out.append('SymLinks:')
        for link, path in self.symlinks.items():
            out.append('{}: {}'.format(link, path))
        return '\n'.join(out)

    def _walk(self, repos_dict, depth=0, parent=None):
        if parent is None:
            parent = list()
        for k, v in sorted(repos_dict.items(), key=lambda x: x[0]):
            if isinstance(v, dict):
                self._walk(v, depth + 1, parent + [k])
                continue

            if v is None:
                continue

            path = '/'.join(parent + [k])
            if os.path.exists(path):
                continue

            if v.startswith('git@') or v.startswith('https://'):
                self._repos[v] = path
            else:
                self._symlinks[v] = path

    @property
    def repos(self):
        return self._repos

    @property
    def symlinks(self):
        return self._symlinks

    @property
    def dict(self):
        return self._dict

    def from_yaml(self, file):
        with open(file, 'r') as f:
            # TODO: Handle errors
            self._dict = yaml.load(f)
            self._walk(self._dict)
            return self
