from common import *
from joblib import Parallel, delayed
import yaml, os

def success(path, run):
  out = [filter_output(l) for l in run.stdout]
  out.append("Done pulling %s" % path)
  return out

def failure(path, run):
  print colored("Failed to pull %s" % path, 'red')

def git_pull(path, index):
  branch = git_branch_name(path)
  if not has_remote(branch, path):
    pprint(("Skipped path %s, branch %s for it doesn't have a remote" % (path, branch)), index)
    return None

  pprint(("Pulling %s on branch %s" % (path, branch)), index)
  cmd = git('pull', path)

  if cmd.returncode == 0:
    pprint('\n'.join(success(path, cmd)), index)
  else:
    failure(path, cmd)

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

  num_cores = get_cpu_count()
  # paths     = []

  recursive_walk(repos)
  Parallel(n_jobs=num_cores)(delayed(git_pull)(p,i) for i, p in enumerate(paths))

paths = []
main()
