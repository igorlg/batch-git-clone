import yaml, subprocess, os

def git_clone(name, path):
	if not os.path.exists(path):
		print "Cloning %s into %s" % (name, path)
		subprocess.call(["git", "clone", v, path])
		print "Done!"

def recursive_walk(d, depth=0, parent=[]):
	for k, v in sorted(d.items(), key=lambda x: x[0]):
		if isinstance(v, dict):
			recursive_walk(v, depth+1, parent + [k])
		else:
			path = "/".join(parent + [k])
			git_clone(v, path)			

with open('_repos.yml', 'r') as f:
	repos = yaml.load(f)

recursive_walk(repos)
