#!/usr/bin/env python
import Command
import rhgamestationFiles
from generators.Generator import Generator
import os.path
import glob
import sys
import adfGenerator
import whdlGenerator
import cdGenerator
import utils.runner as runner
from functools import partial


class AmiberryGenerator(Generator):
    # Main entry of the module
    # Return command
    def generate(self, system, rom, playersControllers):
        print("Amiga Emulation")
        print("Params : <%s>, <%s>" % (system.name, rom))

        # ------------ CHECK entry params ------------
        if not os.path.exists(rom) or os.path.isdir(rom):
            raise IOError(
                "Please execute this script on full path to an uae adf or cue like /rhgamestation/share/roms/amiga/gamename.uae\nFor uae file, the game folder should be named exactly alike and be in the same folder : /rhgamestation/share/roms/amiga/gamename")

        # command params
        uaeName = os.path.basename(rom)
        romFolder = os.path.dirname(rom)
        romType = uaeName[-3:].lower()
        gameName = uaeName[0:len(uaeName) - 4]

        # detect bad parameters
        if not uaeName or not romFolder or not gameName or not len(romType) == 3 or romType.lower() not in ['adf',
                                                                                                            'uae',
                                                                                                            'cue',
                                                                                                            'iso']:
            raise IOError("Please execute this script on an uae or adf file only")

        print("Launching game <%s> of type <%s> from <%s>" % (gameName, romType, romFolder))

        if len(playersControllers) > 0:
            controller = playersControllers['1']
        else:
            print("No controller found")
            controller = None

        # ------------ Prepare WHDL reference dictionary ------------
        referenceWHDL = {}

        # ------------ Launch ADF ------------
        if romType == "adf":
            if not os.path.exists(os.path.join(romFolder, uaeName)):
                raise IOError("ADF file " + romFolder + "/" + uaeName + "doesn't exist")

            adfGenerator.generateAdf(rom, romFolder, uaeName, system.name, controller)

        # ------------ Launch WHD ------------
        elif romType == "uae":
            whdlDir = os.path.join(romFolder, gameName)
            whdlZip = whdlDir + ".zip"
            if not os.path.exists(whdlZip) or os.path.isdir(whdlZip):
                if not os.path.exists(whdlDir) or not os.path.isdir(whdlDir):
                    raise IOError(
                        "No WHDLoad folder <" + whdlDir + "> corresponding to your uae file " + romFolder + "/" + uaeName)

            referenceWHDL = whdlGenerator.generateWHDL(rom, romFolder, gameName, system.name, controller)

        # ----------- Launch CD32 (and maybe amiga CD in the future) --------------"
        elif romType == "cue" or romType == "iso":
            if not os.path.exists(os.path.join(romFolder, uaeName)):
                raise IOError("CD file " + romFolder + "/" + uaeName + "doesn't exist")

            cdGenerator.generateCD(rom, romFolder, uaeName, system.name, controller)

        postExec = partial(whdlGenerator.handleBackupFromGame, rom, romFolder, gameName,
                           system.name, referenceWHDL) if romType == "uae" else None

        # Kept for future debug purposes on unpatched version
        # mandatory change of current working dir to amiberry's one
        # os.chdir(os.path.join(rhgamestationFiles.amiberryMountPoint,"amiberry"))
        # print("Executing %s in %s" % ("amiberry",os.getcwd()))
        # os.popen("./amiberry")
        # Handle backup for WHDL
        # if romType == "uae" :
        # whdlGenerator.handleBackup(rom,romFolder,gameName,system.name)
        # sys.exit()

        commandArray = [os.path.join(rhgamestationFiles.amiberryMountPoint, "amiberry", "amiberry")]
        return Command.Command(videomode='default', array=commandArray,
                               env={"SDL_VIDEO_GL_DRIVER": "/usr/lib/libGLESv2.so",
                                    "SDL_VIDEO_EGL_DRIVER": "/usr/lib/libGLESv2.so"},
                               cwdPath=os.path.join(rhgamestationFiles.amiberryMountPoint, "amiberry"), postExec=postExec)
