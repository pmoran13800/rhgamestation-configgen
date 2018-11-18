#!/usr/bin/env python
import Command
import rhgamestationFiles
from generators.Generator import Generator
import advMameControllers
import shutil
import os.path


class AdvMameGenerator(Generator):
    # Main entry of the module
    def generate(self, system, rom, playersControllers):
        romName = os.path.basename(os.path.splitext(rom)[0])
        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']]]
        
        if not system.config['configfile']:
            # Using rhgamestation config file
            system.config['configfile'] = rhgamestationFiles.advancemameConfig
            advMameControllers.writeControllersConfig(system, playersControllers)
            
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])
        
        commandArray.extend( ['-cfg', system.config['configfile']] )
        commandArray.append(romName)
        
        #~ return Command.Command(videomode=system.config['videomode'], array=commandArray, env={"TERM":"linux"})
        return Command.Command(videomode='default', array=commandArray, env={"TERM":"linux"})
