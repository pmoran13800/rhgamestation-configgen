#!/usr/bin/env python
import Command
#~ import reicastControllers
import rhgamestationFiles
from generators.Generator import Generator
import reicastControllers
import shutil
import os.path
import ConfigParser
import glob
import sys

class ReicastGenerator(Generator):
    # Main entry of the module
    def config_upgrade(self, version):
        '''
        Upgrade the user's configuration file with new values added to the
        system configuration file upgraded by S11Share:do_upgrade()

        Args:
            version (str): New RHGamestation version

        Returns (bool):
            Returns True if this Generators sucessfully handled the upgrade.
        '''
        # Copy the bios from share_init to share if it doesn't exis
        try:
            reicastBiosFileInit = rhgamestationFiles.BIOS_INIT + '/dc_nvmem.bin'
            reicastBiosFile = rhgamestationFiles.BIOS + '/dc_nvmem.bin'
            if os.path.isfile(reicastBiosFileInit) and not os.path.isfile(reicastBiosFile):
                shutil.copy2(reicastBiosFileInit, reicastBiosFile)

            # Copy the VMUs
            if not os.path.exists(rhgamestationFiles.SAVES + '/dreamcast/reicast/'):
                    os.makedirs(rhgamestationFiles.SAVES + '/dreamcast/reicast/')
            for srcFile in glob.glob(rhgamestationFiles.SAVES_INIT + '/dreamcast/reicast/vmu_save_*.bin'):
                destFile = rhgamestationFiles.SAVES + '/dreamcast/reicast/' + os.path.basename(srcFile)
                # Don't copy if the destination already exists
                if os.path.isfile(destFile): continue
                shutil.copy2(srcFile, destFile)

            print("ReicastGenerator 's configuration successfully upgraded")
            return True
        except Exception as e:
            #print(e)
            print("ReicastGenerator 's configuration failed!")
            return False

    # Configure fba and return a command
    def generate(self, system, rom, playersControllers):
        if not system.config['configfile']:
            # Write emu.cfg to map joysticks, init with the default emu.cfg
            Config = ConfigParser.ConfigParser()
            Config.optionxform = str
            Config.read(rhgamestationFiles.reicastConfigInit)
            section = "input"
            # For each pad detected
            for index in playersControllers :
                controller = playersControllers[index]
                # Get the event number
                eventNum = controller.dev.replace('/dev/input/event','')
                # Write its mapping file
                controllerConfigFile = reicastControllers.generateControllerConfig(controller)
                # set the evdev_device_id_X
                Config.set(section, 'evdev_device_id_' + controller.player, eventNum)
                # Set the evdev_mapping_X
                Config.set(section, 'evdev_mapping_' + controller.player, controllerConfigFile)

            cfgfile = open(rhgamestationFiles.reicastConfig,'w+')
            Config.write(cfgfile)
            cfgfile.close()
                
        # the command to run  
        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']]]
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])
        commandArray.append(rom)
        # Here is the trick to make reicast find files :
        # emu.cfg is in $XDG_CONFIG_DIRS or $XDG_CONFIG_HOME. The latter is better
        # VMU will be in $XDG_DATA_HOME because it needs rw access -> /rhgamestation/share/saves/dreamcast
        # BIOS will be in $XDG_DATA_DIRS
        # controller cfg files are set with an absolute path, so no worry
        return Command.Command(videomode=system.config['videomode'], array=commandArray, env={"XDG_CONFIG_HOME":rhgamestationFiles.CONF, "XDG_DATA_HOME":rhgamestationFiles.reicastSaves, "XDG_DATA_DIRS":rhgamestationFiles.reicastBios})
