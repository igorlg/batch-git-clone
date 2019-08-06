import os
import yaml

from gitbatch.common import git


class GitRepos:
    def __init__(self):
        self._repos = list()
        self._dict = dict()

    def __str__(self):
        return '\n'.join([str(repo) for repo in self])

    def __iter__(self):
        for repo in self.repos:
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
                self._repos.append(Repository(path, remote=v))
            else:
                self._repos.append(Repository(path, link=v))

    @property
    def repos(self):
        return self._repos

    @property
    def dict(self):
        return self._dict

    def from_yaml(self, file):
        with open(file, 'r') as f:
            # TODO: Handle errors
            self._dict = yaml.load(f)
            self._walk(self._dict)
            return self


class Repository:
    def __init__(self, local, remote=None, link=None):
        self._local = local
        self._remote = remote
        self._symlink = link

    @property
    def local(self):
        return self._local

    @property
    def remote(self):
        return self._remote

    @property
    def symlink(self):
        return self._symlink

    @property
    def exists(self):
        return os.path.isdir(self._local)

    @property
    def link_exists(self):
        return os.path.isdir(self._symlink)

    @property
    def is_link(self):
        return self._symlink is not None

    def clone(self):
        if self.is_link:
            return False, 'Cannot clone {}. Is type Symlink'.format(self.local)
        if self.exists:
            return False, 'Skipping clone of {}. Path {} exists'.format(self.remote, self.local)

        out, err, ret = git(['clone', self.remote, self.local])
        if ret == 0:
            return True, 'Done cloning "{}" into "{}"'.format(self.remote, self.local)
        else:
            return False, 'ERROR: Unable to clone "{}"'.format(self.local)

    def pull(self):
        if self.is_link:
            return False, 'Cannot pull {}. Is type Symlink'.format(self.local)
        if not self.exists:
            return False, 'Cannot pull {}. Path doesnt exist'.format(self.local)

        out, err, ret = git(['pull', self.local])
        if ret == 0:
            return True, 'Done pulling "{}"'.format(self.local)
        else:
            return False, 'ERROR: Unable to pull "{}"'.format(self.local)

    def fetch(self):
        if self.is_link:
            return False, 'Cannot fetch {}. Is type Symlink'.format(self.local)
        if not self.exists:
            return False, 'Cannot fetch {}. Path doesnt exist'.format(self.local)

        out, err, ret = git(['fetch', self.local])
        if ret == 0:
            return True, 'Done fetch "{}"'.format(self.local)
        else:
            return False, 'ERROR: Unable to fetch "{}"'.format(self.local)

    def link(self):
        if not self.is_link:
            print('Cannot link {}. Is type Remote'.format(self.local))
        if self.exists:
            print('Skipping link of {} as destination path {} exists'.format(self.symlink, self.local))
            return False

        if not self.link_exists:
            print('Unable to link {} to {}. Source doesnt exist'.format(self.symlink, self.local))
            return False

        print("Creating symlink {} to {}".format(self.local, self.symlink))
        os.symlink(self.symlink, self.local)
