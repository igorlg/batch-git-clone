from joblib import Parallel, delayed
import multiprocessing
import yaml, subprocess, os

def git_clone(name, path):
	if not os.path.exists(path):
		subprocess.call(["git", "clone", name, path])
		print "Done!"

def recursive_walk(d, depth=0, parent=[]):
	for k, v in sorted(d.items(), key=lambda x: x[0]):
		if isinstance(v, dict):
			recursive_walk(v, depth+1, parent + [k])
		else:
			path = "/".join(parent + [k])
			# git_clone(v, path)
			# git_repos.append({v: path})
			git_repos[v] = path

with open('_repos.yml', 'r') as f:
	repos = yaml.load(f)

num_cores = multiprocessing.cpu_count()
git_repos = {}

recursive_walk(repos)
Parallel(n_jobs=num_cores)(delayed(git_clone)(r,p) for r,p in git_repos.iteritems())
