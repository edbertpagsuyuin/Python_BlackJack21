import time
import random
from Card import Card

#creates and shuffles the deck
class Deck:
    def __init__(self):
        self.suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
        self.faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = []
        for suit in self.suits:
            for i, face in enumerate(self.faces):
                value = i + 1
                if value > 10:
                    value = 10
                self.cards.append(Card(value, suit, face))
                
    def draw(self):
        return self.cards.pop()
    
    def shuffle_deck(self):
        print("Shuffling the deck...", end = "")
        random.shuffle(self.cards)
        time.sleep(2)
        print("Done Shuffling")



