import pygame as pyg


class Button:

    def __init__(self, display, width, height, x_pos, y_pos, text, font):

        self.__display = display
        self.__width = width
        self.__height = height
        self.__x_pos = x_pos
        self.__y_pos = y_pos

        self.__yellow = (255, 210, 0)
        self.__white = (255, 255, 255)
        self.__black = (0, 0, 0)
        self.__button = pyg.Rect(self.__x_pos, self.__y_pos, self.__width, self.__height)

        self.__text = text
        self.__font = font

    def display_button(self):
        """
        Places the given image at the given x and y coordinate
        """

        # Draws the button on the screen
        pyg.draw.rect(self.__display, self.__yellow, self.__button)

        # Adds shading to the button
        pyg.draw.line(self.__display, self.__white, (self.__x_pos, self.__y_pos), (self.__x_pos + self.__width, self.__y_pos), 2)
        pyg.draw.line(self.__display, self.__white, (self.__x_pos, self.__y_pos), (self.__x_pos, self.__y_pos + self.__height), 2)
        pyg.draw.line(self.__display, self.__black, (self.__x_pos, self.__y_pos + self.__height), (self.__x_pos + self.__width, self.__y_pos + self.__height), 2)
        pyg.draw.line(self.__display, self.__black, (self.__x_pos + self.__width, self.__y_pos), (self.__x_pos + self.__width, self.__y_pos + self.__height), 2)

        # Adds text to the button
        text = self.__font.render(self.__text, True, self.__white)
        self.__display.blit(text, (self.__x_pos + self.__width // 7, self.__y_pos + self.__height // 15))

    def get_button(self):
        """
        Returns the button to be used outside of the class
        """

        return self.__button


class PlayButton(Button):

    def __init__(self, display, width, height, x_pos, y_pos, text, font, play_menu):
        super().__init__(display, width, height, x_pos, y_pos, text, font)
        self.__play_menu = play_menu

    def go_to_play_menu(self):
        """
        Takes the player to the Play Menu which displays rules and further options
        """

        self.__play_menu.play_menu_loop()


class ExitButton(Button):

    def __init__(self, display, display_set_up, width, height, x_pos, y_pos, text, font):
        super().__init__(display, width, height, x_pos, y_pos, text, font)
        self.__display_set_up = display_set_up

    def exit(self):
        """
        Exits the program when the button is clicked
        """

        self.__display_set_up.exit()
