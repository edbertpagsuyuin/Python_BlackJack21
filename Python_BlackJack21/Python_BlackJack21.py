import time
import colorama
from colorama import Fore, Style, init
import os
clear = lambda: os.system('cls')

init(autoreset=True)

from Deck import Deck
from Player import Player

# Game class to handle the game logic
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.dealer = Player("Dealer", Fore.WHITE)
        self.colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX,
            Fore.LIGHTYELLOW_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX,
            Fore.GREEN]

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
            valid = False
            while not valid:
                player_name = input(f"Enter name for player {i+1}: ").strip()

                if not player_name or (isinstance(player_name, str) and player_name.startswith("Computer")):
                   readline = input("Invalid input. Name can't be Null or starts with Computer\nPress any key to continue...")
                   print()
                else:
                    self.players.append(Player(player_name, self.colors[i]))
                    valid = True

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
        print("\nPreparing Game!")
        self.deck.shuffle_deck()
        print("Distributing cards...", end = "")
        self.distribute_cards()
        time.sleep(2)
        print("Done distributing")

        print("\n----- Initial Hands -----")
        for player in self.players:
            player.show_hand()
        self.dealer.show_hand(False)

        input("\nPress any key to start the Game!")
        
        
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
