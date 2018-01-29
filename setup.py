#
# New Icarus setup script.
# Version: 2.0
# Author: Skylar Kelty
#

import os
import pwd
import glob
import json
import shutil
import readline
import subprocess

# Globals.
home = os.path.expanduser("~")
scriptpath = os.path.dirname(os.path.realpath(__file__))
scriptvers = '2.0'
basicenvvers = '0.2.0'
supportedpackages = {
    'python': '3.6.4',
    'tensorflow': '1.5.0'
}

# Fix Python 2.x input.
try: input = raw_input
except NameError: pass

# Reset the user's environment.
def resetEnvironment(globalstate):
    subprocess.call(['rm', '-rf', home + '/slurm'])
    subprocess.call(['rm', '-rf', home + '/.bashrc'])
    subprocess.call(['rm', '-rf', home + '/anaconda'])
    subprocess.call(['rm', '-rf', home + '/.config/kent'])
    subprocess.call(['rm', '-rf', home + '/.bash_profile'])

    return readEnvState()

# Replace username in template files.
def replaceUsernameInExamples():
    username = pwd.getpwuid(os.getuid())[0]
    for filename in glob.glob(home + '/slurm/examples/*/*.sh'):
        subprocess.call(['sed', '-i', "s/USERNAME/%s/g" % username, filename])

# Basic Kent environment setup.
def ensureBasicEnvironment(globalstate):
    if 'basesetup' in globalstate and globalstate['basesetup'] == basicenvvers:
        return globalstate

    print('Setting up basic environment...')

    # Setup paths.
    subprocess.call(['mkdir', '-p', home + '/.config/kent/shellext'])
    subprocess.call(['mkdir', '-p', home + '/slurm/logs'])
    subprocess.call(['mkdir', '-p', home + '/slurm/examples/basic'])

    # Setup shell.
    subprocess.call(['cp', scriptpath + '/env/.bashrc', home + '/.bashrc'])
    subprocess.call(['cp', scriptpath + '/env/.bash_profile', home + '/.bash_profile'])
    subprocess.call(['cp', '-R', scriptpath + '/env/slurm/examples/basic', home + '/slurm/examples/'])
    replaceUsernameInExamples()

    globalstate['basesetup'] = basicenvvers
    return globalstate

# Install Python.
def installPython(globalstate):
    print('Installing Python...')

    subprocess.call(['/bin/bash', '/opt/icarus/pkg/Anaconda3-5.0.1-Linux-x86_64.sh', '-b', '-p', home + '/anaconda'])
    subprocess.call(['cp', scriptpath + '/env/.bash_python', home + '/.config/kent/shellext/'])
    subprocess.call([home + '/anaconda/bin/conda', 'update', '--all', '-y'])

    subprocess.call(['mkdir', '-p', home + '/slurm/examples/python'])
    subprocess.call(['cp', '-R', scriptpath + '/env/slurm/examples/python', home + '/slurm/examples/'])
    replaceUsernameInExamples()

    globalstate['python'] = supportedpackages['python']
    return globalstate

# Install Tensorflow.
def installTensorflow(globalstate):
    if 'python' not in globalstate['installed']:
        globalstate = installPython(globalstate)
        if 'python' not in globalstate['installed']:
            print('Python was not installed, therefore I cannot install Tensorflow')
            return globalstate

    print('Installing Tensorflow...')

    subprocess.call([home + '/anaconda/bin/pip', 'install', '--upgrade', '/opt/icarus/pkg/tensorflow-1.5.0-cp36-cp36m-linux_x86_64.whl'])

    subprocess.call(['mkdir', '-p', home + '/slurm/examples/tensorflow'])
    subprocess.call(['cp', '-R', scriptpath + '/env/slurm/examples/tensorflow', home + '/slurm/examples/'])
    replaceUsernameInExamples()

    globalstate['tensorflow'] = supportedpackages['tensorflow']
    return globalstate

# Read in our environment's state.
def readEnvState():
    if not os.path.isfile(home + '/.config/kent/env.json'):
        return {'version': scriptvers, 'installed': {}}
    return json.load(open(home + '/.config/kent/env.json'))

# Save our environment's state.
def saveEnvState(state):
    if not os.path.isdir(home + '/.config'):
        os.mkdir(home + '/.config')
    if not os.path.isdir(home + '/.config/kent'):
        os.mkdir(home + '/.config/kent')
    json.dump(state, open(home + '/.config/kent/env.json', 'w'))

# Setup globals and ask the user what they want to do.
def runInit():
    # First, decide what we have already installed.
    globalstate = readEnvState()
    installoptions = [pkg.title() for pkg in supportedpackages.keys() if pkg not in globalstate['installed'].keys()]

    # Build an options table.
    i = 1
    options = {}
    for pkg in installoptions:
        options[i] = {'name': pkg, 'type': 'Install', 'command': "install%s" % pkg}
        i += 1

    options[i] = {'name': 'environment', 'type': 'Reset', 'command': "resetEnvironment"}
    i += 1
    options[i] = {'name': ' ', 'type': 'Quit', 'command': "quit"}

    # Print out options.
    print('Welcome to Icarus! What would you like to do?')
    for i in options:
        print(" %i) %s %s" % (i, options[i]['type'], options[i]['name']))

    # Work out what we want to do.
    answer = 99999
    while answer not in options.keys():
        try: answer = int(input('> '))
        except ValueError: pass
    command = options[answer]['command']

    # Reset the environment, better check first.
    if command == 'resetEnvironment':
        answer = input('Warning! This will delete everything in your home directory and you will not be able to get it back! are you sure? (yes/no) ')
        if answer == 'yes':
            globalstate = resetEnvironment(globalstate)
            saveEnvState(globalstate)
            runInit()
            return
        else:
            runInit()
            return
    elif options[answer]['type'] == 'Install':
        # Make sure we always have the basic environment setup.
        globalstate = ensureBasicEnvironment(globalstate)
        saveEnvState(globalstate)

        # Now setup our tool.
        globalstate = globals()[command](globalstate)
        saveEnvState(globalstate)

        # Back to the start!
        runInit()
        return

if __name__ == '__main__':
    runInit()
