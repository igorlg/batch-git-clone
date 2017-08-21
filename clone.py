from common import *
from joblib import Parallel, delayed
import yaml, os

def success(path, name, run):
  for l in run.stdout: filter_output(l)
  print "Done cloning repo %s into %s" % (name, path)

def failure(path, run):
  print colored("Failed to clone %s" % path, 'red')

def git_clone(name, path):
  print "Cloning %s into %s" % (name, path)
  cmd = git(['clone', name, path])

  if cmd.returncode == 0:
    success(path, name, cmd)
  else:
    failure(path, name, cmd)

def recursive_walk(d, depth=0, parent=[]):
  for k, v in sorted(d.items(), key=lambda x: x[0]):
    if isinstance(v, dict):
      recursive_walk(v, depth+1, parent + [k])
    else:
      path = "/".join(parent + [k])
      if not os.path.exists(path):
        git_repos[v] = path

def main():
  with open('_repos.yml', 'r') as f:
    repos = yaml.load(f)

  recursive_walk(repos)
  Parallel(n_jobs=get_cpu_count())(delayed(git_clone)(r,p) for r,p in git_repos.iteritems())

git_repos = {}
main()
