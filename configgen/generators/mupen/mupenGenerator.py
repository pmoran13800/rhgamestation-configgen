#!/usr/bin/env python
import Command
import mupenConfig
import mupenControllers
import rhgamestationFiles
from generators.Generator import Generator


class MupenGenerator(Generator):
    # Main entry of the module
    # Configure mupen and return a command
    def generate(self, system, rom, playersControllers):
        # Settings rhgamestation default config file if no user defined one
        if not system.config['configfile']:
            # Using rhgamestation config file
            system.config['configfile'] = rhgamestationFiles.mupenCustom
            # Write configuration file
            mupenConfig.writeMupenConfig(system, playersControllers, rom)
            #  Write controllers configuration files
            mupenControllers.writeControllersConfig(playersControllers)

        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']], "--corelib", "/usr/lib/libmupen64plus.so.2.0.0", "--gfx", "/usr/lib/mupen64plus/mupen64plus-video-{}.so".format(system.config['core']),
                        "--configdir", rhgamestationFiles.mupenConf, "--datadir", rhgamestationFiles.mupenConf]
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])
        commandArray.append(rom)

        return Command.Command(videomode=system.config['videomode'], array=commandArray, env={"SDL_VIDEO_GL_DRIVER":"/usr/lib/libGLESv2.so"})
