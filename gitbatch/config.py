import os


class Config:
    def __init__(self, **kwargs):
        if 'config' in kwargs.keys():
            print('Reading config from file {}'.format(kwargs['config']))

        self.__dict__.update(kwargs)

        self._check_repos_file()
        self._check_parallel()

    def __str__(self):
        return '\n'.join(['{}: {}'.format(k, v) for k, v in self.__dict__.items()])

    def _check_repos_file(self):
        """Check validity of the Repository File. Parameter: Config.repos_file """

        # Validate if Readable
        if not os.access(self.repos_file, os.R_OK):
            raise ValueError('repos_file "{}" not readable'.format(self.repos_file))

    def _check_parallel(self):
        """Check validity of the Paarallel. Parameter: Config.parallel"""
        # Disable Parallel (run in series)
        if self.parallel == 0:
            self.parallel = 1
        # Max of 10 workers
        self.parallel = min(self.parallel, 10)
