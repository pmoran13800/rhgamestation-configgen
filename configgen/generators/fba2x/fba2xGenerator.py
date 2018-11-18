#!/usr/bin/env python
import Command
import fba2xControllers
import rhgamestationFiles
import fba2xConfig
import shutil
from generators.Generator import Generator
import os.path


class Fba2xGenerator(Generator):
    # Main entry of the module
    # Configure fba and return a command
    def generate(self, system, rom, playersControllers):
        # Settings rhgamestation default config file if no user defined one
        if not system.config['configfile']:
            # Using rhgamestation config file
            system.config['configfile'] = rhgamestationFiles.fbaCustom
            # Copy original fba2x.cfg
            shutil.copyfile(rhgamestationFiles.fbaCustomOrigin, rhgamestationFiles.fbaCustom)
            #  Write controllers configuration files
            fba2xControllers.writeControllersConfig(system, rom, playersControllers)
            # Write configuration to retroarchcustom.cfg
            fba2xConfig.writeFBAConfig(system)

        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']], "--configfile", system.config['configfile'], '--logfile', rhgamestationFiles.logdir+"/fba2x.log"]
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])
        commandArray.append(rom)
        return Command.Command(videomode=system.config['videomode'], array=commandArray)
