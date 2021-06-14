import pygame as pyg
from random import shuffle


class Deck:

    def __init__(self):

        self.__suits = ("clubs", "diamonds", "hearts", "spades")
        self.__ranks = (
            "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"
        )
        self.__values = {
            "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "jack": 11, "queen": 12, "king": 13, "ace": 14
        }

        self.__deck = []
        for suit in self.__suits:
            for rank in self.__ranks:
                value = self.__values.get(rank)
                self.__deck.append(Card(suit, rank, value))

    def shuffle_deck(self):
        """
        Shuffles the cards
        """

        shuffle(self.__deck)

    def deal(self):
        """
        Deals a single card
        """

        card = self.__deck.pop()
        return card

    def get_deck(self):
        """
        Returns the deck to be used outside of the class
        """

        return self.__deck

    def set_deck(self, cards):
        """
        Sets the deck to a new list of cards
        (Used for moving cards from the discard pile back to deck when no more cards in the deck)
        """

        self.__deck = cards


class Card:

    def __init__(self, suit, rank, value):

        self.__suit = suit
        self.__rank = rank
        self.__value = value
        self.__image = pyg.image.load(f"img\\cards\\{self.__rank} of {self.__suit}.png")
        self.__x = None
        self.__y = None

    def get_image(self):
        """
        Returns the image to be used outside of class
        """

        return self.__image

    def get_suit(self):
        """
        Returns the suit of the card
        """

        return self.__suit

    def get_rank(self):
        """
        Returns the rank of the card
        """

        return self.__rank

    def get_value(self):
        """
        Returns the value of the card
        """

        return self.__value

    def set_x(self, x):
        """
        Sets x to the passed x position
        """

        self.__x = x

    def get_x(self):
        """
        Returns the x position of the image
        """

        return self.__x

    def set_y(self, y):
        """
        Sets y to the passed y position
        """

        self.__y = y

    def get_y(self):
        """
        Returns the y position of the image
        """

        return self.__y


class Hand:

    def __init__(self, display):

        self.__cards_in_hand = []
        self.__display = display

    def add_card(self, card):
        """
        Adds a card to the hand
        """

        self.__cards_in_hand.append(card)

    def remove_card(self, card):
        """
        Removes a selected card from hand
        """

        return self.__cards_in_hand.pop(self.__cards_in_hand.index(card))

    def get_cards_in_hand(self):
        """
        Returns the cards in hand to be used outside of class
        """

        return self.__cards_in_hand

    def show_hand(self, x, y, is_player):
        """
        Displays the cards currently held in hand by the player and backs of cards held by the computer
        """

        gap_between_cards = 5

        if is_player:
            for card in self.__cards_in_hand:
                card_img = card.get_image()
                self.__display.blit(card_img, (x, y))
                card.set_x(x)
                card.set_y(y)
                x += card_img.get_width() + gap_between_cards
        else:
            for card in self.__cards_in_hand:
                card_img = pyg.image.load("img\\cards\\back.png")
                self.__display.blit(card_img, (x, y))
                x += card_img.get_width() + gap_between_cards

    def sort_hand(self, reverse):
        """
        Uses a modified insertion sort algorithm to sort cards by suit and rank
        """

        if reverse:
            for i in range(1, len(self.__cards_in_hand)):
                item_to_insert = self.__cards_in_hand[i]
                j = i - 1

                # Checks if the alphabetical value of a card suit is higher than another suit and if a card value is higher
                # than another value when the card suit is the same
                while j >= 0 and self.__cards_in_hand[j].get_suit() < item_to_insert.get_suit() or j >= 0 and self.__cards_in_hand[j].get_suit() == item_to_insert.get_suit() and self.__cards_in_hand[j].get_value() < item_to_insert.get_value():
                    self.__cards_in_hand[j + 1] = self.__cards_in_hand[j]
                    j -= 1

                self.__cards_in_hand[j + 1] = item_to_insert
        else:
            for i in range(1, len(self.__cards_in_hand)):
                item_to_insert = self.__cards_in_hand[i]
                j = i - 1

                # Checks if the alphabetical value of a card suit is higher than another suit and if a card value is higher
                # than another value when the card suit is the same
                while j >= 0 and self.__cards_in_hand[j].get_suit() > item_to_insert.get_suit() or j >= 0 and self.__cards_in_hand[j].get_suit() == item_to_insert.get_suit() and self.__cards_in_hand[j].get_value() > item_to_insert.get_value():
                    self.__cards_in_hand[j + 1] = self.__cards_in_hand[j]
                    j -= 1

                self.__cards_in_hand[j + 1] = item_to_insert


class DiscardPile:

    def __init__(self, display):

        self.__cards_in_discard_pile = []
        self.__top_card = None
        self.__display = display

    def add_card(self, card):
        """
        Adds a card to the discard pile and sets the top card to the last element
        """

        self.__cards_in_discard_pile.append(card)
        self.__top_card = self.__cards_in_discard_pile[-1]

    def show_top_card(self, x, y):
        """
        Displays the top card of the discard pile at the x, y coordinate
        """

        top_card_img = self.__top_card.get_image()
        self.__display.blit(top_card_img, (x, y))

    def get_cards_in_discard_pile(self):
        """
        Returns the list of cards currently in the discard pile to be used outside of the class
        """

        return self.__cards_in_discard_pile

    def set_top_card(self, card):
        """
        Sets the top card to the value of passed card
        """

        self.__top_card = card

    def get_top_card(self):
        """
        Returns the top card to be used outside of class
        """

        return self.__top_card
