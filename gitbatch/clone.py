from common import *
from joblib import Parallel, delayed
import yaml, os

def success(path, name, out):
  for l in out: filter_output(l)
  print("Done cloning repo {} into {}".format(name, path))

def failure(path):
  print(colored("Failed to clone {}".format(path), 'red'))

def git_clone(name, path):
  print("Cloning {} into {}".format(name, path))
  out, err, ret = git(['clone', name, path])

  if ret == 0:
    success(path, name, out)
  else:
    failure(path)

def create_symlinks(links):
  for t,l in links.items():
    if os.path.exists(l): # Link already exists
      continue
    elif not os.path.exists(t): # Targer doesn't exist
      print("Skipping link {} to {} as {} doesn't exists".format(l, t, t))
      continue

    print("Creating symlink {} to {}".format(l, t))
    os.symlink(t, l)

def recursive_walk(d, depth=0, parent=[]):
  for k, v in sorted(d.items(), key=lambda x: x[0]):
    if isinstance(v, dict):
      recursive_walk(v, depth+1, parent + [k])
    else:
      path = "/".join(parent + [k])
      try:
        if v.startswith('symlink:'):
          link = v.split(':')[1]
          sym_links[link] = path
        elif not os.path.exists(path):
          git_repos[v] = path
      except:
        continue

def main():
  with open('_repos.yml', 'r') as f:
    repos = yaml.load(f)

  recursive_walk(repos)
  Parallel(n_jobs=get_cpu_count())(delayed(git_clone)(r,p) for r,p in git_repos.items())
  create_symlinks(sym_links)

git_repos = {}
sym_links = {}
main()