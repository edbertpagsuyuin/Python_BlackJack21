#each card in the deck
class Card:
    def __init__(self, value, suit, face):
        self.value = value
        self.suit = suit
        self.face = face

    def __str__(self):
        return f"{self.face} of {self.suit} (value {self.value})"



