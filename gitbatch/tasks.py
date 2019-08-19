import os
import subprocess


class RepositoryTask:
    def __init__(self, repo, action, dry_run=False, silent=False):
        self.repo = repo
        self.action = action
        self.dry_run = dry_run
        self.silent = silent
        self.output = None
        self.executed = False

    def __str__(self):
        out = ''
        if self.dry_run:
            out = '[DRY RUN] '
        if self.silent:
            out = '{}[SILENT] '.format(out)
        out = '{}{} of {}'.format(out, self.action.capitalize(), self.repo)
        return out

    def __call__(self, *args, **kwargs):
        if self.executed:
            self.output = 'Task already executed. Skipping'
            return self

        self.executed = True

        if self.action == 'clone':
            self._task_clone()
        elif self.action == 'pull':
            self._task_pull()
        elif self.action == 'fetch':
            self._task_fetch()
        elif self.action == 'link':
            self._task_link()
        else:
            raise Exception('RepositoryTask: action {} not supported'.format(self.action))
        return self

    @property
    def details(self):
        leftlen = max([len(k)+2 for k in self.__dict__.keys()])

        def line(k, v):
            return '{}:'.format(k).ljust(leftlen) + str(v)
        return '\n'.join([line(k, v) for k, v in self.__dict__.items()])

    def _out(self, msg):
        if not self.silent:
            print(str(msg))
        self.output = '{}\n{}'.format(self.output, str(msg))
        return self

    @staticmethod
    def _git_cmd(cmd, args=None, cwd=None):
        if not isinstance(args, list):
            args = [args]

        gitcmd = ['git', cmd] + args
        out = list()
        try:
            result = subprocess.run(gitcmd, capture_output=True, check=True, cwd=cwd)
            out.append(result.stdout.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            out.append(e.stdout.decode('utf-8'))
            out.append(e.stderr.decode('utf-8'))
        return '\n'.join(out)

    def _task_clone(self):
        r = self.repo
        if r.local_exists:
            self._out('Skipping clone of {} to {}. Path already exists'.format(r.remote, r.local))
            return None

        # self._out('Running CLONE of {} to {}'.format(r.remote, r.local))
        cmd = ['git', 'clone', r.remote, r.local]
        self._out('Running "{}"'.format(' '.join(cmd)))
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            self._out(result.stdout.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            self._out(e.stdout.decode('utf-8'))
            self._out(e.stderr.decode('utf-8'))

    def _task_link(self):
        r = self.repo
        if r.local_exists:
            self._out('Skipping linking {} to {}. Link already exists'.format(r.local, r.link))
            return None

        self._out('Running LINK of {} to {}'.format(r.local, r.link))
        try:
            os.symlink(r.link, r.local, target_is_directory=True)
            self._out('Created link {} to {}'.format(r.local, r.link))
        except FileNotFoundError:
            self._out('Symlink not created. Target {} does not exist'.format(r.link))

    def _task_pull(self):
        r = self.repo
        if not r.local_exists:
            self._out('Skipping pull of {}. Repository does not exist'.format(r.local))
            return None

        cmd = ['git', 'pull']
        self._out('Running "{}" from Dir {}'.format(' '.join(cmd), r.local))
        try:
            result = subprocess.run(cmd, capture_output=True, check=True, cwd=r.local)
            self._out(result.stdout.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            self._out(e.stdout.decode('utf-8'))
            self._out(e.stderr.decode('utf-8'))

    def _task_fetch(self):
        r = self.repo
        if not r.local_exists:
            self._out('Skipping fetch of {}. Repository does not exist'.format(r.local))
            return None

        self._out('Running FETCH on {}'.format(r.local))
        self._out(' '.join(self._git_cmd(cmd='fetch', args='--all', cwd=r.local)))
