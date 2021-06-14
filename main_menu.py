import pygame as pyg
from button import PlayButton, ExitButton


class MainMenu:

    def __init__(self, display, main_clock, display_set_up, display_dimensions, bg, play_menu):

        self.__display = display
        self.__main_clock = main_clock
        self.__display_set_up = display_set_up
        self.__display_dimensions = display_dimensions
        self.__bg = bg

        # Loads in the logo image and creates dimensions for it
        self.__logo = pyg.image.load("img\\logo.png")
        self.__logo_x_pos = (self.__display_dimensions[0] // 2) - (self.__logo.get_width() // 2)
        self.__logo_y_pos = 20

        # Sets the button width to be 20% of the display width
        self.__button_width = int(self.__display_dimensions[0] * 0.2)
        # Sets the button height to be 15% of the display height
        self.__button_height = int(self.__display_dimensions[1] * 0.15)
        self.__font = pyg.font.Font("COMIC.TTF", 50)

        self.__play_menu = play_menu
        self.__play_button_x_pos = self.__display_dimensions[0] // 2 - self.__button_width - 25
        self.__play_button_y_pos = self.__display_dimensions[1] - 200
        self.__play_button_text = "PLAY"
        self.__play_button = PlayButton(self.__display, self.__button_width, self.__button_height, self.__play_button_x_pos, self.__play_button_y_pos, self.__play_button_text, self.__font, self.__play_menu)

        self.__exit_button_x_pos = self.__display_dimensions[0] // 2 + 25
        self.__exit_button_y_pos = self.__display_dimensions[1] - 200
        self.__exit_button_text = "EXIT"
        self.__exit_button = ExitButton(self.__display, self.__display_set_up, self.__button_width, self.__button_height, self.__exit_button_x_pos, self.__exit_button_y_pos, self.__exit_button_text, self.__font)

        self.__mouse_click = False

    def main_menu_loop(self):
        """
        Runs and displays the main menu
        """

        # The main menu main loop
        while True:

            self.__display.fill((0, 0, 0))

            # Scales the background image and displays it on the screen
            scaled_bg = pyg.transform.scale(self.__bg, self.__display_dimensions)
            self.__display.blit(scaled_bg, (0, 0))

            # Displays the logo on the screen
            self.__display.blit(self.__logo, (self.__logo_x_pos, self.__logo_y_pos))

            # Displays the play and exit button on to the screen
            self.__play_button.display_button()
            self.__exit_button.display_button()

            # Stores the position of the mouse
            mouse_pos = pyg.mouse.get_pos()

            # If the mouse is over the play button and the button is clicked, runs the play menu
            if self.__play_button.get_button().collidepoint((mouse_pos[0], mouse_pos[1])):
                if self.__mouse_click:
                    self.__play_button.go_to_play_menu()
            # If the mouse is over the exit button and the button is clicked exits the game
            if self.__exit_button.get_button().collidepoint((mouse_pos[0], mouse_pos[1])):
                if self.__mouse_click:
                    self.__exit_button.exit()

            # Resets the mouse click
            self.__mouse_click = False

            for event in pyg.event.get():
                # If the x button is clicked, exits the program
                if event.type == pyg.QUIT:
                    self.__display_set_up.exit()
                # If a key is pressed and that key is escape (ESC), exits the program
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        self.__display_set_up.exit()
                # If the left mouse button is clicked, sets the mouse click to true
                if event.type == pyg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__mouse_click = True

            # Updates the screen on every iteration
            pyg.display.update()
            # Sets the FPS
            self.__main_clock.tick(60)
