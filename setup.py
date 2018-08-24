#
# New Icarus setup script.
# Version: 2.1
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
    'base': '0.3.0',
    'python': '3.6.4',
    'tensorflow': '1.5.0',
    'julia': '0.6.2',
    'r': '3.5.0'
}

bioscience_packages = {
    'bwa': '0.7.12',
    'picard-tools': '2.17',
    'samtools': '1.2',
    'bcftools': '3.4.2',
    'ensembl-vep': '91.3',
    'htslib': '1.7'
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

    if globalstate['installed']['base'] < '0.2.3':
        subprocess.call(['mkdir', '-p', home + '/.local/lib'])
        subprocess.call(['mkdir', '-p', home + '/.local/include'])
        subprocess.call(['mkdir', '-p', home + '/.local/share'])

    if globalstate['installed']['base'] < '0.3.0':
        # Install Spack.
        subprocess.call(['git', 'clone', 'https://github.com/spack/spack.git', home + '/.spack-base'])
        subprocess.call(['cp', scriptpath + '/env/.bash_spack', home + '/.config/kent/shellext/'])
        subprocess.call(['~/.spack-base/bin/spack', 'bootstrap'])

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

    globalstate['installed']['base'] = '0.2.0'
    globalstate = upgradeBase(globalstate)

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

    subprocess.call(['cp', scriptpath + '/env/.Rprofile', home + '/.Rprofile'])

    subprocess.call(['mkdir', '-p', home + '/slurm/examples/R'])
    subprocess.call(['cp', '-R', scriptpath + '/env/slurm/examples/R', home + '/slurm/examples/'])
    replaceUsernameInExamples()

    globalstate['installed']['r'] = supportedpackages['r']
    return globalstate

# R environment setup.
def upgradeR(globalstate):
    print('Upgrading R...')

    if globalstate['installed']['base'] < '3.5.0':
        subprocess.call([home + '/anaconda/bin/conda', 'update', 'r-essentials', '-y'])
        subprocess.call(['cp', scriptpath + '/env/.Rprofile', home + '/.Rprofile'])

    globalstate['installed']['base'] = supportedpackages['base']
    return globalstate

# Install BWA.
def installBwa(globalstate):
    print('Installing BWA...')

    subprocess.call(['cp', scriptpath + '/pkg/biosciences/bwa/bwa', home + '/.local/bin/'])

    globalstate['installed']['bwa'] = bioscience_packages['bwa']
    return globalstate

# Install picard-tools.
def installPicardTools(globalstate):
    print('Installing Picard-Tools...')

    subprocess.call(['cp', scriptpath + '/pkg/biosciences/picard-tools/picard-2.17.10-6-g6a44477-SNAPSHOT-all.jar', home + '/.local/lib/'])
    subprocess.call(['ln', '-s', home + '/.local/lib/picard-2.17.10-6-g6a44477-SNAPSHOT-all.jar', home + '/.local/lib/picard.jar'])
    subprocess.call(['cp', scriptpath + '/env/.bash_picard', home + '/.config/kent/shellext/'])

    globalstate['installed']['picard-tools'] = bioscience_packages['picard-tools']
    return globalstate

# Install HTS Lib.
def installHtslib(globalstate):
    print('Installing HTSLib...')

    subprocess.call(['tar', '-xf', scriptpath + '/pkg/biosciences/htslib/htslib.tar.xz', '-C', home + '/.local/'])

    globalstate['installed']['htslib'] = bioscience_packages['htslib']
    return globalstate

# Install SamTools.
def installSamtools(globalstate):
    print('Installing SamTools...')

    if 'htslib' not in globalstate['installed']:
        globalstate = installHtslib(globalstate)
        if 'htslib' not in globalstate['installed']:
            print('HTSLib could not be installed, therefore I cannot install SamTools')
            return globalstate

    subprocess.call(['tar', '-xf', scriptpath + '/pkg/biosciences/samtools/samtools.tar.xz', '-C', home + '/.local/'])

    globalstate['installed']['samtools'] = bioscience_packages['samtools']
    return globalstate

# Install ensembl-vep.
def installEnsemblVep(globalstate):
    print('Installing ensembl-vep...')

    subprocess.call(['mkdir', '-p', home + '/.ensembl'])
    subprocess.call(['tar', '-xzf', scriptpath + '/pkg/biosciences/ensembl-vep/91.3.tar.gz', '-C', home + '/.ensembl/'])
    subprocess.call(['perl', '-xzf', home + '/.ensembl/ensembl-vep-release-91.3/INSTALL.pl',' --NO_HTSLIB', '--AUTO=a', '--QUIET'])
    subprocess.call(['ln', '-s', home + '/.ensembl/ensembl-vep-release-91.3/vep', home + '/.local/bin/vep'])
    subprocess.call(['ln', '-s', home + '/.ensembl/ensembl-vep-release-91.3/variant_recoder', home + '/.local/bin/variant_recoder'])
    subprocess.call(['ln', '-s', home + '/.ensembl/ensembl-vep-release-91.3/haplo', home + '/.local/bin/haplo'])
    subprocess.call(['ln', '-s', home + '/.ensembl/ensembl-vep-release-91.3/filter_vep', home + '/.local/bin/filter_vep'])

    print('Ensembl-vep has been installed at ~/.ensembl.')

    globalstate['installed']['ensembl-vep'] = bioscience_packages['ensembl-vep']
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

# Show a menu with options.
def showMenu(message, options):
    # Print out options.
    print(message)
    for i in options:
        print(" %i) %s %s" % (i, options[i]['type'], options[i]['name']))

    # Work out what we want to do.
    answer = 99999
    while answer not in options.keys():
        try: answer = int(input('> '))
        except ValueError: pass
        except EOFError:
            print('')
            pass
        except KeyboardInterrupt:
            print("Quitting...")
            exit()

    # Check the answer.
    if answer not in options:
        return

    return options[answer]


# Returns options for a given package dict.
def getPkgOptions(pkgs):
    globalstate = readEnvState()
    installoptions = [pkg.title().replace('-', '') for pkg in pkgs.keys() if pkg not in globalstate['installed'].keys()]
    upgrades = [pkg.title().replace('-', '') for pkg in globalstate['installed'].keys() if pkg in pkgs and globalstate['installed'][pkg] != pkgs[pkg]]

    i = 0
    options = {}
    for pkg in upgrades:
        options[i] = {'name': pkg, 'type': 'Upgrade', 'command': "upgrade%s" % pkg}
        i += 1
    for pkg in installoptions:
        options[i] = {'name': pkg, 'type': 'Install', 'command': "install%s" % pkg}
        i += 1

    return options

# Process response.
def processMenuResponse(globalstate, answer):
    command = answer['command']

    if command == 'resetEnvironment':
        # Reset the environment, better check first.
        checkresp = input('Warning! This will delete everything in your home directory and you will not be able to get it back! are you sure? (yes/no) ')
        if checkresp == 'yes':
            globalstate = resetEnvironment(globalstate)
            saveEnvState(globalstate)
        return globalstate

    if answer['type'] == 'Install' or answer['type'] == 'Upgrade':
        # Make sure we always have the basic environment setup.
        globalstate = installBase(globalstate)
        saveEnvState(globalstate)

        # Now setup our tool.
        globalstate = globals()[command](globalstate)
        saveEnvState(globalstate)
        return globalstate

    # Just run it, this should return a global state.
    if command in globals():
        return globals()[command](globalstate)

    exit()

# Setup globals and ask the user what they want to do.
def showBiosciencesMenu(globalstate):
    # Build an options table.
    i = 1
    options = {}

    # Bioscience options.
    suppopts = getPkgOptions(bioscience_packages)
    for pkg in suppopts:
        options[i] = suppopts[pkg]
        i += 1

    options[i] = {'name': 'Back', 'type': 'Go', 'command': "showMainMenu"}

    # Print out options.
    answer = showMenu('Bioscience packages', options)
    if not answer:
        return

    globalstate = processMenuResponse(globalstate, answer)
    showBiosciencesMenu(globalstate)

# Setup globals and ask the user what they want to do.
def showMainMenu(globalstate):
    # Build an options table.
    i = 1
    options = {}

    # Core options.
    suppopts = getPkgOptions(supportedpackages)
    for pkg in suppopts:
        options[i] = suppopts[pkg]
        i += 1

    options[i] = {'name': 'Biosciences', 'type': 'Show', 'command': "showBiosciencesMenu"}
    i += 1
    options[i] = {'name': 'environment', 'type': 'Reset', 'command': "resetEnvironment"}
    i += 1
    options[i] = {'name': ' ', 'type': 'Quit', 'command': "quit"}

    # Print out options.
    answer = showMenu('Welcome to Icarus! What would you like to do?', options)
    if not answer:
        return

    globalstate = processMenuResponse(globalstate, answer)
    showMainMenu(globalstate)

if __name__ == '__main__':
    globalstate = readEnvState()
    showMainMenu(globalstate)
