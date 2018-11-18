#!/usr/bin/env python

esInputs = '/rhgamestation/share/system/.emulationstation/es_input.cfg'
esSettings = '/rhgamestation/share/system/.emulationstation/es_settings.cfg'
rhgamestationConf = '/rhgamestation/share/system/rhgamestation.conf'

retroarchRoot = '/rhgamestation/share/system/configs/retroarch'
retroarchCustom = retroarchRoot + '/retroarchcustom.cfg'
retroarchCustomOrigin = retroarchRoot + "/retroarchcustom.cfg.origin"
retroarchCoreCustom = retroarchRoot + "/cores/retroarch-core-options.cfg"

retroarchBin = "retroarch"
retroarchCores = "/usr/lib/libretro/"
shadersRoot = "/rhgamestation/share_init/shaders/presets/"
shadersExt = '.gplsp'
libretroExt = '_libretro.so'

fbaRoot = '/rhgamestation/share/system/configs/fba/'
fbaCustom = fbaRoot + 'fba2x.cfg'
fbaCustomOrigin = fbaRoot + 'fba2x.cfg.origin'
fba2xBin = '/usr/bin/fba2x'

mupenCustom = "/rhgamestation/share/system/configs/mupen64/mupen64plus.cfg"

shaderPresetRoot = "/rhgamestation/share/system/configs/shadersets/"

kodiJoystick = '/rhgamestation/share/system/.kodi/userdata/keymaps/rhgamestation.xml'
kodiMapping  = '/rhgamestation/share/system/configs/kodi/input.xml'

kodiBin  = '/rhgamestation/scripts/kodilauncher.sh'

logdir = '/rhgamestation/share/system/logs/'
