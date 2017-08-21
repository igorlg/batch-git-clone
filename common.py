from termcolor import colored
from subprocess import Popen, PIPE
from multiprocessing import cpu_count

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
  return run

def pprint(text, index):
  colors = [ 'white', 'blue', 'yellow', 'green']
  i = index % len(colors)
  print colored(text, colors[i])

def filter_output(line):
  if (
    not line.startswith('Warning: Permanently added')
    and not line.startswith('See git-pull(1) for details.') 
    and not line.startswith('git pull <remote> <branch>')
  ):
    return line.strip()

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
