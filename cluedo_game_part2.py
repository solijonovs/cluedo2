"""
Cluedo / Clue - Project 2 Part 2
Author: King Solijonov

This is a text-based Python implementation of Cluedo with:
- Mansion layout
- Characters, weapons, and rooms
- Random murder solution
- Card deck and card dealing
- Player movement
- Suggestions
- Refutations by other players
- Deduction notebook
- Accusation mechanism
- Win/loss logic

Run:
    python3 cluedo_game_part2.py
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


Card = str
Suggestion = Tuple[str, str, str]


@dataclass
class Player:
    """Represents a human or computer-controlled player."""
    name: str
    character: str
    current_room: str
    hand: List[Card] = field(default_factory=list)
    active: bool = True
    is_human: bool = False


class Mansion:
    """Represents the mansion rooms and valid movement paths."""

    def __init__(self) -> None:
        self.rooms: Dict[str, List[str]] = {
            "Kitchen": ["Ballroom", "Dining Room"],
            "Ballroom": ["Kitchen", "Conservatory", "Hall"],
            "Conservatory": ["Ballroom", "Library"],
            "Dining Room": ["Kitchen", "Lounge"],
            "Lounge": ["Dining Room", "Hall"],
            "Hall": ["Lounge", "Ballroom", "Study"],
            "Study": ["Hall", "Library"],
            "Library": ["Study", "Conservatory", "Billiard Room"],
            "Billiard Room": ["Library"],
        }

    def get_rooms(self) -> List[str]:
        return list(self.rooms.keys())

    def get_connected_rooms(self, room: str) -> List[str]:
        return self.rooms.get(room, [])

    def can_move(self, current_room: str, next_room: str) -> bool:
        return next_room in self.get_connected_rooms(current_room)


class DeductionNotebook:
    """
    Tracks information the human player learns.
    This helps support reasoning and deduction throughout the game.
    """

    def __init__(self, all_cards: List[Card]) -> None:
        self.possible_cards = set(all_cards)
        self.seen_cards = set()
        self.suggestion_history: List[Dict[str, str]] = []

    def mark_seen(self, card: Card) -> None:
        self.seen_cards.add(card)

    def add_suggestion_record(
        self,
        suggester: str,
        character: str,
        weapon: str,
        room: str,
        refuter: Optional[str],
        shown_card: Optional[str],
    ) -> None:
        self.suggestion_history.append(
            {
                "suggester": suggester,
                "character": character,
                "weapon": weapon,
                "room": room,
                "refuter": refuter if refuter else "No one",
                "shown_card": shown_card if shown_card else "Unknown/None",
            }
        )

        if shown_card:
            self.mark_seen(shown_card)

    def get_unknown_cards(self) -> List[Card]:
        return sorted(self.possible_cards - self.seen_cards)

    def display(self) -> None:
        print("\n" + "=" * 60)
        print("DEDUCTION NOTEBOOK")
        print("=" * 60)

        print("\nCards you have seen:")
        if self.seen_cards:
            for card in sorted(self.seen_cards):
                print(f"- {card}")
        else:
            print("- None yet")

        print("\nCards still unknown:")
        for card in self.get_unknown_cards():
            print(f"- {card}")

        print("\nSuggestion / Refutation History:")
        if not self.suggestion_history:
            print("- No suggestions recorded yet.")
        else:
            for index, record in enumerate(self.suggestion_history, start=1):
                print(
                    f"{index}. {record['suggester']} suggested "
                    f"{record['character']} with the {record['weapon']} "
                    f"in the {record['room']} | Refuted by: {record['refuter']} "
                    f"| Card shown: {record['shown_card']}"
                )


class CluedoGame:
    """Main game controller."""

    def __init__(self) -> None:
        self.mansion = Mansion()

        self.characters = [
            "Miss Scarlett",
            "Colonel Mustard",
            "Mrs. White",
            "Mr. Green",
            "Mrs. Peacock",
            "Professor Plum",
        ]

        self.starting_positions = {
            "Miss Scarlett": "Lounge",
            "Colonel Mustard": "Dining Room",
            "Mrs. White": "Kitchen",
            "Mr. Green": "Conservatory",
            "Mrs. Peacock": "Library",
            "Professor Plum": "Study",
        }

        self.weapons = [
            "Candlestick",
            "Revolver",
            "Rope",
            "Lead Pipe",
            "Knife",
            "Wrench",
        ]

        self.rooms = self.mansion.get_rooms()

        self.solution: Suggestion = self.select_solution()

        self.players: List[Player] = []
        self.current_player_index = 0
        self.human_player: Optional[Player] = None

        self.all_cards = self.characters + self.weapons + self.rooms
        self.notebook = DeductionNotebook(self.all_cards)

        self.game_over = False

    def select_solution(self) -> Suggestion:
        """Randomly selects the murderer, weapon, and room."""
        return (
            random.choice(self.characters),
            random.choice(self.weapons),
            random.choice(self.rooms),
        )

    def create_players(self) -> None:
        """Creates one human player and three computer players."""
        print("\nChoose your character:")
        for index, character in enumerate(self.characters, start=1):
            print(f"{index}. {character}")

        choice = self.get_number_choice(1, len(self.characters))
        human_character = self.characters[choice - 1]

        self.human_player = Player(
            name="You",
            character=human_character,
            current_room=self.starting_positions[human_character],
            is_human=True,
        )

        self.players.append(self.human_player)

        available_characters = [c for c in self.characters if c != human_character]
        random.shuffle(available_characters)

        for index in range(3):
            character = available_characters[index]
            self.players.append(
                Player(
                    name=f"Computer Player {index + 1}",
                    character=character,
                    current_room=self.starting_positions[character],
                    is_human=False,
                )
            )

    def deal_cards(self) -> None:
        """Removes the solution cards and deals the remaining cards to players."""
        deck = [card for card in self.all_cards if card not in self.solution]
        random.shuffle(deck)

        player_index = 0
        for card in deck:
            self.players[player_index].hand.append(card)
            player_index = (player_index + 1) % len(self.players)

        for card in self.human_player.hand:
            self.notebook.mark_seen(card)

    def display_intro(self) -> None:
        print("=" * 70)
        print("Welcome to Cluedo - Project 2 Part 2")
        print("Solve the mystery by using suggestions, refutations, and deductions.")
        print("=" * 70)

    def display_game_setup(self) -> None:
        print("\nMansion Rooms:")
        for room, connections in self.mansion.rooms.items():
            print(f"- {room}: connects to {', '.join(connections)}")

        print("\nWeapons:")
        for weapon in self.weapons:
            print(f"- {weapon}")

        print("\nCharacters:")
        for character in self.characters:
            print(f"- {character}: starts in {self.starting_positions[character]}")

    def display_human_hand(self) -> None:
        print("\nYour Cards:")
        for card in sorted(self.human_player.hand):
            print(f"- {card}")

    def get_number_choice(self, low: int, high: int) -> int:
        while True:
            try:
                choice = int(input(f"Enter a number from {low} to {high}: "))
                if low <= choice <= high:
                    return choice
                print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")

    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_turn(self) -> None:
        """Moves to the next active player."""
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if self.current_player().active:
                return

    def move_player(self, player: Player) -> None:
        connected_rooms = self.mansion.get_connected_rooms(player.current_room)

        if player.is_human:
            print(f"\nYou are currently in the {player.current_room}.")
            print("Available rooms:")
            for index, room in enumerate(connected_rooms, start=1):
                print(f"{index}. {room}")

            choice = self.get_number_choice(1, len(connected_rooms))
            player.current_room = connected_rooms[choice - 1]
            print(f"You moved to the {player.current_room}.")
        else:
            player.current_room = random.choice(connected_rooms)
            print(f"{player.name} moved to the {player.current_room}.")

    def build_human_suggestion(self, player: Player) -> Suggestion:
        print("\nMake a suggestion.")
        print("The room is automatically your current room.")

        print("\nChoose a suspect:")
        for index, character in enumerate(self.characters, start=1):
            print(f"{index}. {character}")
        character = self.characters[self.get_number_choice(1, len(self.characters)) - 1]

        print("\nChoose a weapon:")
        for index, weapon in enumerate(self.weapons, start=1):
            print(f"{index}. {weapon}")
        weapon = self.weapons[self.get_number_choice(1, len(self.weapons)) - 1]

        room = player.current_room
        return character, weapon, room

    def build_computer_suggestion(self, player: Player) -> Suggestion:
        character = random.choice(self.characters)
        weapon = random.choice(self.weapons)
        room = player.current_room
        return character, weapon, room

    def handle_suggestion(self, player: Player, suggestion: Suggestion) -> None:
        """
        Handles suggestion and refutation.
        Other players are checked in turn order.
        First player with a matching card can refute.
        """
        character, weapon, room = suggestion
        print(
            f"\n{player.name} suggests: "
            f"{character} with the {weapon} in the {room}."
        )

        refuter = None
        shown_card = None

        players_to_check = self.get_players_after(player)

        for other_player in players_to_check:
            matching_cards = [
                card for card in other_player.hand
                if card in suggestion
            ]

            if matching_cards:
                refuter = other_player
                shown_card = random.choice(matching_cards)
                break

        if refuter is None:
            print("No player could refute this suggestion.")
            self.notebook.add_suggestion_record(
                player.name, character, weapon, room, None, None
            )
            return

        print(f"{refuter.name} refuted the suggestion.")

        if player.is_human:
            print(f"{refuter.name} showed you this card: {shown_card}")
            self.notebook.add_suggestion_record(
                player.name, character, weapon, room, refuter.name, shown_card
            )
        else:
            if refuter.is_human:
                print(f"You refuted {player.name}'s suggestion by showing a matching card.")
                self.notebook.add_suggestion_record(
                    player.name, character, weapon, room, "You", "Unknown to computer"
                )
            else:
                self.notebook.add_suggestion_record(
                    player.name, character, weapon, room, refuter.name, "Unknown"
                )

    def get_players_after(self, player: Player) -> List[Player]:
        """Returns players after the suggester in turn order."""
        start_index = self.players.index(player)
        ordered_players = []
        for offset in range(1, len(self.players)):
            index = (start_index + offset) % len(self.players)
            if self.players[index].active:
                ordered_players.append(self.players[index])
        return ordered_players

    def make_accusation(self, player: Player) -> None:
        """Allows a player to make a final accusation."""
        if player.is_human:
            print("\nMake an accusation.")
            print("Warning: If incorrect, you are eliminated.")

            print("\nChoose the murderer:")
            for index, character in enumerate(self.characters, start=1):
                print(f"{index}. {character}")
            character = self.characters[self.get_number_choice(1, len(self.characters)) - 1]

            print("\nChoose the weapon:")
            for index, weapon in enumerate(self.weapons, start=1):
                print(f"{index}. {weapon}")
            weapon = self.weapons[self.get_number_choice(1, len(self.weapons)) - 1]

            print("\nChoose the room:")
            for index, room in enumerate(self.rooms, start=1):
                print(f"{index}. {room}")
            room = self.rooms[self.get_number_choice(1, len(self.rooms)) - 1]
        else:
            unknown = self.notebook.get_unknown_cards()
            character = random.choice(self.characters)
            weapon = random.choice(self.weapons)
            room = random.choice(self.rooms)

        accusation = (character, weapon, room)

        print(
            f"\n{player.name} accuses: "
            f"{character} with the {weapon} in the {room}."
        )

        if accusation == self.solution:
            print("\nCorrect accusation!")
            print(f"{player.name} solved the murder and wins the game!")
            self.game_over = True
        else:
            print("\nIncorrect accusation.")
            player.active = False
            if player.is_human:
                print("You are eliminated from making more suggestions or accusations.")
                print(f"The correct solution was: {self.solution[0]} with the {self.solution[1]} in the {self.solution[2]}.")
                self.game_over = True
            else:
                print(f"{player.name} is eliminated.")

    def human_turn(self, player: Player) -> None:
        while True:
            print("\n" + "=" * 60)
            print(f"Your Turn - Character: {player.character}")
            print(f"Current Room: {player.current_room}")
            print("=" * 60)
            print("1. Move")
            print("2. Make suggestion")
            print("3. Make accusation")
            print("4. View deduction notebook")
            print("5. View your cards")
            print("6. View mansion layout")
            print("7. Quit game")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.move_player(player)
            elif choice == "2":
                suggestion = self.build_human_suggestion(player)
                self.handle_suggestion(player, suggestion)
                break
            elif choice == "3":
                self.make_accusation(player)
                break
            elif choice == "4":
                self.notebook.display()
            elif choice == "5":
                self.display_human_hand()
            elif choice == "6":
                self.display_game_setup()
            elif choice == "7":
                print("Game ended by player.")
                self.game_over = True
                break
            else:
                print("Invalid choice.")

    def computer_turn(self, player: Player) -> None:
        print("\n" + "-" * 60)
        print(f"{player.name}'s Turn - Character: {player.character}")
        print("-" * 60)

        self.move_player(player)

        # Computer players usually make suggestions.
        suggestion = self.build_computer_suggestion(player)
        self.handle_suggestion(player, suggestion)

        # Small chance for computer to make an accusation.
        if random.random() < 0.10 and not self.game_over:
            self.make_accusation(player)

    def active_players_count(self) -> int:
        return sum(1 for player in self.players if player.active)

    def game_loop(self) -> None:
        while not self.game_over and self.active_players_count() > 0:
            player = self.current_player()

            if not player.active:
                self.next_turn()
                continue

            if player.is_human:
                self.human_turn(player)
            else:
                self.computer_turn(player)

            if not self.game_over:
                self.next_turn()

    def start(self) -> None:
        self.display_intro()
        self.display_game_setup()
        self.create_players()
        self.deal_cards()
        self.display_human_hand()
        self.game_loop()


if __name__ == "__main__":
    game = CluedoGame()
    game.start()
