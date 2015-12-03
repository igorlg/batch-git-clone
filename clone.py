import yaml, subprocess, os

def recursive_walk(d, depth=0, parent=[]):
	for k, v in sorted(d.items(), key=lambda x: x[0]):
		if isinstance(v, dict):
			recursive_walk(v, depth+1, parent + [k])
		else:
			path = "/".join(parent + [k])
			if not os.path.exists(path):
				subprocess.call(["git", "clone", v, path])

with open('repos.yml', 'r') as f:
	repos = yaml.load(f)

recursive_walk(repos)
