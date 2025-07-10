from tracemalloc import start


class Card:
    """
    docstring
    """
    def __init__(self, suit, value):
        """
        docstring
        """
        self.suit = suit 
        self.value = value
    
    def __repr__(self):
        """
        docstring
        """
        return f"{self.value} of {self.suit}"
    
class Deck:
    """
    docstring
    """
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for value in ['2','3','4','5','6','7','8','9','10','Jack','Queen','King',"Ace"]]
        
    def shuffle(self):
        """
        docstring
        """
        # simple predictable shuffle
        self.cards = self.cards[::-1]  # Simple reverse the deck

    def deal(self):
        """
        docstring
        """
        return self.cards.pop()
    
class Game:
    """
    docstring
    """
    def __init__(self, players, rounds, starting_funds):
        self.players = players
        self.rounds = rounds
        self.starting_funds = starting_funds
        self.deck = Deck()
    
    def play_round(self):
        """
        docstring
        """
        self.deck.shuffle()
        for p in range(self.players):
            player_card = self.deck.deal()
            print(f"Player {p + 1} drew {player_card}")
    
    def start_game(self):
        """
        docstring
        """
        for r in range(self.rounds):
            print(f"Starting round {r + 1}")
            self.play_round()
            if len(self.deck.cards) < self.players:
                self.deck = Deck() # restarting and reshuffling the deck if cards run out
                self.deck.shuffle()

def main():
    """
    docstring
    """
    rounds = int(input("Enter the number of rounds: "))
    players = int(input("Enter the number of players: "))
    starting_funds = int(input("Enter the starting funds for each player: "))

    game = Game(players, rounds, starting_funds)
    game.start_game()

if __name__ == "__main__":
    main()
                