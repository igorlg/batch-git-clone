from joblib import Parallel, delayed
import multiprocessing
import yaml, subprocess, os

def git_pull(path):
  basepath = os.path.dirname(os.path.abspath(__file__))
  if os.path.exists(path):
    os.chdir(path)
    print "Pulling " + path
    subprocess.call(["git", "pull"])
    # print "Done!"
    os.chdir(basepath)

def recursive_walk(d, depth=0, parent=[]):
  for k, v in sorted(d.items(), key=lambda x: x[0]):
    if isinstance(v, dict):
      recursive_walk(v, depth+1, parent + [k])
    else:
      path = "/".join(parent + [k])
      paths.append(path)
      # git_pull(path)

with open('_repos.yml', 'r') as f:
  repos = yaml.load(f)

num_cores = multiprocessing.cpu_count()
paths     = []

recursive_walk(repos)
Parallel(n_jobs=num_cores)(delayed(git_pull)(p) for p in paths)
