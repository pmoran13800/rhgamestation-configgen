#!/usr/bin/env python
import Command
import rhgamestationFiles
from generators.Generator import Generator
import kodiConfig

class KodiGenerator(Generator):
    # Main entry of the module
    # Configure kodi inputs and return the command to run
    def generate(self, system, rom, playersControllers):
        kodiConfig.writeKodiConfig(playersControllers)
        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']]]
        return Command.Command(videomode=system.config['videomode'], array=commandArray)
