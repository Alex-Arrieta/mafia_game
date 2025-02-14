import random
from collections import Counter

class MafiaGameEngine:
    """
    The Mafia game engine. It tracks players, game phases, and processes actions.
    """
    def __init__(self, players):
        """
        players: a list of AIPlayer objects.
        """
        self.players = {player.name: player for player in players}
        self.day_count = 0
        self.night_count = 0
        self.narrative = []  # A log of narrative events

    def get_alive_players(self):
        """Return a list of names of alive players."""
        return [name for name, player in self.players.items() if player.alive]

    def announce(self, message):
        """Add a message to the narrative and print it."""
        self.narrative.append(message)
        print(message)

    def day_phase(self):
        """Conduct the day phase: players may vote and post messages."""
        self.day_count += 1
        self.announce(f"\n--- Day {self.day_count} ---")
        alive_players = self.get_alive_players()

        # Gather day actions from each alive player.
        day_actions = {}
        for name in alive_players:
            player = self.players[name]
            # Build context for the player.
            context = {"alive_players": alive_players}
            action = player.act("day", context)
            day_actions[name] = action

            # Process any messages.
            if action["action"] == "post_message":
                self.announce(action.get("message", ""))
        
        # Tally votes (if any).
        votes = [action.get("target") for action in day_actions.values() if action["action"] == "vote" and action.get("target")]
        if votes:
            vote_count = Counter(votes)
            most_common = vote_count.most_common(1)[0]
            target, count = most_common
            # For this simple example, we require a plurality vote.
            self.announce(f"Players voted to eliminate {target} (received {count} vote{'s' if count != 1 else ''}).")
            self.eliminate_player(target)
        else:
            self.announce("No votes were cast. No one is eliminated today.")

    def night_phase(self):
        """Conduct the night phase: special roles take actions."""
        self.night_count += 1
        self.announce(f"\n--- Night {self.night_count} ---")
        alive_players = self.get_alive_players()

        # Collect actions by role.
        mafia_votes = []
        doctor_action = None
        detective_action = None

        for name in alive_players:
            player = self.players[name]
            context = {"alive_players": alive_players}
            # Only roles with night actions respond.
            if player.role in ["mafia", "doctor", "detective"]:
                action = player.act("night", context)
                if action["action"] == "mafia_vote" and player.role == "mafia":
                    mafia_votes.append(action.get("target"))
                elif action["action"] == "doctor_save" and player.role == "doctor":
                    doctor_action = action.get("target")
                elif action["action"] == "check_alignment_detective" and player.role == "detective":
                    detective_action = action.get("target")

        # Process mafia votes.
        if mafia_votes:
            vote_count = {}
            for target in mafia_votes:
                if target:
                    vote_count[target] = vote_count.get(target, 0) + 1
            # Choose the target with the most votes.
            target = max(vote_count, key=vote_count.get)
            self.announce(f"Mafia targeted {target}.")

            # Process doctor save.
            if doctor_action == target:
                self.announce(f"Doctor saved {target} during the night!")
            else:
                self.announce(f"{target} was killed during the night!")
                self.eliminate_player(target)
        else:
            self.announce("No mafia actions were taken tonight.")

        # Process detective action.
        if detective_action:
            # The detective gets a result.
            target_player = self.players.get(detective_action)
            if target_player:
                alignment = "mafia" if target_player.role == "mafia" else "not mafia"
                self.announce(f"Detective checked {detective_action} and found that they are {alignment}.")
            else:
                self.announce("Detective's target was invalid.")

    def eliminate_player(self, name):
        """Eliminate (kill) the player by name."""
        if name in self.players and self.players[name].alive:
            self.players[name].alive = False
            self.announce(f"{name} has been eliminated.")

    def check_game_over(self):
        """Return (game_over: bool, winning_team: str or None)."""
        alive = self.get_alive_players()
        mafia_alive = [p.name for p in self.players.values() if p.alive and p.role == "mafia"]
        town_alive = [p.name for p in self.players.values() if p.alive and p.role != "mafia"]

        if not mafia_alive:
            return (True, "Town")
        if len(mafia_alive) >= len(town_alive):
            return (True, "Mafia")
        return (False, None)

    def run_game(self):
        """Run the game loop until a win condition is met."""
        game_over = False
        while not game_over:
            self.day_phase()
            game_over, winner = self.check_game_over()
            if game_over:
                break

            self.night_phase()
            game_over, winner = self.check_game_over()
        self.announce(f"\nGame Over! The {winner} have won!")