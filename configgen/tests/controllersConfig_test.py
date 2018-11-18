#!/usr/bin/env python

import os
import sys
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import configgen.controllersConfig as controllersConfig

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/es_input.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/es_input.cfg")))

# Injecting test es_input
controllersConfig.esInputs = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/es_input.cfg"))


class TestControllersConfig(unittest.TestCase):
    def test_load_all_controllers(self):
        controllers = controllersConfig.loadAllControllersConfig()
        self.assertEquals(33, len(controllers))

    def test_find_input_args(self):
        controllers = controllersConfig.loadAllControllersConfig()
        controller = controllers['060000004c0500006802000000010000PLAYSTATION(R)3 Controller (00:48:E8:D1:63:25)']
        self.assertEquals("button", controller.inputs["a"].type)
        self.assertEquals("axis", controller.inputs["joystick1up"].type)
        self.assertEquals("1", controller.inputs["a"].value)
        self.assertEquals("13", controller.inputs["a"].id)

    def test_associate_controllers_with_players_with_sameuuid(self):
        uuid = "060000004c0500006802000000010000"
        players = controllersConfig.loadControllerConfig("-1", uuid, "p1controller", "", "0", 
                                                        "-1", uuid, "p2controller", "", "0", 
                                                        "-1", uuid, "p3controller", "", "0", 
                                                        "-1", uuid, "p4controller", "","0", 
                                                        "-1", uuid, "p5controller", "","0")
        self.assertEquals(5, len(players))
        self.assertEquals(uuid, players["1"].guid)
        self.assertEquals(players["1"].realName, "p1controller")
        self.assertEquals(players["2"].realName, "p2controller")
        self.assertEquals(players["3"].realName, "p3controller")
        self.assertEquals(players["4"].realName, "p4controller")
        self.assertEquals(players["5"].realName, "p5controller")
        self.assertEquals(players["3"].configName, players["1"].configName)

    def test_associate_controllers_with_players_with_differentuuid(self):
        uuid1 = "060000004c0500006802000000010000"
        uuid2 = "030000005e0400009102000007010000"
        uuid3 = "030000005e0400008e02000014010000"
        uuid4 = "03000000b50700000399000000010000"
        uuid5 = "0000000058626f782047616d65706101"
        players = controllersConfig.loadControllerConfig("-1", uuid1, "p1controller", "", "0", 
                                                        "-1", uuid2, "p2controller", "", "0", 
                                                        "-1", uuid3, "p3controller", "", "0", 
                                                        "-1", uuid4, "p4controller", "","0", 
                                                        "-1", uuid5, "p5controller", "","0")
        self.assertEquals(5, len(players))
        self.assertEquals(uuid1, players["1"].guid)
        self.assertEquals(uuid2, players["2"].guid)
        self.assertEquals(uuid3, players["3"].guid)
        self.assertEquals(uuid4, players["4"].guid)
        self.assertEquals(uuid5, players["5"].guid)
        self.assertEquals("13", players["1"].inputs["a"].id)

    def test_controllers_defaults(self):
        uuid1 = "060000004c0500006802000000010000"
        players = controllersConfig.loadControllerConfig("0", uuid1, "p1controller", "","0",
                                                        "-1","FAKEUUID", "DEFAULTNAME", "", "0",
                                                        "-1","FAKEUUID", "DEFAULTNAME", "","0", 
                                                        "-1","FAKEUUID", "DEFAULTNAME", "","0",
                                                        "-1","FAKEUUID", "DEFAULTNAME", "","0")

        self.assertEquals(1, len(players))
        self.assertEquals("0", players["1"].index)


if __name__ == '__main__':
    unittest.main()
