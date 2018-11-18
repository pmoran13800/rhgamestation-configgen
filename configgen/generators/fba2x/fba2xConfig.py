#!/usr/bin/env python
import sys
import os
import rhgamestationFiles
from settings.unixSettings import UnixSettings

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


fbaSettings = UnixSettings(rhgamestationFiles.fbaCustom)

# return true if the option is considered enabled (for boolean options)
def enabled(key, dict):
    return key in dict and (dict[key] == '1' or dict[key] == 'true')


# return true if the option is considered defined
def defined(key, dict):
    return key in dict and isinstance(dict[key], str) and len(dict[key]) > 0


ratioIndexes = {'16/9': '0', '4/3': '1'}


def writeFBAConfig(system):
    writeFBAConfigToFile(createFBAConfig(system))


# take a system, and returns a dict of retroarch.cfg compatible parameters
def createFBAConfig(system):
    fbaConfig = dict()
    rhgamestationConfig = system.config
    if enabled('smooth', rhgamestationConfig):
        fbaConfig['DisplaySmoothStretch'] = '1'
    else:
        fbaConfig['DisplaySmoothStretch'] = '0'

    if defined('ratio', rhgamestationConfig) and rhgamestationConfig['ratio'] in ratioIndexes:
        fbaConfig['MaintainAspectRatio'] = ratioIndexes[rhgamestationConfig['ratio']]
    else:
        fbaConfig['MaintainAspectRatio'] = '1'

    if defined('shaders', rhgamestationConfig) and rhgamestationConfig['shaders'] == 'scanlines':
        fbaConfig['DisplayEffect'] = '1'
    else :
        fbaConfig['DisplayEffect'] = '0'

    return fbaConfig


def writeFBAConfigToFile(config):
    for setting in config:
        fbaSettings.save(setting, config[setting])
