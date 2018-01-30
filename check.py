#
# Check for updates
# Version: 2.0
# Author: Skylar Kelty
#

from setup import readEnvState, saveEnvState, supportedpackages

globalstate = readEnvState()
upgrades = [pkg.title() for pkg in globalstate['installed'].keys() if globalstate['installed'][pkg] != supportedpackages[pkg]]
if len(upgrades) > 0:
    print("There are updates available for your environment!")
