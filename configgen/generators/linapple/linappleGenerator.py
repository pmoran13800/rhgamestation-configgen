'''
Created on Mar 6, 2016

@author: Laurent Marchelli
'''

import os
import shutil
import Command
from generators.Generator import Generator
from generators.linapple.linappleConfig import LinappleConfig
import rhgamestationFiles

class LinappleGenerator(Generator):
    '''
    Command line generator for linapple-pie emulator
    
    Ensure the user's configuration directory has all needed files to run
    linapple emulator and manage configuration file to tune emulator behaviour 
    with current hardware configuration.
    
    Args:
        path_init (str):
            Full path name where default settings are stored.
            ('/rhgamestation/share_init/system/.linapple')
        
        path_user (str):
            Full path name where user settings are stored.
            ('/rhgamestation/share/system/.linapple')
            
    '''
    def __init__(self, path_init, path_user):
        self.path_init = path_init
        self.path_user = path_user
        self.resources = ['Master.dsk']
        self.filename = 'linapple.conf'

    def check_resources(self):
        '''
        Check system needed resources
        
        Returns (bool:
            Returns True if the check suceeded, False otherwise.
        '''
        # Create user setting path, if it does not exists
        if not os.path.exists(self.path_user):
            os.makedirs(self.path_user)

        # Ensure system configuration file is available
        sys_conf = os.path.join(self.path_init, self.filename)
        if not os.path.exists(sys_conf):
            return False

        # Ensure system resources are available
        for r in self.resources:
            sys_filename = os.path.join(self.path_init, r)
            if not os.path.exists(sys_filename):
                return False
            usr_filename = os.path.join(self.path_user, r)
            if not os.path.exists(usr_filename):
                shutil.copyfile(sys_filename, usr_filename)

        return True

    def generate(self, system, rom, playersControllers):
        '''
        Configure linapple inputs and return the command line to run.
        
        Args:
            system (Emulator):
                Emulator object containing a config dictionay with all
                parameters set in EmulationStation.
            rom (str) :
                Path and filename of the rom to run.
            playerControllers (dict):
                Dictionary of controllers connected (1 to 5). 
            
        Returns (configgen.Command, None) :
            Returns Command object containing needed parameter to launch the 
            emulator or None if an error occured.
        '''
        # Check resources
        if not self.check_resources(): 
            return

        if not system.config['configfile']:
            # Load config file
            usr_conf = os.path.join(self.path_user, self.filename)
            filename = usr_conf \
                if os.path.exists(usr_conf) \
                else os.path.join(self.path_init, self.filename)
            config = LinappleConfig(filename=filename)
            # Adjust configuration 
            config.joysticks(playersControllers)
            config.system(system, rom)
            # Save changes 
            config.save(filename=usr_conf)

        commandArray = [ rhgamestationFiles.rhgamestationBins[system.config['emulator']] ]
        if 'args' in system.config and system.config['args'] is not None:
            commandArray.extend(system.config['args'])

        return Command.Command(videomode=system.config['videomode'], array=commandArray)

    def config_upgrade(self, version):
        '''
        Upgrade the user's configuration file with new values added to the
        system configuration file upgraded by S11Share:do_upgrade()
        
        Args: 
            version (str): New RHGamestation version
            
        Returns (bool):
            Returns True if this Generators sucessfully handled the upgrade.
        '''
        # Check resources
        if not self.check_resources(): 
            return False

        # Load system configuration file
        config = LinappleConfig(filename=os.path.join(
                    self.path_init, self.filename))

        # If an user's configuration file exists, upgrade it
        usr_conf = os.path.join(self.path_user, self.filename)
        if os.path.exists(usr_conf):
            config_sys = config
            config = LinappleConfig(filename=usr_conf)
            for k,v in config_sys.settings.items():
                if k not in config.settings:
                    config.settings[k]=v

        # Save config file (original/updated) to user's directory
        config.save(filename=usr_conf)
        print("{} 's configuration successfully upgraded".format(self.__class__.__name__))
        return True

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
