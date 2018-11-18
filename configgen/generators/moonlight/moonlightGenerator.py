#!/usr/bin/env python
import Command
import rhgamestationFiles
import controllersConfig
from generators.Generator import Generator
import shutil
import os.path


class MoonlightGenerator(Generator):
    # Main entry of the module
    # Configure fba and return a command
    def generate(self, system, rom, playersControllers):
        outputFile = rhgamestationFiles.moonlightCustom + '/gamecontrollerdb.txt'
        configFile = controllersConfig.generateSDLGameDBAllControllers(playersControllers, outputFile)
        gameName,confFile = self.getRealGameNameAndConfigFile(rom)
        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']], 'stream','-config',  confFile]
        if 'args' in system.config and system.config['args'] is not None:
             commandArray.extend(system.config['args'])
        commandArray.append('-app')
        commandArray.append(gameName)
        return Command.Command(videomode='default', array=commandArray, env={"XDG_DATA_DIRS": rhgamestationFiles.CONF})

    def getRealGameNameAndConfigFile(self, rom):
        # Rom's basename without extension
        romName = os.path.splitext(os.path.basename(rom))[0]
        # find the real game name
        f = open(rhgamestationFiles.moonlightGamelist, 'r')
        for line in f:
            try:
                gfeRom, gfeGame, confFile = line.rstrip().split(';')
                #confFile = confFile.rstrip()
            except:
                gfeRom, gfeGame = line.split(';')
                confFile = rhgamestationFiles.moonlightConfig
            #If found
            if gfeRom == romName:
                # return it
                f.close()
                return [gfeGame, confFile]
        # If nothing is found (old gamelist file format ?)
        return [gfeGame, rhgamestationFiles.moonlightConfig]
