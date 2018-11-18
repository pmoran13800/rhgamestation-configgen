#!/usr/bin/env python

import sys
import os.path
import unittest
import shutil
import configgen.controllersConfig as controllersConfig
import configgen.settings.unixSettings as unixSettings
import rhgamestationFiles

from configgen.Emulator import Emulator
from configgen.generators.libretro.libretroGenerator import LibretroGenerator

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import configgen.generators.libretro.libretroConfig as libretroConfig
import configgen.generators.libretro.libretroGenerator as libretroGenerator

RETROARCH_ORIGIN_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustomorigin.cfg'))
RETROARCH_CUSTOM_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustom.cfg'))
RHGAMESTATION_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/rhgamestation.conf'))
RETROARCH_CORE_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcorecustom.cfg"))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_CUSTOM_CFG_FILE)
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_ORIGIN_CFG_FILE)
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/rhgamestation.conf.origin')), \
                RHGAMESTATION_CFG_FILE)
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcores.cfg")), \
                RETROARCH_CORE_CONFIG)

# Injecting test files
libretroGenerator.rhgamestationFiles.retroarchCustom = RETROARCH_CUSTOM_CFG_FILE
libretroGenerator.rhgamestationFiles.retroarchCustomOrigin = RETROARCH_ORIGIN_CFG_FILE
libretroConfig.coreSettings = unixSettings.UnixSettings(RETROARCH_CORE_CONFIG, separator=' ')

libretroConfig.libretroSettings = unixSettings.UnixSettings(RETROARCH_CUSTOM_CFG_FILE, separator=' ')

PS3UUID = "060000004c0500006802000000010000"

rom = "MyRom.nes"

libretroGen = LibretroGenerator()


class TestLibretroGenerator(unittest.TestCase):
    def setUp(self):
        self.snes = Emulator(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2',
                             rewind='false', emulator='libretro')
        self.snes2 = Emulator(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2',
                              rewind='false', emulator='libretro')
        self.nes = Emulator(name='nes', videomode='6', core='catsfc', shaders='', ratio='16/9', smooth='1',
                            rewind='false', configfile='/myconfigfile.cfg', emulator='libretro')

        # test inputs
        self.basicInputs1 = {'hotkey': controllersConfig.Input("hotkey", "button", "10", "1","")}
        self.basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", 1, 0, "Joypad1RealName",
                                                             self.basicInputs1)

        self.sdl2controler = controllersConfig.Controller("contr1", "joypad", "030000003512000012ab000010010000", 2, 1,
                                                          "Bluetooth Wireless Controller   ", self.basicInputs1)
        self.controllers = dict()
        self.controllers['1'] = self.basicController1

        self.sdl2controllers = dict()
        self.sdl2controllers['1'] = self.basicController1
        self.sdl2controllers['2'] = self.sdl2controler

    def test_generate_system_no_custom_settings(self):
        command = libretroGen.generate(self.snes, rom, dict())
        self.assertEquals(command.videomode, '4')
        self.assertEquals(command.array,
                          [rhgamestationFiles.rhgamestationBins["libretro"], '-L', '/usr/lib/libretro/pocketsnes_libretro.so', '--config',
                           RETROARCH_CUSTOM_CFG_FILE, 'MyRom.nes'])

    def test_generate_system_custom_settings(self):
        command = libretroGen.generate(self.nes, rom, dict())
        self.assertEquals(command.videomode, '6')
        self.assertEquals(command.array,
                          [rhgamestationFiles.rhgamestationBins["libretro"], '-L', '/usr/lib/libretro/catsfc_libretro.so', '--config', '/myconfigfile.cfg',
                           'MyRom.nes'])

    def test_generate_forced_input_config(self):
        command = libretroGen.generate(self.nes, rom, dict())
        self.assertEquals(command.videomode, '6')
        self.assertEquals(command.array,
                          [rhgamestationFiles.rhgamestationBins["libretro"], '-L', '/usr/lib/libretro/catsfc_libretro.so', '--config', '/myconfigfile.cfg',
                           'MyRom.nes'])

    def test_custom_inputdriver_override_choice(self):
        self.snes.config['inputdriver'] = 'sdl2'
        command = libretroGen.generate(self.snes, rom, self.controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_joypad_driver'), 'sdl2')

    def test_standard_inputdriver(self):
        command = libretroGen.generate(self.snes, rom, self.controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_joypad_driver'), 'udev')

    def test_inputdriver_none_specified(self):
        command = libretroGen.generate(self.snes, rom, self.sdl2controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_joypad_driver'), 'sdl2')

    def test_inputdriver_auto(self):
        self.snes.config['inputdriver'] = 'auto'
        command = libretroGen.generate(self.snes, rom, self.sdl2controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_joypad_driver'), 'sdl2')

    def test_remove_hotkeys_on_configure_with_es_menu_none(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller","","0",
                                                                -1, 0, "p2controller","","0", 
                                                                -1, 0, "p3controller","","0", 
                                                                -1, 0, "p4controller","","0", 
                                                                -1, 0, "p5controller","","0")

        command = libretroGen.generate(self.snes, rom, controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_menu_toggle_btn'), '14')
        self.snes2.config['specials'] = "none"
        command = libretroGen.generate(self.snes2, rom, controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_menu_toggle_btn'), None)


if __name__ == '__main__':
    unittest.main()
