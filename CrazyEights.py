from display import DisplaySetUp
from game_menu import GameMenu
from play_menu import PlayMenu
from main_menu import MainMenu


display_set_up = DisplaySetUp()
display = display_set_up.get_display()
main_clock = display_set_up.get_main_clock()
display_dimensions = display_set_up.get_display_dimensions()
background_image = display_set_up.get_background_image()

game_menu = GameMenu(display, display_dimensions, display_set_up, main_clock, background_image)

play_menu = PlayMenu(display_set_up, display, display_dimensions, main_clock, background_image, game_menu)

main_menu = MainMenu(display, main_clock, display_set_up, display_dimensions, background_image, play_menu)
main_menu.main_menu_loop()
