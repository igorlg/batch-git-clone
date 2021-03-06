from termcolor import colored
from subprocess import Popen, PIPE
from multiprocessing import cpu_count
import re

def get_cpu_count():
  return cpu_count()

def git(commands, path=None):
  try:
    cmd = ['git'] + commands
  except:
    cmd = ['git'] + [commands]

  run = Popen(cmd,
              stdout=PIPE,
              stderr=PIPE,
              cwd=path)
  run.wait()

  err = [l.strip() for l in run.stderr]
  if run.returncode == 0:
    out = [l.strip() for l in run.stdout]
  else:
    out = []
  return out, err, run.returncode

def pprint(text, index):
  colors = [ 'white', 'blue', 'yellow', 'green']
  i = index % len(colors)
  print(colored(text, colors[i]))

def filter_output(line):
  try:
    if (
      not line.startswith('Warning: Permanently added')
      and not line.startswith('See git-pull(1) for details.')
      and not line.startswith('git pull <remote> <branch>')
    ):
      return str(line.strip())
    else:
      return ''
  except:
    return str(line.strip())

def git_branch_name(path):
  out, err, ret = git(['rev-parse', '--abbrev-ref', 'HEAD'], path)
  return out

def git_remotes(path):
  out, err, ret = git(['remote', '-v'], path)
  if ret == 0:
    for r in out:
      try:
        return re.search('^\w+\s+(.+)\s\(fetch\)$', r.decode("utf-8")).group(1)
      except AttributeError:
        return None
  return None
