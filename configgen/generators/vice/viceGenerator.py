#!/usr/bin/env python
import Command
import rhgamestationFiles
from generators.Generator import Generator
import os.path
import glob


class ViceGenerator(Generator):
    # Main entry of the module
    # Return command
    def generate(self, system, rom, playersControllers):
        # Settings rhgamestation default config file if no user defined one
        if not system.config['configfile']:
            # Using rhgamestation config file
            #system.config['configfile'] = rhgamestationFiles.mupenCustom
            pass
        # Find rom path
        romPath = os.path.dirname(rom)
        romName = os.path.splitext(os.path.basename(rom))[0]

        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']], 
                        "-config", rhgamestationFiles.viceConfig,
                        "-autostart", rom]
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])

        return Command.Command(videomode='default', array=commandArray,  env={"SDL_VIDEO_GL_DRIVER": "/usr/lib/libGLESv2.so"})
