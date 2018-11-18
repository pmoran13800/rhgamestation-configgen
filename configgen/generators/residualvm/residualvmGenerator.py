#!/usr/bin/env python
import Command
import rhgamestationFiles
from generators.Generator import Generator
import os.path
import glob


class ResidualVMGenerator(Generator):
    # Main entry of the module
    # Return residualvm command
    def generate(self, system, rom, playersControllers):
        # Find rom path
        if os.path.isdir(rom):
          # rom is a directory: must contains a <game name>.residualvm file
          romPath = rom
          romFile = glob.glob(romPath + "/*.residualvm")[0]
          romName = os.path.splitext(os.path.basename(romFile))[0]
        else:
          # rom is a file: split in directory and file name
          romPath = os.path.dirname(rom)
          romName = os.path.splitext(os.path.basename(rom))[0]
        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']], 
                        "--fullscreen",
                        "--joystick=0", 
#                       "--screenshotpath="+rhgamestationFiles.screenshotsDir, 
                        "--extrapath=/usr/share/residualvm",
                        "--savepath="+rhgamestationFiles.residualvmSaves,
                        "--path=""{}""".format(romPath)]
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])
        commandArray.append("""{}""".format(romName))

        return Command.Command(videomode='default', array=commandArray, env={"SDL_VIDEO_GL_DRIVER":"/usr/lib/libGLESv2.so","SDL_VIDEO_EGL_DRIVER":"/usr/lib/libGLESv2.so"})
