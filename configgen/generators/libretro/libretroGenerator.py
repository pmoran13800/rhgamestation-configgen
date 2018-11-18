#!/usr/bin/env python
import Command
import libretroControllers
import rhgamestationFiles
import libretroConfig
import shutil
from generators.Generator import Generator
import os.path


class LibretroGenerator(Generator):
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
        return libretroConfig.updateLibretroConfig(version)
    
    
    # Configure retroarch and return a command
    def generate(self, system, rom, playersControllers):
        # Settings rhgamestation default config file if no user defined one
        if not system.config['configfile']:
            # Using rhgamestation config file
            system.config['configfile'] = rhgamestationFiles.retroarchCustom
            # Create retroarchcustom.cfg if does not exists
            if not os.path.isfile(rhgamestationFiles.retroarchCustom):
                shutil.copyfile(rhgamestationFiles.retroarchCustomOrigin, rhgamestationFiles.retroarchCustom)
            #  Write controllers configuration files
            libretroControllers.writeControllersConfig(system, playersControllers)
            # Write configuration to retroarchcustom.cfg
            libretroConfig.writeLibretroConfig(system, playersControllers)

        # Retroarch core on the filesystem
        retroarchCore = rhgamestationFiles.retroarchCores + system.config['core'] + rhgamestationFiles.libretroExt
        romName = os.path.basename(rom)

        # the command to run
        commandArray = [rhgamestationFiles.rhgamestationBins[system.config['emulator']], "-L", retroarchCore, "--config", system.config['configfile']]
        configToAppend = []
        
        # Custom configs - per core
        customCfg = "{}/{}.cfg".format(rhgamestationFiles.retroarchRoot, system.name)
        if os.path.isfile(customCfg):
            configToAppend.append(customCfg)
        
        # Custom configs - per game
        customGameCfg = "{}/{}/{}.cfg".format(rhgamestationFiles.retroarchRoot, system.name, romName)
        if os.path.isfile(customGameCfg):
            configToAppend.append(customGameCfg)
        
        # Overlay management
        overlayFile = "{}/{}/{}.cfg".format(rhgamestationFiles.OVERLAYS, system.name, romName)
        if os.path.isfile(overlayFile):
            configToAppend.append(overlayFile)
        
        # Generate the append
        if configToAppend:
            commandArray.extend(["--appendconfig", "|".join(configToAppend)])
            
         # Netplay mode
        if 'netplaymode' in system.config and system.config['netplaymode'] is not None and system.config['netplaymode'] in ('host', 'client'):
            if system.config['netplaymode'] == 'host':
                commandArray.append("--host")
		if system.config['hash']:
		    commandArray.extend(["--hash", system.config['hash']])
	    elif system.config['netplaymode'] == 'client':
                if system.config['netplay_ip'] is not None:
                    commandArray.extend(["--connect", system.config['netplay_ip']])
		else:
		    raise ValueError("You must specify n IP in client mode")
	    else:
		raise ValueError("Netplay mode should be host or client")
	    port = system.config.get('netplay_port', "55435")
	    commandArray.extend(["--port", port])
	    nick = system.config['netplay_nickname'] if system.config['netplay_nickname'] else "Anonymous"
	    commandArray.extend(["--nick", nick])

        # Optionnal arguments
        if 'args' in system.config and system.config['args'] is not None:
             commandArray.extend(system.config['args'])
             
        commandArray.append(rom)
        return Command.Command(videomode=system.config['videomode'], array=commandArray)
