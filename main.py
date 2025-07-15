import random
import customtkinter


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
        """
        Initializes a new deck of 52 cards.
        """
        self.cards = [
            Card(suit, value)
            for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]
            for value in [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Jack",
                "Queen",
                "King",
                "Ace",
            ]
        ]

    def shuffle(self):
        """
        Shuffles the deck using the Fisher-Yates algorithm for randomness.
        """
        # Using Fisher-Yates instead of reverse shuffle
        for idx in range(len(self.cards) - 1, 0, -1):
            rand_idx = random.randint(0, idx)
            self.cards[idx], self.cards[rand_idx] = (
                self.cards[rand_idx],
                self.cards[idx],
            )

    def deal(self):
        """
        Removes and returns the top card from the deck.
        """
        return self.cards.pop()


class Player:
    """
    Represents a player in the card game, with a name/id and score.
    """

    def __init__(self, player_id, starting_funds):
        self.player_id = player_id
        self.score = 0
        self.funds = starting_funds
        self.last_card = None

    def __repr__(self):
        return f"Player {self.player_id} (Score: {self.score})"


class Game:
    """
    Manages the card game logic, including players, rounds, and funds.
    """

    def __init__(self, num_players, rounds, starting_funds):
        self.rounds = rounds
        self.starting_funds = starting_funds
        self.deck = Deck()
        self.players = [Player(i + 1, starting_funds) for i in range(num_players)]

    def play_round(self):
        """
        Shuffles the deck, deals one card to each player, determines the winner, updates scores and funds.
        Returns a tuple: (round_results, winner, scores, funds)
        """
        self.deck.shuffle()
        round_results = []
        card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
        }
        highest_val = -1
        winner = None
        bet_amount = 10

        # Only players who can afford the bet participate
        active_players = [p for p in self.players if p.funds >= bet_amount]

        # Deduct bet
        for player in active_players:
            player.funds -= bet_amount

        # Deal cards only to active players
        for player in active_players:
            dealt_card = self.deck.deal()
            player.last_card = dealt_card
            val = card_values[dealt_card.value]
            round_results.append((player.player_id, dealt_card, val))
            if val > highest_val:
                highest_val = val
                winner = player

        # Calculate pot
        pot = bet_amount * len(active_players)

        # Award pot to winner
        if winner:
            winner.score += 1
            winner.funds += pot

        # Update players list to remove bankrupt players
        self.players = [p for p in self.players if p.funds > 0]

        # Prepare data for display
        scores = [(p.player_id, p.score) for p in self.players]
        funds = [(p.player_id, p.funds) for p in self.players]

        return round_results, winner, scores, funds

    def start_game(self):
        """
        Runs the game for the specified number of rounds, reshuffling if the deck runs out.
        """
        for r in range(self.rounds):
            print(f"Starting round {r + 1}")
            self.play_round()
            # If we have fewer cards left than players, reset the deck
            if len(self.deck.cards) < len(self.players):
                self.deck = Deck()
                self.deck.shuffle()


class App(customtkinter.CTk):
    """
    Basic GUI application for the card game using customtkinter.
    Allows user input for rounds, players, and starting funds, and displays game output.
    """

    def __init__(self):
        """
        Initializes the GUI window and widgets for user input and output display.
        """
        super().__init__()
        self.title("Card Game")
        self.geometry("400x400")

        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.pack(pady=25)

        self.label_rounds = customtkinter.CTkLabel(
            self.input_frame, text="Number of rounds:"
        )
        self.label_rounds.pack()
        self.entry_rounds = customtkinter.CTkEntry(self.input_frame)
        self.entry_rounds.pack(pady=3)

        self.label_players = customtkinter.CTkLabel(
            self.input_frame, text="Number of players:"
        )
        self.label_players.pack()
        self.entry_players = customtkinter.CTkEntry(self.input_frame)
        self.entry_players.pack(pady=3)

        self.label_funds = customtkinter.CTkLabel(
            self.input_frame, text="Starting funds:"
        )
        self.label_funds.pack()
        self.entry_funds = customtkinter.CTkEntry(self.input_frame)
        self.entry_funds.pack(pady=3)

        self.start_button = customtkinter.CTkButton(
            self.input_frame, text="Start Game", command=self.start_game
        )
        self.start_button.pack(pady=10)

        self.output_box = customtkinter.CTkTextbox(self, width=350, height=180)
        self.output_box.pack(pady=10)
        self.output_box.pack_forget()

    def start_game(self):
        """
        Reads user input, sets up the game, hides input widgets, and prepares for round-by-round dealing.
        """
        try:
            self.total_rounds = int(self.entry_rounds.get())
            self.total_players = int(self.entry_players.get())
            self.starting_funds = int(self.entry_funds.get())
        except ValueError:
            self.output_box.pack()
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", "Please enter valid numbers.\n")
            return

        self.input_frame.pack_forget()
        self.output_box.pack()
        self.output_box.delete("1.0", "end")
        self.current_round = 1
        self.game = Game(self.total_players, self.total_rounds, self.starting_funds)
        self.deal_button = customtkinter.CTkButton(
            self, text="Deal Round", command=self.deal_round
        )
        self.deal_button.pack(pady=10)
        self.output_box.insert(
            "end",
            f"Ready to start {self.total_rounds} rounds.\nClick 'Deal Round' to begin.\n",
        )

    def deal_round(self):
        """
        Handles the logic for dealing one round, with a delay between each player's card, tracks scores/funds and displays winner.
        """
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", f"Starting round {self.current_round}\n")
        result = self.game.play_round()
        self.round_results, self.round_winner, self.scores, self.funds = result
        self.player_index = 0
        self.show_next_player_card()

    def show_next_player_card(self):
        """
        Shows each player's card with a 1s delay, then displays the winner, scores, and funds.
        """
        if self.player_index < len(self.round_results):
            pid, card, val = self.round_results[self.player_index]
            self.output_box.insert("end", f"Player {pid} drew {card}\n")
            self.player_index += 1
            self.after(1000, self.show_next_player_card)
        else:
            if self.round_winner:
                self.output_box.insert(
                    "end",
                    f"\nWinner: Player {self.round_winner.player_id} ({self.round_winner.last_card})\n",
                )
            else:
                self.output_box.insert("end", "\nNo winner this round.\n")
            self.output_box.insert("end", "Scores and Funds:\n")
            for i in range(len(self.scores)):
                pid, score = self.scores[i]
                _, funds = self.funds[i]
                self.output_box.insert(
                    "end", f"Player {pid}: Score {score}, Funds: {funds}\n"
                )
            self.current_round += 1
            if len(self.game.players) == 0:
                self.deal_button.configure(state="disabled")
                self.output_box.insert(
                    "end", "\nGame over! All players are out of funds.\n"
                )
            elif len(self.game.deck.cards) < len(self.game.players):
                self.game.deck = Deck()
                self.game.deck.shuffle()
                if self.current_round <= self.total_rounds:
                    self.deal_button.configure(
                        state="normal", text=f"Deal Round {self.current_round}"
                    )
                    self.output_box.insert(
                        "end", "\nClick 'Deal Round' for the next round.\n"
                    )
                else:
                    self.deal_button.configure(state="disabled")
                    self.output_box.insert(
                        "end", "\nGame over! All rounds completed.\n"
                    )
            elif self.current_round <= self.total_rounds:
                self.deal_button.configure(
                    state="normal", text=f"Deal Round {self.current_round}"
                )
                self.output_box.insert(
                    "end", "\nClick 'Deal Round' for the next round.\n"
                )
            else:
                self.deal_button.configure(state="disabled")
                self.output_box.insert("end", "\nGame over! All rounds completed.\n")


def main():
    """
    Handles user input and starts the game.
    """
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

# Note: All docstrings in this file were generated using GitHub Copilot AI assistance.
