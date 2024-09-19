import os
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


repo = Repo('.')
print(os.getcwd())
command = f"git remote update && git status -uno | grep -q 'Your branch is behind'"
result = os.system(command)
if result == 0:
    repo.git.pull()
    # check for python files
    if os.path.exists('requirements.txt'):
        pipInstall()
    # check for gitmodules
    if os.path.exists('.gitmodules'):
        gitModules()
