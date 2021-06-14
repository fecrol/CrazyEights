import pygame as pyg
from deck import Deck, Hand, DiscardPile
from button import Button


class GameMenu:

    def __init__(self, display, display_dimensions, display_set_up, main_clock, bg):

        self.__running = True
        self.__mouse_click = False

        self.__display = display
        self.__display_dimensions = display_dimensions
        self.__display_set_up = display_set_up
        self.__main_clock = main_clock
        self.__bg = bg

        self.__deck_img = pyg.image.load("img\\cards\\back.png")
        self.__deck_x_pos = (self.__display_dimensions[0] // 2) + 5
        self.__deck_y_pos = (self.__display_dimensions[1] // 2) - (self.__deck_img.get_height() // 2)

        self.__discard_pile_x = (self.__display_dimensions[0] // 2) - (self.__deck_img.get_width() + 5)
        self.__discard_pile_y = (self.__display_dimensions[1] // 2) - (self.__deck_img.get_height() // 2)

        self.__icons = {
            "clubs": pyg.image.load("img\\clubs.png"),
            "diamonds": pyg.image.load("img\\diamonds.png"),
            "hearts": pyg.image.load("img\\hearts.png"),
            "spades": pyg.image.load("img\\spades.png")
        }

        self.__icon_x_pos = self.__discard_pile_x + self.__icons.get("clubs").get_width() - 5
        self.__icon_y_pos = self.__discard_pile_y - self.__icons.get("clubs").get_height() - 15

        self.__sort_button_width = 80
        self.__sort_button_height = 30
        self.__sort_button_x_pos = (self.__display_dimensions[0] // 2) - (self.__sort_button_width // 2)
        self.__sort_button_y_pos = self.__display_dimensions[1] - self.__sort_button_height - 20
        self.__sort_button_text = "SORT"
        self.__sort_font = pyg.font.Font("COMIC.TTF", 20)
        self.__sort_button = Button(self.__display, self.__sort_button_width, self.__sort_button_height, self.__sort_button_x_pos, self.__sort_button_y_pos, self.__sort_button_text, self.__sort_font)

        self.__new_button_width = 80
        self.__new_button_height = 30
        self.__new_button_x_pos = 15
        self.__new_button_y_pos = 15
        self.__new_button_text = "NEW"
        self.__new_font = pyg.font.Font("COMIC.TTF", 20)
        self.__new_button = Button(self.__display, self.__new_button_width, self.__new_button_height, self.__new_button_x_pos, self.__new_button_y_pos, self.__new_button_text, self.__new_font)

        self.__exit_button_width = 80
        self.__exit_button_height = 30
        self.__exit_button_x_pos = 15
        self.__exit_button_y_pos = 65
        self.__exit_button_text = "EXIT"
        self.__exit_font = pyg.font.Font("COMIC.TTF", 20)
        self.__exit_button = Button(self.__display, self.__exit_button_width, self.__exit_button_height, self.__exit_button_x_pos, self.__exit_button_y_pos, self.__exit_button_text, self.__exit_font)

        self.__change_suit_box_width = (self.__icons.get("clubs").get_width() * 4) + (13 * 2)
        self.__change_suit_box_height = self.__icons.get("clubs").get_height() + 30
        self.__change_suit_box_x_pos = (self.__display_dimensions[0] // 2) - (self.__change_suit_box_width // 2)
        self.__change_suit_box_y_pos = 360
        self.__yellow = (255, 210, 0)
        self.__white = (255, 255, 255)
        self.__change_suit_box_text = "Choose a Suit"
        self.__change_suit_font = pyg.font.Font("COMIC.TTF", 15)
        self.__change_suit_box = pyg.Rect(self.__change_suit_box_x_pos, self.__change_suit_box_y_pos, self.__change_suit_box_width, self.__change_suit_box_height)

        self.__win_text_x_pos = 0
        self.__win_text_y_pos = 0
        self.__win_text_font = pyg.font.Font("COMIC.TTF", 40)
        self.__player_win_text = "YOU WIN!"
        self.__computer_win_text = "COMPUTER WINS!"

        self.__icons_x_pos = {
            "clubs": self.__change_suit_box_x_pos + 5,
            "diamonds": self.__change_suit_box_x_pos + self.__icons.get("diamonds").get_width() + 10,
            "hearts": self.__change_suit_box_x_pos + (self.__icons.get("hearts").get_width() * 2) + 15,
            "spades": self.__change_suit_box_x_pos + (self.__icons.get("spades").get_width() * 3) + 20,
        }
        self.__change_suit_icon_y = self.__change_suit_box_y_pos + 25

        self.__player_turn = True
        self.__computer_turn = False
        self.__draw_card = False
        self.__current_suit = None
        self.__eight_is_selected = False
        self.__selected_card = None
        self.__game_over = False
        self.__player_win = False
        self.__computer_win = False

    def game_menu_loop(self):
        """
        Runs and displays the game menu
        """

        self.__running = True
        self.__game_over = False
        self.__player_win = False
        self.__computer_win = False
        self.__player_turn = True
        self.__computer_turn = False

        # Creates a deck, discard pile and player hand
        deck = Deck()
        discard_pile = DiscardPile(self.__display)
        player_hand = Hand(self.__display)
        computer_hand = Hand(self.__display)

        # Shuffles the cards
        deck.shuffle_deck()

        # Adds 7 cards to the player hand and computer hand
        for num in range(7):
            player_hand.add_card(deck.deal())
            computer_hand.add_card(deck.deal())

        # Sorts the computer hand in descending order of rank so computer always gets rid of higher rank cards first
        computer_hand.sort_hand(reverse=True)

        discard_pile.add_card(deck.deal())

        self.__current_suit = discard_pile.get_top_card().get_suit()

        while self.__running:

            self.__display.fill((0, 0, 0))

            # Scales the background image and places it on the screen
            scaled_bg = pyg.transform.scale(self.__bg, self.__display_dimensions)
            self.__display.blit(scaled_bg, (0, 0))

            # Displays the deck of cards on the screen
            self.__display.blit(self.__deck_img, (self.__deck_x_pos, self.__deck_y_pos))

            # Automatically moves cards in to the right position along the x-axis based on the width between cards,
            # the gap between cards and the number of cards currently in hand
            player_cards_x = (self.__display_dimensions[0] // 2) - ((70 + 5) * len(player_hand.get_cards_in_hand()) / 2)
            player_cards_y = self.__display_dimensions[1] // 2 + 125
            player_hand.show_hand(player_cards_x, player_cards_y, is_player=True)

            # Automatically moves cards in to the right position along the x-axis based on the width between cards,
            # the gap between cards and the number of cards currently in hand
            computer_cards_x = (self.__display_dimensions[0] // 2) - ((70 + 5) * len(computer_hand.get_cards_in_hand()) / 2)
            computer_cards_y = 65
            computer_hand.show_hand(computer_cards_x, computer_cards_y, is_player=False)

            discard_pile.show_top_card(self.__discard_pile_x, self.__discard_pile_y)

            self.__display_current_suit_icon()

            self.__new_button.display_button()

            self.__exit_button.display_button()

            self.__sort_button.display_button()

            if self.__eight_is_selected:
                self.__display_change_suit_box()

            # If the game is over displays a win or lose message depending on whether the player or computer won
            if self.__game_over:
                if self.__player_win:
                    self.__display_win_text(self.__player_win_text)
                if self.__computer_win:
                    self.__display_win_text(self.__computer_win_text)

            # Stores the position of the mouse
            mouse_pos = pyg.mouse.get_pos()

            if not self.__game_over:
                # Loops through the cards in the players hand
                for card in player_hand.get_cards_in_hand():
                    # Checks if it is the player turn
                    if self.__player_turn:
                        card_img = card.get_image()
                        card_rect_x = card.get_x() + (card_img.get_width() / 2)
                        card_rect_y = card.get_y() + (card_img.get_height() / 2)
                        if card_img.get_rect(center=(card_rect_x, card_rect_y)).collidepoint((mouse_pos[0], mouse_pos[1])) and not self.__eight_is_selected:
                            if self.__mouse_click:
                                self.__player_card_play(discard_pile, card, player_hand)
                        if self.__eight_is_selected:
                            self.__player_eight_play(mouse_pos, player_hand, discard_pile)

                self.__check_for_win(player_hand, computer_hand)

                self.__reshuffle_deck(deck, discard_pile)

                # Loops through the cards in the players hand and checks if a playable card is present. If not,
                # allows the player to draw a single card
                for card in player_hand.get_cards_in_hand():
                    if self.__player_turn:
                        top_card = discard_pile.get_top_card()
                        top_card_rank = top_card.get_rank()

                        card_suit = card.get_suit()
                        card_rank = card.get_rank()
                        if card_rank == "eight" or card_suit == self.__current_suit or card_rank == top_card_rank:
                            self.__draw_card = False
                            break
                        else:
                            self.__draw_card = True

            # If player cannot play any card, player can draw a card
            if self.__player_turn and self.__draw_card:
                deck_rect_x = self.__deck_x_pos + (self.__deck_img.get_width() / 2)
                deck_rect_y = self.__deck_y_pos + (self.__deck_img.get_height() / 2)
                if self.__deck_img.get_rect(center=(deck_rect_x, deck_rect_y)).collidepoint((mouse_pos[0], mouse_pos[1])):
                    if self.__mouse_click:
                        self.__card_draw(deck, player_hand, discard_pile, False)
                        self.__draw_card = False
                        if not self.__eight_is_selected:
                            self.__player_turn = False
                            self.__computer_turn = True

            # Allows computer to play a turn and sets player turn to true to allow player to play a card or draw a card
            # if the game is not over
            if not self.__game_over:
                self.__reshuffle_deck(deck, discard_pile)
                self.__computer_card_play(discard_pile, computer_hand, deck)
                self.__check_for_win(player_hand, computer_hand)
                self.__player_turn = True

            # Resets the mouse click
            self.__mouse_click = False

            for event in pyg.event.get():
                # If the exit button is clicked, exits the program
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

            if self.__new_button.get_button().collidepoint((mouse_pos[0], mouse_pos[1])):
                if self.__mouse_click:
                    self.__eight_is_selected = False
                    self.__selected_card = None
                    self.__running = False
                    self.game_menu_loop()
            if self.__sort_button.get_button().collidepoint((mouse_pos[0], mouse_pos[1])):
                if self.__mouse_click:
                    player_hand.sort_hand(reverse=False)
            if self.__exit_button.get_button().collidepoint((mouse_pos[0], mouse_pos[1])):
                if self.__mouse_click:
                    self.__eight_is_selected = False
                    self.__selected_card = None
                    self.__running = False

            # Updates the screen on every iteration
            pyg.display.update()
            # Sets the FPS
            self.__main_clock.tick(60)

    def __player_card_play(self, discard_pile, card, hand):
        """
        Allows for the play of a playable card
        """

        top_card = discard_pile.get_top_card()
        top_card_rank = top_card.get_rank()

        # Stores the current suit and rank of the card in computer hand
        card_suit = card.get_suit()
        card_rank = card.get_rank()

        # Checks if the card is an 8
        if card_rank == "eight":
            self.__eight_is_selected = True
            self.__selected_card = card
        else:
            # Checks if the cards suit or rank equals that of the discard pile card
            if card_suit == self.__current_suit or card_rank == top_card_rank:
                self.__add_card_to_discard_pile(hand, card, discard_pile)

                # Sets player turn to false to stop player from playing extra cards
                self.__player_turn = False
                # Sets computer turn to true to allow computer to play a card
                self.__computer_turn = True

    def __player_eight_play(self, mouse_pos, hand, discard_pile):
        """
        Allows the player to change the current suit when they play an 8
        """

        for icon in self.__icons:
            icon_x_pos = self.__icons_x_pos.get(icon) + (self.__icons.get(icon).get_width() / 2)
            icon_y_pos = self.__change_suit_icon_y + (self.__icons.get("clubs").get_height() / 2)
            if self.__icons.get(icon).get_rect(center=(icon_x_pos, icon_y_pos)).collidepoint(mouse_pos[0], mouse_pos[1]):
                if self.__mouse_click:
                    card_to_remove = hand.remove_card(self.__selected_card)
                    discard_pile.set_top_card(card_to_remove)
                    discard_pile.add_card(card_to_remove)

                    self.__current_suit = icon
                    self.__selected_card = None
                    self.__eight_is_selected = False
                    self.__player_turn = False
                    self.__computer_turn = True

    def __computer_card_play(self, discard_pile, hand, deck):
        """
        Allows the computer to play a card based what the computer has available. The computer will try to get rid
        of suits first, then ranks, then eights and if it can't play any card it will draw
        """

        top_card_rank = discard_pile.get_top_card().get_rank()

        for card in hand.get_cards_in_hand():
            if self.__computer_turn:
                if card.get_suit() == self.__current_suit and card.get_rank() != "eight":
                    self.__add_card_to_discard_pile(hand, card, discard_pile)
                    self.__computer_turn = False

        for card in hand.get_cards_in_hand():
            if self.__computer_turn:
                if card.get_rank() == top_card_rank and card.get_rank() != "eight":
                    self.__add_card_to_discard_pile(hand, card, discard_pile)
                    self.__computer_turn = False

        for card in hand.get_cards_in_hand():
            if self.__computer_turn:
                self.__computer_eight_play(hand, card, discard_pile)

        if self.__computer_turn:
            self.__card_draw(deck, hand, discard_pile, True)
            self.__computer_turn = False

    def __computer_eight_play(self, hand, card, discard_pile):
        """
        Allows the computer to change the current_suit when computer plays an 8
        """

        suit_count_indexes = {
            0: "clubs",
            1: "diamonds",
            2: "hearts",
            3: "spades"
        }

        if card.get_rank() == "eight":
            card_to_remove = hand.remove_card(card)

            suit_counts = [
                len([card for card in hand.get_cards_in_hand() if card.get_suit() == "clubs"]),
                len([card for card in hand.get_cards_in_hand() if card.get_suit() == "diamonds"]),
                len([card for card in hand.get_cards_in_hand() if card.get_suit() == "hearts"]),
                len([card for card in hand.get_cards_in_hand() if card.get_suit() == "spades"])
            ]

            suit = suit_count_indexes.get(suit_counts.index(max(suit_counts)))
            discard_pile.set_top_card(card_to_remove)
            discard_pile.add_card(card_to_remove)
            self.__current_suit = suit
            self.__computer_turn = False

    def __card_draw(self, deck, hand, discard_pile, is_computer):
        """
        Draws a card into the hand. If the card is playable, plays it automatically
        """

        card = deck.deal()
        hand.add_card(card)

        top_card = discard_pile.get_top_card()
        top_card_rank = top_card.get_rank()

        if card.get_rank() == "eight":
            if not is_computer:
                self.__eight_is_selected = True
                self.__selected_card = card
            else:
                self.__computer_eight_play(hand, card, discard_pile)
        else:
            if card.get_suit() == self.__current_suit or card.get_rank() == top_card_rank:
                card = hand.remove_card(card)
                discard_pile.add_card(card)
                self.__current_suit = discard_pile.get_top_card().get_suit()

        if is_computer:
            hand.sort_hand(reverse=True)

    def __add_card_to_discard_pile(self, hand, card, discard_pile):
        """
        Removes a card from hand and adds it to the discard pile
        """

        card_to_remove = hand.remove_card(card)
        discard_pile.set_top_card(card_to_remove)
        discard_pile.add_card(card_to_remove)
        self.__current_suit = discard_pile.get_top_card().get_suit()

    def __check_for_win(self, player_hand, computer_hand):
        """
        Checks if player or computer discarded all their cards. If so, ends the game
        """

        if len(player_hand.get_cards_in_hand()) == 0:
            self.__draw_card = False
            self.__player_turn = False
            self.__computer_turn = False
            self.__game_over = True
            self.__player_win = True

        if len(computer_hand.get_cards_in_hand()) == 0:
            self.__draw_card = False
            self.__player_turn = False
            self.__computer_turn = False
            self.__game_over = True
            self.__computer_win = True

    @staticmethod
    def __reshuffle_deck(deck, discard_pile):
        """
        When there is no more cards in the deck, moves all the cards aside from the last played card from the
        discard pile back into the deck and shuffles the deck
        """

        if len(deck.get_deck()) == 0:
            cards = discard_pile.get_cards_in_discard_pile()[:-1]
            deck.set_deck(cards)
            deck.shuffle_deck()

    def __display_current_suit_icon(self):
        """
        Displays the icon of the suit of the current top card in the discard pile
        """

        self.__display.blit(self.__icons.get(self.__current_suit), (self.__icon_x_pos, self.__icon_y_pos))

    def __display_change_suit_box(self):
        """
        Displays a box which allows player to change the current suit when player plays an 8
        """

        pyg.draw.rect(self.__display, self.__yellow, self.__change_suit_box)

        text = self.__change_suit_font.render(self.__change_suit_box_text, True, self.__white)
        self.__display.blit(text, (self.__change_suit_box_x_pos + 27, self.__change_suit_box_y_pos))

        for icon in self.__icons:
            self.__display.blit(self.__icons.get(icon), (self.__icons_x_pos.get(icon), self.__change_suit_icon_y))

    def __display_win_text(self, win_text):
        """
        Displays who won the game
        """

        text = self.__win_text_font.render(win_text, True, self.__white)
        self.__win_text_x_pos = (self.__display_dimensions[0] // 2) - (text.get_width() // 2)
        self.__display.blit(text, (self.__win_text_x_pos, self.__win_text_y_pos))
