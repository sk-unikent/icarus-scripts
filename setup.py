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
supportedpackages = {
    'base': '0.2.2',
    'python': '3.6.4',
    'tensorflow': '1.5.0',
    'julia': '0.6.2',
    'r': '3.4.2'
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
def upgradeBase(globalstate):
    print('Upgrading basic environment...')

    if globalstate['installed']['base'] < '0.2.2':
        # Add new upgrade check script.
        subprocess.call(['cp', scriptpath + '/env/.bash_updates', home + '/.config/kent/shellext/'])

    globalstate['installed']['base'] = supportedpackages['base']
    return globalstate

# Basic Kent environment setup.
def installBase(globalstate):
    if 'base' in globalstate['installed']:
        if globalstate['installed']['base'] == supportedpackages['base']:
            return globalstate
        return upgradeBase(globalstate)

    print('Setting up basic environment...')

    # Setup paths.
    subprocess.call(['mkdir', '-p', home + '/.config/kent/shellext'])
    subprocess.call(['mkdir', '-p', home + '/slurm/logs'])
    subprocess.call(['mkdir', '-p', home + '/slurm/examples/basic'])
    subprocess.call(['mkdir', '-p', home + '/.local/bin'])

    # Setup shell.
    subprocess.call(['cp', scriptpath + '/env/.bashrc', home + '/.bashrc'])
    subprocess.call(['cp', scriptpath + '/env/.bash_profile', home + '/.bash_profile'])
    subprocess.call(['cp', '-R', scriptpath + '/env/slurm/examples/basic', home + '/slurm/examples/'])
    replaceUsernameInExamples()

    globalstate['installed']['base'] = supportedpackages['base']
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

    globalstate['installed']['python'] = supportedpackages['python']
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

    globalstate['installed']['tensorflow'] = supportedpackages['tensorflow']
    return globalstate

# Install Julia.
def installJulia(globalstate):
    print('Installing Julia...')

    subprocess.call(['mkdir', '-p', home + '/julia'])
    subprocess.call(['tar', 'xzvf', '/opt/icarus/pkg/julia-0.6.2-linux-x86_64.tar.gz', '-C', home + '/julia'])
    subprocess.call(['ln', '-s', home + '/julia/julia-d386e40c17', home + '/julia/current'])
    subprocess.call(['ln', '-s', home + '/julia/julia-d386e40c17/bin/julia', home + '/.local/bin/julia062'])
    subprocess.call(['cp', scriptpath + '/env/.bash_julia', home + '/.config/kent/shellext/'])

    subprocess.call(['mkdir', '-p', home + '/slurm/examples/julia'])
    subprocess.call(['cp', '-R', scriptpath + '/env/slurm/examples/julia', home + '/slurm/examples/'])
    replaceUsernameInExamples()

    globalstate['installed']['julia'] = supportedpackages['julia']
    return globalstate

# Install R.
def installR(globalstate):
    if 'python' not in globalstate['installed']:
        globalstate = installPython(globalstate)
        if 'python' not in globalstate['installed']:
            print('Anaconda could not be installed, therefore I cannot install R')
            return globalstate

    print('Installing R...')

    subprocess.call([home + '/anaconda/bin/conda', 'install', 'r-essentials', '-y'])

    subprocess.call(['mkdir', '-p', home + '/slurm/examples/R'])
    subprocess.call(['cp', '-R', scriptpath + '/env/slurm/examples/R', home + '/slurm/examples/'])
    replaceUsernameInExamples()

    globalstate['installed']['r'] = supportedpackages['r']
    return globalstate

# Read in our environment's state.
def readEnvState():
    if not os.path.isfile(home + '/.config/kent/env.json'):
        return {'version': scriptvers, 'installed': {}}
    return json.load(open(home + '/.config/kent/env.json', 'r'))

# Save our environment's state.
def saveEnvState(state):
    if not os.path.isdir(home + '/.config'):
        os.mkdir(home + '/.config')
    if not os.path.isdir(home + '/.config/kent'):
        os.mkdir(home + '/.config/kent')
    json.dump(state, open(home + '/.config/kent/env.json', 'w'))

# Returns options for a given package dict.
def getPkgOptions(pkgs):
    globalstate = readEnvState()
    installoptions = [pkg.title() for pkg in pkgs.keys() if pkg not in globalstate['installed'].keys()]
    upgrades = [pkg.title() for pkg in globalstate['installed'].keys() if globalstate['installed'][pkg] != pkgs[pkg]]

    i = 0
    options = {}
    for pkg in upgrades:
        options[i] = {'name': pkg, 'type': 'Upgrade', 'command': "upgrade%s" % pkg}
        i += 1
    for pkg in installoptions:
        options[i] = {'name': pkg, 'type': 'Install', 'command': "install%s" % pkg}
        i += 1

    return options

# Setup globals and ask the user what they want to do.
def runInit():
    # First, decide what we have already installed.
    globalstate = readEnvState()

    # Build an options table.
    i = 1
    options = {}
    suppopts = getPkgOptions(supportedpackages)
    for pkg in suppopts:
        options[i] = suppopts[pkg]
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
        except KeyboardInterrupt:
            print("Quitting...")
            exit()

    # Check the answer.
    if answer not in options:
        return

    # Execute the command.
    command = options[answer]['command']
    if command == 'resetEnvironment':
        # Reset the environment, better check first.
        answer = input('Warning! This will delete everything in your home directory and you will not be able to get it back! are you sure? (yes/no) ')
        if answer == 'yes':
            globalstate = resetEnvironment(globalstate)
            saveEnvState(globalstate)
            runInit()
            return
        else:
            runInit()
            return
    elif options[answer]['type'] == 'Install' or options[answer]['type'] == 'Upgrade':
        # Make sure we always have the basic environment setup.
        globalstate = installBase(globalstate)
        saveEnvState(globalstate)

        # Now setup our tool.
        globalstate = globals()[command](globalstate)
        saveEnvState(globalstate)

        # Back to the start!
        runInit()
        return

if __name__ == '__main__':
    runInit()
