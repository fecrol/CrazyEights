import pygame as pyg
from button import Button


class PlayMenu:

    def __init__(self, display_set_up, display, display_dimensions, main_clock, bg, game_menu):

        self.__running = True
        self.__display_set_up = display_set_up
        self.__display = display
        self.__display_dimensions = display_dimensions
        self.__main_clock = main_clock
        self.__bg = bg
        self.__how_to_image = pyg.image.load("img\\how_to_play.png")

        # Sets the button width to be 20% of the display width
        self.__button_width = int(self.__display_dimensions[0] * 0.4)
        # Sets the button height to be 15% of the display height
        self.__button_height = int(self.__display_dimensions[1] * 0.15)

        self.__vs_btn_x = self.__display_dimensions[0] // 2 + 55
        self.__vs_one_btn_y = 45

        self.__font = pyg.font.Font("COMIC.TTF", 50)
        self.__vs_one_btn_text = "Play Game"
        self.__vs_one_button = Button(self.__display, self.__button_width, self.__button_height, self.__vs_btn_x,
            self.__vs_one_btn_y, self.__vs_one_btn_text, self.__font)

        self.__back_btn_y = self.__button_height + 90
        self.__back_btn_text = "Main Menu"
        self.__back_button = Button(self.__display, self.__button_width, self.__button_height, self.__vs_btn_x,
            self.__back_btn_y, self.__back_btn_text, self.__font)

        self.__mouse_click = False

        self.__game_menu = game_menu

    def play_menu_loop(self):
        """
        Runs and displays the play menu
        """

        # Sets the running variable to true everytime the function is called
        self.__running = True

        while self.__running:

            self.__display.fill((0, 0, 0))

            # Scales the background image and places it on the screen
            scaled_bg = pyg.transform.scale(self.__bg, self.__display_dimensions)
            self.__display.blit(scaled_bg, (0, 0))

            # Displays the how to play image on the screen
            self.__display.blit(self.__how_to_image, (0, 0))

            # Displays the button to the screen
            self.__vs_one_button.display_button()
            self.__back_button.display_button()

            # Stores the position of the mouse
            mouse_pos = pyg.mouse.get_pos()

            if self.__vs_one_button.get_button().collidepoint((mouse_pos[0], mouse_pos[1])):
                if self.__mouse_click:
                    self.__game_menu.game_menu_loop()
            if self.__back_button.get_button().collidepoint((mouse_pos[0], mouse_pos[1])):
                if self.__mouse_click:
                    self.__running = False

            # Resets the mouse click
            self.__mouse_click = False

            for event in pyg.event.get():
                # If the x button is clicked, exits the program
                if event.type == pyg.QUIT:
                    self.__display_set_up.exit()
                # If a key is pressed and that key is escape (ESC), exits the program
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        self.__running = False
                # If the left mouse button is clicked, sets the mouse click to true
                if event.type == pyg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__mouse_click = True

            # Updates the screen on every iteration
            pyg.display.update()
            # Sets the FPS
            self.__main_clock.tick(60)
