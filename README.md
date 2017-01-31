Batch-clone you Git repos
=====================

# What: 
Define all your Git repos and the folder structure they sould be organized (if you have one) in a YAML file and then just run the script. It uses the Git CLI for that.

> If you want to clone repos by SSH, make sure your keys are set and working.

# Why:
**I had a problem:** whenever I had to use a new PC at work or at home, I had to clone *several* Git repos. This quickly became a *PITA*, so I created this small Python script to do that for me.

# Feedback
All and any feedback, suggestion, improvement and/or bug-fix is highly appreciated. This is a small script but quite useful, so I hope it will also help others...

# Future
I hope to keep improving it. My task list is, so far:
- [ ] Support parameters on the command line:
  - [ ] Prefix Path
  - [ ] Config File
  - [ ] Git Key Location and/or User/Pass
- [ ] Function to manage the YAML from the command line (CRUD the config)
- [X] Clone repositories in **parallel**
- [ ] Error handling
- [ ] Package as PyPy
- [ ] Use a Git library (such as GitPython) instead of the CLI

Once again, any and all suggestion and feedback is much appreciated.

