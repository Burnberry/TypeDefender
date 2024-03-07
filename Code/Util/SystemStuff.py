from pyglet import canvas


class SystemStuff:
    @staticmethod
    def getDefaultScreenResolution():
        """
        :return: width, height
        """
        display = canvas.Display()
        screen = display.get_default_screen()
        return screen.width, screen.height

    @staticmethod
    def getBestConfig(template):
        """
        :return: config
        """
        return canvas.Display().get_default_screen().get_best_config(template)
