from joblib import Parallel, delayed
from termcolor import colored
import multiprocessing
import yaml, subprocess, os

def pprint(text, index):
  colors = [ 'white', 'blue', 'yellow', 'green']
  i = index % len(colors)
  print colored(text, colors[i])

def git(commands, path):
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
    and not line.startswith('See git-pull(1) for details.') 
    and not line.startswith('git pull <remote> <branch>')
  ):
    return line.strip()

def success(path, run):
  out = [filter_output(l) for l in run.stdout]
  out.append("Done pulling %s" % path)
  return out

def failure(path, run):
  print colored("Failed to pull %s" % path, 'red')

def git_branch_name(path):
  cmd = git(['rev-parse', '--abbrev-ref', 'HEAD'], path)

  if cmd.returncode == 0:
    lines = [l.strip() for l in cmd.stdout]
    return lines[0]
  else:
    return 'master'

def git_remote_branches(path):
  cmd = git(['branch', '-l', '-r'], path)

  if cmd.returncode == 0:
    return [l.strip() for l in cmd.stdout]
  else:
    return []

def has_remote(branch, path):
  remotes = git_remote_branches(path)
  for l in remotes:
    if branch in l:
      return True
  return False

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

with open('_repos.yml', 'r') as f:
  repos = yaml.load(f)

num_cores = multiprocessing.cpu_count()
paths     = []

recursive_walk(repos)
Parallel(n_jobs=num_cores)(delayed(git_pull)(p,i) for i, p in enumerate(paths))
