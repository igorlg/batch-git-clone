from common import *
from joblib import Parallel, delayed
import yaml, os

def success(path, out):
  out = [filter_output(l) for l in out]
  out.append("Done fetching {}".format(path))
  return '\n'.join(out)

def failure(path):
  print(colored("Failed to pull {}".format(path), 'red'))

def git_pull(path, index):
  remote = git_remotes(path)

  if remote is None:
    pprint(("Skipping {} for it has no remotes".format(path)), index)
    return

  pprint(("Pulling {} from {}".format(path, remote)), index)
  out, err, ret = git('pull', path)

  if ret == 0:
    pprint(success(path, out), index)
  else:
    failure(path)

def recursive_walk(d, depth=0, parent=[]):
  for k, v in sorted(d.items(), key=lambda x: x[0]):
    if isinstance(v, dict):
      recursive_walk(v, depth+1, parent + [k])
    else:
      path = "/".join(parent + [k])
      if os.path.exists(path):
        paths.append(path)

def main():
  with open('_repos.yml', 'r') as f:
    repos = yaml.load(f)

  recursive_walk(repos)
  Parallel(n_jobs=get_cpu_count())(delayed(git_pull)(p,i) for i, p in enumerate(paths))

paths = []
main()
