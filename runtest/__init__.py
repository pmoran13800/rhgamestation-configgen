'''
Created on Mar 6, 2016

@author: Laurent Marchelli
'''
import os
#import sys

# Define working directories
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
dir_res = os.path.join(dir_root, 'tests/resources')
dir_tmp = os.path.join(dir_root , 'tests/tmp')
# if dir_root not in sys.path:
#     sys.path.append(dir_root)

# Override configuration directories
import configgen.rhgamestationFiles as rhgamestationFiles
rhgamestationFiles.HOME = dir_tmp
rhgamestationFiles.HOME_INIT = dir_res
rhgamestationFiles.esInputs = os.path.join(dir_res, 'es_input.cfg')
rhgamestationFiles.esSettings = os.path.join(dir_res, 'es_settings.cfg')
rhgamestationFiles.rhgamestationConf = os.path.join(dir_res, 'rhgamestation.conf')
rhgamestationFiles.savesDir = os.path.join(dir_tmp, 'saves')

from .fixture import FixtureJoystick, fixture_joystick
from .case import TestCase, RedirectStdStreams
from .loader import TestLoader, main
