from joblib import Parallel, delayed
import multiprocessing
import yaml, subprocess, os

def git(commands, path=None):
  try:
    cmd = ['git'] + commands
  except:
    cmd = ['git'] + [commands]

  run = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=path)
  run.wait()
  return run

def filter_output(line):
  if (
    not line.startswith('Warning: Permanently added')
  ):
    print line.strip()

def success(path, run):
  for l in run.stdout: filter_output(l)
  print "Done pulling " + path

def failure(path, run):
  for l in run.stderr: filter_output(l)
  print "Failed to pull " + path

def git_clone(name, path):
  print "Cloning " + name + " into " + path
  clone = git(['clone', name, path])

  if pull.returncode == 0:
    success(path, pull)
  else:
    failure(path, pull)

def recursive_walk(d, depth=0, parent=[]):
  for k, v in sorted(d.items(), key=lambda x: x[0]):
    if isinstance(v, dict):
      recursive_walk(v, depth+1, parent + [k])
    else:
      path = "/".join(parent + [k])
      if not os.path.exists(path):
        git_repos[v] = path

with open('_repos.yml', 'r') as f:
  repos = yaml.load(f)

num_cores = multiprocessing.cpu_count()
git_repos = {}

recursive_walk(repos)
Parallel(n_jobs=num_cores)(delayed(git_clone)(r,p) for r,p in git_repos.iteritems())
