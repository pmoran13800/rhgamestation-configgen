#!/usr/bin/env python
import Command
import rhgamestationFiles
from generators.Generator import Generator
import os.path
import glob


class DosBoxGenerator(Generator):
    # Main entry of the module
    # Return command
    def generate(self, system, rom, playersControllers):
        # Find rom path
        gameDir = rom
        batFile = gameDir + "/dosbox.bat"
        gameConfFile = gameDir + "/dosbox.cfg"
           
        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']], 
			"-userconf", 
			"-exit", 
			"""{}""".format(batFile),
			"-c", """set ROOT={}""".format(gameDir),
			"-vkeybd", "/usr/share/dosbox"]
        if os.path.isfile(gameConfFile):
            commandArray.append("-conf")
            commandArray.append("""{}""".format(gameConfFile))
        else:
            commandArray.append("-conf")
            commandArray.append("""{}""".format(rhgamestationFiles.dosboxConfig))
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])
        return Command.Command(videomode='default', array=commandArray, env={"SDL_VIDEO_GL_DRIVER":"/usr/lib/libGLESv2.so"})
