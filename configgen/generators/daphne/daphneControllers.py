#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rhgamestationFiles
import ConfigParser

keyboard_keys = {
    "KEY_UP":         "273 114",
    "KEY_DOWN":       "274 102",
    "KEY_LEFT":       "276 100",
    "KEY_RIGHT":      "275 103",
    "KEY_BUTTON1":    "306 97",
    "KEY_BUTTON2":    "308 115",
    "KEY_BUTTON3":    "32 113",
    "KEY_START1":     "49 0",
    "KEY_START2":     "50 0",
    "KEY_COIN1":      "53 0",
    "KEY_COIN2":      "54 0",
    "KEY_SKILL1":     "304 119",
    "KEY_SKILL2":     "122 105",
    "KEY_SKILL3":     "120 107",
    "KEY_SERVICE":    "57 0",
    "KEY_TEST":       "283 0",
    "KEY_RESET":      "284 0",
    "KEY_SCREENSHOT": "293 0",
    "KEY_QUIT":       "27 113"
}
joystick_keys = {
    "KEY_UP":         "up",
    "KEY_DOWN":       "down",
    "KEY_LEFT":       "left",
    "KEY_RIGHT":      "right",
    "KEY_BUTTON1":    "b",
    "KEY_BUTTON2":    "a",
    "KEY_BUTTON3":    "y",
    "KEY_START1":     "start",
    "KEY_START2":     None,
    "KEY_COIN1":      "select",
    "KEY_COIN2":      None,
    "KEY_SKILL1":     None,
    "KEY_SKILL2":     None,
    "KEY_SKILL3":     None,
    "KEY_SERVICE":    None,
    "KEY_TEST":       None,
    "KEY_RESET":      None,
    "KEY_SCREENSHOT": None,
    "KEY_QUIT":       "hotkey"
}
joystick_axis = {
    "KEY_UP":         ["joystick1up","up"],
    "KEY_DOWN":       ["-joystick1up","down"],
    "KEY_LEFT":       ["joystick1left","left"],
    "KEY_RIGHT":      ["-joystick1left","right"],
    "KEY_BUTTON1":    None,
    "KEY_BUTTON2":    None,
    "KEY_BUTTON3":    None,
    "KEY_START1":     None,
    "KEY_START2":     None,
    "KEY_COIN1":      None,
    "KEY_COIN2":      None,
    "KEY_SKILL1":     None,
    "KEY_SKILL2":     None,
    "KEY_SKILL3":     None,
    "KEY_SERVICE":    None,
    "KEY_TEST":       None,
    "KEY_RESET":      None,
    "KEY_SCREENSHOT": None,
    "KEY_QUIT":       None
}

# Create the controller configuration file
def generateControllerConfig(system, controllers):
    Config = ConfigParser.ConfigParser()
    # To prevent ConfigParser from converting to lower case
    Config.optionxform = str

# Format is KEY=keyboard1 keyboard2 joystick_btn joystick_axis
# keyboard1 and keyboard2 are hardcoded values (see above)
# joystick_btn is computed from controller configuration: hundreds=joystick index, units=button index (+1)
# joystick_axis too: hundreds=joystick index, units=axis index (+1), sign=direction
    section = 'KEYBOARD'
    Config.add_section(section)

    for index in controllers:
        controller = controllers[index]
        # we only care about player 1
        if controller.player != "1":
            continue

        # dirty hack: if quit is same button than another key, force pagedown instead
        input_quit = controller.inputs[joystick_keys["KEY_QUIT"]]
        for propertyName, propertyValue in joystick_keys.iteritems():
            if propertyName != "KEY_QUIT" and propertyValue is not None:
                input = controller.inputs[propertyValue]
                if input.type == input_quit.type and input.id == input_quit.id:
                    joystick_keys["KEY_QUIT"] = "pagedown"
                    break

        for propertyName, keyboardValue in keyboard_keys.iteritems():
            # Map buttons
            joystickButtonValue = 0
            if joystick_keys[propertyName] is not None:
                joystickButtonName = joystick_keys[propertyName]
                if joystickButtonName in controller.inputs:
                    input = controller.inputs[joystickButtonName]
                    if input.type == 'button':
                        joystickButtonValue = (int(index)-1)*100 + int(input.id) + 1

            # Map axis
            joystickAxisValue = 0
            if joystick_axis[propertyName] is not None:
                joystickAxisNames = joystick_axis[propertyName]
                for joystickAxisName in joystickAxisNames:
                    axis_dir = 1
                    if joystickAxisName.startswith("-"):
                       axis_dir = -1
                       joystickAxisName = joystickAxisName[1:]
                    if joystickAxisName in controller.inputs:
                        input = controller.inputs[joystickAxisName]
                        if input.type == 'axis':
                            joystickAxisValue = ((int(index)-1)*100 + int(input.id) + 1) * int(input.value) * axis_dir
                            break

            Config.set(section, propertyName, keyboardValue+" "+str(joystickButtonValue)+" "+str(joystickAxisValue))

    cfgFile = open(rhgamestationFiles.daphneInputIni, "w")
    Config.write(cfgFile)
    cfgFile.close()
