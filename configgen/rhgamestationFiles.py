#!/usr/bin/env python
HOME_INIT = '/rhgamestation/share_init/system/'
HOME = '/rhgamestation/share/system'
CONF = HOME + '/configs'
SAVES = '/rhgamestation/share/saves'
SAVES_INIT = '/rhgamestation/share_init/saves'
SCREENSHOTS = '/rhgamestation/share/screenshots'
BIOS = '/rhgamestation/share/bios'
BIOS_INIT = '/rhgamestation/share_init/bios'
OVERLAYS = '/rhgamestation/share/overlays'
ROMS = '/rhgamestation/share/roms'

esInputs = HOME + '/.emulationstation/es_input.cfg'
esSettings = HOME + '/.emulationstation/es_settings.cfg'
rhgamestationConf = HOME + '/rhgamestation.conf'
logdir = HOME + '/logs/'

# This dict is indexed on the emulator name, not on the system
rhgamestationBins = {'dosbox'      : '/usr/bin/dosbox'
              , 'fba2x'       : '/usr/bin/fba2x'
              , 'kodi'        : '/rhgamestation/scripts/kodilauncher.sh'
              , 'libretro'    : '/usr/bin/retroarch'
              , 'linapple'    : '/usr/bin/linapple'
              , 'moonlight'   : '/usr/bin/moonlight'
              , 'mupen64plus' : '/usr/bin/mupen64plus'
              , 'ppsspp'      : '/usr/bin/PPSSPPSDL'
              , 'reicast'     : '/usr/bin/reicast.elf'
              , 'scummvm'     : '/usr/bin/scummvm'
              , 'residualvm'  : '/usr/bin/residualvm'
              , 'vice'        : '/usr/bin/x64'
              , 'dolphin'     : '/usr/bin/dolphin-emu'
              , 'advancemame' : '/usr/bin/advmame'
              , 'amiberry'    : '/usr/bin/amiberry'
              , 'daphne'      : '/usr/bin/hypseus'
}


retroarchRoot = CONF + '/retroarch'
retroarchCustom = retroarchRoot + '/retroarchcustom.cfg'
retroarchCustomOrigin = retroarchRoot + "/retroarchcustom.cfg.origin"
retroarchCoreCustom = retroarchRoot + "/cores/retroarch-core-options.cfg"
retroarchInitCustomOrigin = HOME_INIT + "configs/retroarch/retroarchcustom.cfg.origin"

retroarchCores = "/usr/lib/libretro/"
shadersRoot = "/rhgamestation/share/shaders/presets/"
shadersExt = '.gplsp'
libretroExt = '_libretro.so'
screenshotsDir = "/rhgamestation/share/screenshots/"
savesDir = "/rhgamestation/share/saves/"

fbaRoot = CONF + '/fba/'
fbaCustom = fbaRoot + 'fba2x.cfg'
fbaCustomOrigin = fbaRoot + 'fba2x.cfg.origin'


mupenConf = CONF + '/mupen64/'
mupenCustom = mupenConf + "mupen64plus.cfg"
mupenInput = mupenConf + "InputAutoCfg.ini"
mupenSaves = SAVES + "/n64"
mupenMappingUser    = mupenConf + 'input.xml'
mupenMappingSystem  = '/rhgamestation/share_init/system/configs/mupen64/input.xml'

shaderPresetRoot = "/rhgamestation/share_init/system/configs/shadersets/"

kodiJoystick = HOME + '/.kodi/userdata/keymaps/rhgamestation.xml'
kodiMappingUser    = CONF + '/kodi/input.xml'
kodiMappingSystem  = '/rhgamestation/share_init/system/configs/kodi/input.xml'


moonlightCustom = CONF+'/moonlight'
moonlightConfig = moonlightCustom + '/moonlight.conf'
moonlightGamelist = moonlightCustom + '/gamelist.txt'
moonlightMapping = dict()
moonlightMapping[1] = moonlightCustom + '/mappingP1.conf'
moonlightMapping[2] = moonlightCustom + '/mappingP2.conf'
moonlightMapping[3] = moonlightCustom + '/mappingP3.conf'
moonlightMapping[4] = moonlightCustom + '/mappingP4.conf'
moonlightMapping[5] = moonlightCustom + '/mappingP5.conf'

reicastCustom = CONF + '/reicast'
reicastConfig = reicastCustom + '/emu.cfg'
reicastConfigInit = HOME_INIT + 'configs/reicast/emu.cfg'
reicastSaves = SAVES + '/dreamcast'
reicastBios = BIOS

dolphinConfig = CONF + "/dolphin-emu"
dolphinData   = SAVES + "/dolphin-emu"
dolphinIni    = dolphinConfig + '/Dolphin.ini'
dolphinHKeys  = dolphinConfig + '/Hotkeys.ini'
dolphinGFX    = dolphinConfig + '/GFX.ini'

ppssppConf = CONF + '/ppsspp/PSP/SYSTEM'
ppssppControlsIni = ppssppConf + '/controls.ini'
ppssppControls = CONF + '/ppsspp/gamecontrollerdb.txt'
ppssppControlsInit = HOME_INIT + 'configs/ppsspp/PSP/SYSTEM/controls.ini'
ppssppConfig = ppssppConf + '/ppsspp.ini'

dosboxCustom = CONF + '/dosbox'
dosboxConfig = dosboxCustom + '/dosbox.conf'

scummvmSaves = SAVES + '/scummvm'
residualvmSaves = SAVES + '/scummvm'

viceConfig = CONF + "/vice/vice.conf"

advancemameConfig = CONF + '/advancemame/advmame.rc'
advancemameConfigOrigin = CONF + '/advancemame/advmame.rc.origin'

amiberryMountPoint = '/tmp/amiga'
amiberrySaves      = SAVES

daphneInputIni = CONF + '/daphne/dapinput.ini'
daphneHomedir = ROMS + '/daphne'
daphneDatadir = '/usr/share/daphne'
