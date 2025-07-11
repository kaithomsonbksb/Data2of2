from tracemalloc import start


class Card:
    """
    Represents a playing card with a suit and value.
    """
    def __init__(self, suit, value):
        """
        Initializes a card with a given suit and value.
        """
        self.suit = suit 
        self.value = value
    
    def __repr__(self):
        """
        Returns a string representation of the card (e.g., "Ace of Spades").
        """
        return f"{self.value} of {self.suit}"
    
class Deck:
    """
    Represents a deck of 52 playing cards.
    """
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for value in ['2','3','4','5','6','7','8','9','10','Jack','Queen','King',"Ace"]]
        
    def shuffle(self):
        """
        Reverses the order of cards in the deck (simple shuffle).
        """
        # simple predictable shuffle
        self.cards = self.cards[::-1]  # Simple reverse the deck

    def deal(self):
        """
        Removes and returns the top card from the deck.
        """
        return self.cards.pop()
    
class Game:
    """
    Manages the card game logic, including players, rounds, and funds.
    """
    def __init__(self, players, rounds, starting_funds):
        self.players = players
        self.rounds = rounds
        self.starting_funds = starting_funds
        self.deck = Deck()
    
    def play_round(self):
        """
        Shuffles the deck and deals one card to each player, printing the result.
        """
        self.deck.shuffle()
        for p in range(self.players):
            player_card = self.deck.deal()
            print(f"Player {p + 1} drew {player_card}")
    
    def start_game(self):
        """
        Runs the game for the specified number of rounds, reshuffling if the deck runs out.
        """
        for r in range(self.rounds):
            print(f"Starting round {r + 1}")
            self.play_round()
            if len(self.deck.cards) < self.players:
                self.deck = Deck() # restarting and reshuffling the deck if cards run out
                self.deck.shuffle()

def main():
    """
    Handles user input and starts the game.
    """
    rounds = int(input("Enter the number of rounds: "))
    players = int(input("Enter the number of players: "))
    starting_funds = int(input("Enter the starting funds for each player: "))

    game = Game(players, rounds, starting_funds)
    game.start_game()

if __name__ == "__main__":
    main()
                

# Note: All docstrings in this file were generated using GitHub Copilot AI assistance.
