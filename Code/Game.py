import time

from pyglet import clock, gl
from pyglet.window import Window, NoSuchConfigException

from Code.Logic.GameState import GameState
from Code.Scenes.ManageScene import ManageScene
from Code.Scenes.WaveScene import WaveScene
from Code.Util.Saves import *

from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.SystemStuff import SystemStuff
from Code.Util.Camera import Camera
from Code.Util.Controller import Controller


class Game:
    def __init__(self):
        self.dt, self.time, self.tick = 0, 0, 0
        self.run = False

        self.showFps = SettingsGlobal.ShowFPS
        self.time0 = 0
        self.timeFrameStart = 0.0

        # Camera/window stuff
        x, y = 0, 0
        res_w, res_h = SettingsGlobal.Width, SettingsGlobal.Height
        w, h = SystemStuff.getDefaultScreenResolution()

        if SettingsGlobal.Fullscreen:
            SettingsGlobal.Scale = min(w // res_w,  h // res_h)
        else:
            SettingsGlobal.Scale = min(6*w//(res_w*8), 6*h//(res_h*8))
        width, height = res_w*SettingsGlobal.Scale, res_h*SettingsGlobal.Scale
        self.camera: Camera = Camera(x, y, width, height, SettingsGlobal.Scale)

        caption = SettingsGlobal.GameName

        if SettingsGlobal.Fullscreen:
            self.window = Window(fullscreen=SettingsGlobal.Fullscreen, caption=caption, config=self.getConfig())
        else:
            self.window = Window(width=width, height=height, caption=caption, config=self.getConfig())

        # Setup controller
        self.controller = Controller(self.window)

        # Game Data
        self.loadData()

        self.scenes = self.createScenes()
        self.scene = self.scenes["wave"]

    def start(self):
        self.run = True
        while self.run:
            self.dt = clock.tick()
            self.loop()

        self.end()

    def loop(self):
        self.updateFpsInfo()

        self.handleInput()
        if self.controller.isControlPressed(Controller.pause):
            return

        self.scene.update(self.dt)
        self.scene.draw()

        self.controller.updateReset()

    def updateFpsInfo(self):
        self.time += self.dt
        self.tick += 1

        # print("frame", self.tick, 1/self.dt, "FPS")

        if self.showFps and self.tick%10 == 0:
            dt = self.time - self.time0
            self.time0 = self.time
            if dt*6 > 1.1:
                x = "SLOW!!"
            else:
                x = ""
            print(dt*6, "FPS", x)

    def handleInput(self):
        self.dispatchEvents()
        self.controller.update(self.dt)

        if self.controller.isControlPressed(Controller.close):
            self.run = False
            return

        if self.controller.isControlPressed(Controller.pause):
            self.controller.updateReset()
            return

    def switchScene(self, name):
        self.scene = self.scenes[name]
        self.scene.onSceneSwitch()

    def createScenes(self):
        return {"wave": WaveScene(self), "manage": ManageScene(self)}

    def end(self):
        pass

    def close(self):
        self.window.close()

    def dispatchEvents(self):
        return self.window.dispatch_events()

    def clear(self):
        self.window.clear()

    def flip(self):
        self.window.flip()

    def onNewGame(self):
        pass
        # self.inventory = loadSave("", Inventory)

    def saveData(self):
        # save(self.inventory, "inventory")
        pass

    def loadData(self):
        self.gameState = GameState()
        # self.inventory = loadSave("inventory", Inventory)

    def resetSave(self):
        pass

    def getConfig(self):
        template = gl.Config(sample_buffers=1, samples=4)
        try:
            config = SystemStuff.getBestConfig(template)
        except NoSuchConfigException:
            template = gl.Config()
            config = SystemStuff.getBestConfig(template)
        return config

    def tickClock(self):
        """Alternative clock ticker"""
        if self.timeFrameStart == 0.0:
            self.dt = 1/60
            self.timeFrameStart = time.perf_counter()
            return

        target = self.timeFrameStart + 1/60
        while time.perf_counter() < target and False:
            _ = 5
            _ += 5
        curTime = time.perf_counter()

        self.dt = curTime - self.timeFrameStart
        # print(1/self.dt)
        self.timeFrameStart = curTime
