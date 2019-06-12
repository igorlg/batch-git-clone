from common import *
from joblib import Parallel, delayed
import yaml, os, pathlib

def success(path, name, out):
  for l in out: filter_output(l)
  print("Done cloning repo {} into {}".format(name, path))

def failure(path):
  print(colored("Failed to clone {}".format(path), 'red'))

def git_clone(name, path):
  print("Cloning {} into {}".format(name, path))
  out, err, ret = git(['clone', name, path], path)

  if ret == 0:
    success(path, name, out)
  else:
    failure(path)

def create_symlinks(links):
  for s,link in links.items():
    src = str(pathlib.Path(s).resolve())

    if os.path.exists(link): # Link already exists
      continue
    elif not os.path.exists(src): # Targer doesn't exist
      print('Skipping link {} to {} as {} doesnt exists'.format(link, src, src))
      continue

    pathlib.Path(link).parent.mkdir(parents=True, exist_ok=True)
    print('Creating symlink {} to {}'.format(link, src))
    os.symlink(src, link)

def recursive_walk(d, depth=0, parent=[]):
  for k, v in sorted(d.items(), key=lambda x: x[0]):
    if isinstance(v, dict):
      recursive_walk(v, depth+1, parent + [k])
      continue

    path = "/".join(parent + [k])
    if os.path.exists(path):
      continue

    if v.startswith('git@') or v.startswith('https://'):
      git_repos[v] = path
    else:
      sym_links[v] = path

def main():
  with open('_repos.yml', 'r') as f:
    repos = yaml.load(f)

  recursive_walk(repos)
  Parallel(n_jobs=get_cpu_count())(delayed(git_clone)(r,p) for r,p in git_repos.items())
  create_symlinks(sym_links)

git_repos = {}
sym_links = {}
main()
