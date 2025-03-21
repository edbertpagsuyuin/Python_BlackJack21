import random
import time
from traceback import print_tb
from colorama import Fore, Style, init
import os
clear = lambda: os.system('cls')
clear()

init(autoreset=True)

#each card in the deck
class Card:
    def __init__(self, value, suit, face):
        self.value = value
        self.suit = suit
        self.face = face

    def __str__(self):
        return f"{self.face} of {self.suit} (value {self.value})"

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

# Game class to handle the game logic
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.dealer = Player("Dealer", Fore.WHITE)
        self.colors = [
            Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX,
            Fore.LIGHTYELLOW_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX,
            Fore.GREEN
        ]

    def setup_players(self):
        while True:
            playersnum = int(input("Enter number of players (0 to 7): "))
            compsnum = 0

            if playersnum < 7:
                compsnum = int(input(f"Enter number of computer (0 to {7 - playersnum}): "))

            if 0 <= playersnum <= 7 and 0 <= compsnum <= 7 and (playersnum + compsnum) <= 7 and (playersnum + compsnum) > 0:
                break
            else:
                readline = input("Invalid input. The total number of players/computer must be between 1 and 7.\nPress any key to continue...")
                clear()

        for i in range(playersnum):
            player_name = input(f"Enter name for player {i+1}: ")
            self.players.append(Player(player_name, self.colors[i]))

        for i in range(compsnum):
            self.players.append(Player(f"Computer {i+1}", self.colors[playersnum + i]))

    def distribute_cards(self):
        for player in self.players:
            player.add_card(self.deck.draw())
            player.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())

    def player_turn(self, player):
        print(f"\n----- {player.name}'s turn -----")
        
        if player.hand_value() == 21:
            print(f"{player.color}{player.name} Blackjack!")
            print()
            print("----- Final Hand -----")
            player.show_hand()
                
        while not player.stand and player.hand_value() < 21:
            if player.name.startswith("Computer"):
                print()
                player.show_hand()
                if player.hand_value() < 17:
                    print(f"{player.color}{player.name} hits.")
                    player.add_card(self.deck.draw())
                    if player.hand_value() > 21:
                        print(f"{player.color}{player.name} busts!")
                        player.stand = True
                else:
                    print(f"{player.color}{player.name} stands.")
                    player.stand = True
             
            else:
                print()
                player.show_hand()
                choice = input(f"{player.color}{player.name}, Hit or Stand? (H/S): ").upper()
                if choice == 'H':
                    player.add_card(self.deck.draw())
                    if player.hand_value() > 21:
                        print(f"{player.color}{player.name} busts!")
                        player.stand = True
                elif choice == 'S':
                    player.stand = True
                else:
                    readline = input("Invalid input. Press any key to continue...")
                    
            if player.stand:
                print()
                print("----- Final Hand -----")
                player.show_hand()
                
            if player.hand_value() == 21:
                print(f"{player.color}{player.name} Blackjack!")
                print()
                print("----- Final Hand -----")
                player.show_hand()

    def dealer_turn(self):
        print(f"\n----- {self.dealer.color}Dealer's turn -----")
        if self.dealer.hand_value() >= 17:
            self.dealer.show_hand()
            
        while self.dealer.hand_value() < 17:
            self.dealer.show_hand()
            print(f"{self.dealer.color}Dealer hits.")
            self.dealer.add_card(self.deck.draw())
     
        if self.dealer.hand_value() == 21:
            print(f"{self.dealer.color}Dealer Blackjack!")
        elif self.dealer.hand_value() > 21:
            print(f"{self.dealer.color}Dealer busts!")
        else:
            print(f"{self.dealer.color}Dealer stands.\n")

        print()
        print("----- Final Hand -----")
        self.dealer.show_hand()

    def show_results(self):
        
        dealer_value = self.dealer.hand_value()
        print("----- Results -----\n")
        self.dealer.show_hand()

        for player in self.players:
            player.show_hand()
            if player.hand_value() > 21:
                print(f"{player.color}{player.name} busts! Dealer wins.")
            elif dealer_value > 21:
                print(f"{player.color}Dealer busts! {player.name} wins!")
            elif player.hand_value() == dealer_value:
                print(f"{player.color}{player.name} and Dealer draw.")
            elif player.hand_value() == 21:
                print(f"{player.color}Blackjack! {player.name} wins!")
            elif dealer_value == 21:
                print(f"{player.color}Blackjack! Dealer wins against {player.name}.!")
            elif player.hand_value() > dealer_value:
                print(f"{player.color}{player.name} wins!")
            else:
                print(f"{player.color}Dealer wins against {player.name}.")
            print()

    def play_game(self):
        self.setup_players()
        print("\nGame Start!")
        self.deck.shuffle_deck()
        print("Distributing cards...", end = "")
        self.distribute_cards()
        time.sleep(2)
        print("Done distributing")

        print("\n----- Initial Hands -----")
        for player in self.players:
            player.show_hand()
        self.dealer.show_hand(False)

        for player in self.players:
            print()
            self.player_turn(player)
        
        self.dealer_turn()
        
        readline = input("All players and the dealer have finished their turns.\nPress any key to show the results...")
        clear()
        self.show_results()

if __name__ == "__main__":
    game = BlackjackGame()
    game.play_game()
