#!/usr/bin/env python
import os
import sys
import rhgamestationFiles
import re
import time
from settings.unixSettings import UnixSettings
from utils.recallog import recallog
import subprocess
import json

# Set a specific video mode
def setVideoMode(videoMode, delay=0.5):
    # The user mentionned default for the videomode
    # video mode can be default, a "CEA 4 HDMI" like, a hdmi_cvt pattern or even a hdmi_timings pattern
    # Anything else should result in a crash
    if videoMode == "default":
        return
    videoMode = videoMode.strip()
    if videoMode == "auto":
        videoSetting = autoMode()
        # autoMode can have replied "default"
        if videoSetting == "default":
            return
        cmd = createVideoModeLine(videoSetting)
    elif "auto" in videoMode:
	realSetting = videoMode.split(' ', 1)[1]
	videoSetting = autoMode(realSetting)
        # autoMode can have replied "default"
        if videoSetting == "default":
            return
        cmd = createVideoModeLine(videoSetting)
    else:
        cmd = createVideoModeLine(videoMode)

    if cmd:
        os.system(cmd)
        time.sleep(delay)
    else:
        recallog("Error: Could not find a suitable video mode")
        sys.exit(1)

def createVideoModeLine(videoMode):
    # pattern (CEA|DMT) [0-9]{1,2} HDMI
    if re.match("^(CEA|DMT) [0-9]{1,2}( HDMI)?$", videoMode):
        return "tvservice -e '{}'".format(videoMode)
    if re.match("^hdmi_cvt [\d\s]{10,20}$", videoMode):
        return "vcgencmd {} && tvservice -e 'DMT 87'".format(videoMode)
    if re.match("^hdmi_timings [\d\s]{48,58}$", videoMode):
        return "vcgencmd {} && tvservice -e 'DMT 87'".format(videoMode)
    recallog("{} is not a valid video mode, abort".format(videoMode))
    return ''

# Set a specific video mode
def isSupported(group="CEA", mode='', drive="HDMI"):
    groups = ['CEA', 'DMT']
    if group not in groups:
        recallog("Error: {} is an unknown group. Can't switch to {} {} {}".format(group, group, mode, drive))
        sys.exit(1)

    drives = ['HDMI', 'DVI']
    if drive not in drives:
        recallog("Error: {} is an unknown drive. Can't switch to {} {} {}".format(drive, group, mode, drive))
        sys.exit(1)
        
    proc = subprocess.Popen(["tvservice -j -m {}".format(group)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    #print "program output:", out
    tvmodes = json.loads(out)

    for tvmode in tvmodes:
	print "Testing {} vs {}".format(tvmode["code"], int(mode))
        if tvmode["code"] == int(mode):
            return True

    recallog("The resolution for '{} {} {}' is not supported by your monitor".format(group, mode, drive))
    return False

# Switch to prefered mode
def setPreffered():
    recalSettings = UnixSettings(rhgamestationFiles.rhgamestationConf)
    esVideoMode = recalSettings.load('system.es.videomode')
    # Scary bug in tvservice : setting preferred mode on composite makes CEA 1 DVI !
    # See https://github.com/raspberrypi/firmware/issues/901
    # Once this issue is solved, just tvservice -p
    if esVideoMode is None or esVideoMode == "auto":
        os.system("tvservice -p")
    else:
        setVideoMode(esVideoMode)

# Check auto mode, return the expected value
def autoMode(expectedMode=None):
    #Resolutions to handle :
    #state 0x40001 [NTSC 4:3], 720x480 @ 60.00Hz, interlaced
    #state 0x12000a [HDMI CEA (16) RGB lim 16:9], 1920x1080 @ 60.00Hz, progressive
    #state 0x400000 [LCD], 800x480 @ 0.00Hz, progressive
    #state 0x400000 [LCD], 320x240 @ 0.00Hz, progressive
    #state 0x120006 [DVI DMT (58) RGB full 16:10], 1680x1050 @ 60.00Hz, progressive

    proc = subprocess.Popen(["tvservice -s"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    # This one does match what i need ! Everything ! Passes the 5 cases listed above
    regex = r".*\[([A-Z]{3,4}) ?(.*[^0-9:]?) ?([0-9]{1,2})?:?([0-9]{1,2})?\], ([0-9]{3,4})x([0-9]{3,4}) @ ([0-9.]{1,6})Hz, (progressive|interlaced).*"

    matches = re.match(regex, out)
    if not matches: 
        # We should log the out var and log that it doesn't match any known pattern
        recallog('auto mode -> had to set default')
        return "default"
    drive, details, wRatio, hRatio, width, height, refreshRate, progressiveOrInterlace = matches.groups()

    # Now the magic
    # if the screen supports CEA 4, and its current format is at least 16:9, go for CEA 4
    if drive not in ["HDMI", "DVI"]:
	recallog("{} is not among HDMI/DVI, fallback to default".format(drive))
	return "default"
    if expectedMode is not None:
	try:
	    autoGroup, autoMode, autoDrive = expectedMode.split( )
	except:
	    recallog("{} is not a valid format".format(expectedMode))
	    raise
    else:
	autoGroup, autoMode, autoDrive = ['CEA', 4, drive]
    if isSupported(autoGroup, autoMode, autoDrive):
        recallog("auto mode -> {} {} {} is valid".format(autoGroup, autoMode, autoDrive))
        return "{} {} {}".format(autoGroup, autoMode, autoDrive)
    # Otherwise (composite output, 5:4 screens, mini DPI screens etc ...) -> default
    else :
        recallog("auto mode -> CEA 4 HDMI/DVI not supported, fallback to default")
        return "default"

# Return the current resolution
def getCurrentResulution():
    # This is really dirty, I must admit ...
    # Call tvservice -s
    proc = subprocess.Popen(["tvservice -s"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    #print "program output:", out
    # If it's a calid json : we're not on pi, so we have the current resolution
    try:
	tvmodes = json.loads(out)
	return tvmodes[0]["width"], tvmodes[0]["height"]
    except ValueError, e:
	regex = r".*\[([A-Z]{3,4}) ?(.*[^0-9:]?) ?([0-9]{1,2})?:?([0-9]{1,2})?\], ([0-9]{3,4})x([0-9]{3,4}) @ ([0-9.]{1,6})Hz, (progressive|interlaced).*"

	matches = re.match(regex, out)
	if not matches: 
	    # We should log the out var and log that it doesn't match any known pattern
	    recallog('auto mode -> had to set default')
	    return "0", "0"
	    drive, details, wRatio, hRatio, width, height, refreshRate, progressiveOrInterlace = matches.groups()
	    return width, height
    # else we're on pi, use parse another way the output
