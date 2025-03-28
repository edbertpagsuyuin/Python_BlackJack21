import colorama
from colorama import Fore, Style, init
import os
clear = lambda: os.system('cls')

#represent each player/computer
class Player:
    def __init__(self, name, color=Style.RESET_ALL):
        self.name = name
        self.hand = []
        self.stand = False
        self.color = color

    def add_card(self, card):
        self.hand.append(card)

    def hand_value(self):
        value = 0
        aces = []
        for card in self.hand:
            value += card.value
            if card.face == 'A':
                aces.append(card)

        for ace in aces:
            if value + 10 <= 21:
                value += 10
                ace.value = 11
            elif ace.value == 11 and value > 21:
                value -= 10
                ace.value = 1
                
        return value

    def show_hand(self, show=True):
        if not show:
            print(f"{self.color}{self.name}'s Hand: \n??? of ??? (value ???)\n{self.hand[1]}")
        else:
            print(f"{self.color}{self.name}'s Hand:")
            self.hand_value() #to check for aces
            for card in self.hand:
                print(f"{self.color}{card}")
            print(f"{self.color}Total value: {self.hand_value()}\n")



