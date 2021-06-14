import pygame as pyg
import sys


class DisplaySetUp:

    def __init__(self):
        self.__background_img = pyg.image.load("img\\background.png")

        # Used to set the FPS
        self.__main_clock = pyg.time.Clock()

        # Initialises PyGame
        pyg.init()

        self.__display_dimensions = (800, 600)
        self.__display = pyg.display.set_mode(self.__display_dimensions)

        self.__icon = pyg.image.load("img\\logo.png")
        pyg.display.set_icon(self.__icon)

        # Sets the window title
        pyg.display.set_caption("Crazy Eights")

    @staticmethod
    def exit():
        """
        Exit function to exit the program
        """

        pyg.quit()
        sys.exit()

    def get_main_clock(self):
        """
        Returns the main clock to be used outside of the class
        """

        return self.__main_clock

    def get_display(self):
        """
        Returns the display to be used outside of the class
        """

        return self.__display

    def set_display(self, display):
        """
        For modifying the display outside of class
        """

        self.__display = display

    def get_display_dimensions(self):
        """
        Returns the display dimensions to be used outside of the class
        """

        return self.__display_dimensions

    def get_background_image(self):
        """
        Returns the background image to be used outside of the class
        """

        return self.__background_img
