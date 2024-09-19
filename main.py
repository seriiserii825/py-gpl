import os
import subprocess
from git import Repo

def pipInstall():
    # check for venv
    if not os.path.exists('venv'):
        os.system('python3 -m venv venv')
        os.system('source venv/bin/activate')
        os.system('python3 -m pip install --upgrade pip')
        os.system('python3 -m pip install -r requirements.txt')
        os.system('deactivate')
    else:
        os.system('source venv/bin/activate')
        os.system('python3 -m pip install -r requirements.txt')
        os.system('deactivate')

def gitPull():
    repo = Repo('.')
    command = f"git remote update && git status -uno | grep -q 'Your branch is behind'"
    result = os.system(command)
    if result == 0:
        repo.git.pull()


def gitModules():
    os.system('git submodule init')
    os.system('git submodule update')
    # get submodule dirs from .gitmodules
    with open('.gitmodules') as f:
        lines = f.readlines()
        for line in lines:
            if 'path' in line:
                path = line.split('=')[1].strip()
                os.chdir(path)
                gitPull()
                os.chdir('..')

def check_if_pull_needed():
    # Fetch the latest updates from the remote
    subprocess.run(['git', 'fetch'], check=True)
    
    # Check the status between local and remote
    local_commit = subprocess.check_output(['git', 'rev-parse', '@'], text=True).strip()
    remote_commit = subprocess.check_output(['git', 'rev-parse', '@{u}'], text=True).strip()
    base_commit = subprocess.check_output(['git', 'merge-base', '@', '@{u}'], text=True).strip()

    if local_commit == remote_commit:
        print("Your branch is up to date with the remote.")
        return False
    elif local_commit == base_commit:
        print("You need to pull the latest changes.")
        return True
    elif remote_commit == base_commit:
        print("You have unpushed local changes.")
        return False
    else:
        print("Your branch has diverged from the remote.")
        return True

result = check_if_pull_needed()
print(f"result: {result}")

repo = Repo('.')
if result:
    repo.git.pull()
    # check for python files
    if os.path.exists('requirements.txt'):
        pipInstall()
    # check for gitmodules
    if os.path.exists('.gitmodules'):
        gitModules()
