"""
Mafia Game Engine Module

This module defines the MafiaGameEngine class that manages game phases,
processes player actions, updates knowledge graphs, and determines the game outcome.
"""

import random
from collections import Counter


class MafiaGameEngine:
    """
    The MafiaGameEngine handles the game loop by running day and night phases until a win condition is met.
    """
    def __init__(self, players):
        """
        Args:
            players (list): List of AIPlayer objects.
        """
        self.players = {player.get_name(): player for player in players}
        self.day_count = 0
        self.night_count = 0
        self.narrative_file = "full_narrative.txt"
        # Clear previous narrative.
        with open(self.narrative_file, "w") as f:
            f.write("")

    def get_alive_players(self):
        """Return a list of names of alive players."""
        return [name for name, player in self.players.items() if player.alive]

    def announce(self, message):
        """
        Log and print a game event.
        """
        with open(self.narrative_file, "a") as f:
            f.write(message + "\n")
        print(message)

    def day_phase(self):
        """
        Conduct the day phase: gather messages and votes from players.
        """
        self.day_count += 1
        header = f"\n{'='*40}\nDAY {self.day_count}\n{'='*40}"
        self.announce(header)
        alive_players = self.get_alive_players()

        # Phase 1: Collect messages (in randomized order).
        day_messages = {}
        previous_messages = {}  # accumulate messages as they are produced
        speaking_order = alive_players.copy()
        random.shuffle(speaking_order)
        for name in speaking_order:
            player = self.players[name]
            # The context now includes what has been said so far.
            context = {
                "alive_players": alive_players,
                "player_name": name,
                "role": player.get_role(),
                "kg": str(player.get_kg()),
                "previous_messages": previous_messages.copy()
            }
            action = player.act_day_message(context)
            if action.get("action") == "post_message":
                message = action.get("message", "").strip()
                day_messages[name] = message
                previous_messages[name] = message
                # Format the message with a clear prefix.
                self.announce(f">>> {name} ({player.get_role()}): {message}")
            else:
                day_messages[name] = "no_message"
                previous_messages[name] = "[No message]"
                self.announce(f">>> {name} ({player.get_role()}): [No message]")

        # Phase 2: Collect votes (also randomized order).
        self.announce(f"\n{'-'*40}\nVoting Phase\n{'-'*40}")
        votes = {}
        voting_order = alive_players.copy()
        random.shuffle(voting_order)
        for name in voting_order:
            player = self.players[name]
            context = {
                "alive_players": alive_players,
                "player_name": name,
                "role": player.get_role(),
                "kg": str(player.get_kg()),
                "previous_messages": previous_messages.copy()
            }
            action = player.act_day_vote(context)
            votes[name] = action.get("target", "no_vote")
            self.announce(f"*** {name} votes: {votes[name]}")
        
        # Tally votes.
        # Normalize vote targets by stripping extra spaces and trailing commas.
        vote_list = [target.strip().rstrip(",") for target in votes.values() if target != "no_vote" and target.strip()]
        if vote_list:
            vote_count = Counter(vote_list)
            most_common = vote_count.most_common()
            max_votes = most_common[0][1]
            # Find all candidates with the maximum number of votes.
            candidates = [candidate for candidate, count in most_common if count == max_votes]
            if len(candidates) > 1:
                self.announce(
                    f"\n>>> There is a tie among {', '.join(candidates)} (each received {max_votes} votes). No one is eliminated today."
                )
            else:
                target = candidates[0]
                self.announce(
                    f"\n>>> Players voted to eliminate {target} (received {max_votes} vote{'s' if max_votes != 1 else ''})."
                )
                self.eliminate_player(target)
        else:
            self.announce("\n>>> No votes were cast. No one is eliminated today.")


    def night_phase(self):
        """
        Conduct the night phase: process mafia, doctor, and detective actions.
        """
        self.night_count += 1
        self.announce(f"\n--- Night {self.night_count} ---")
        alive_players = self.get_alive_players()

        mafia_votes = []
        doctor_action = None
        detective_action = None
        detective_player = None

        for name in alive_players:
            player = self.players[name]
            context = {"alive_players": alive_players, "player_name": name, "role": player.get_role()}
            if player.get_role() in ["mafia", "doctor", "detective"]:
                action = player.act_night(context)
                if action.get("action") == "mafia_vote" and player.get_role() == "mafia":
                    mafia_votes.append(action.get("target"))
                elif action.get("action") == "doctor_save" and player.get_role() == "doctor":
                    doctor_action = action.get("target")
                elif action.get("action") == "check_alignment_detective" and player.get_role() == "detective":
                    detective_action = action.get("target")
                    detective_player = player

        if mafia_votes:
            vote_count = {}
            for target in mafia_votes:
                if target:
                    vote_count[target] = vote_count.get(target, 0) + 1
            target = max(vote_count, key=vote_count.get)
            self.announce(f"Mafia targeted {target}.")
            for player in self.players.values():
                player.get_kg().remove_potential_role(target, "mafia")
            if doctor_action == target:
                self.announce(f"Doctor saved {target} during the night!")
            else:
                self.announce(f"{target} was killed during the night!")
                self.eliminate_player(target)
        else:
            self.announce("No mafia actions were taken tonight.")

        if detective_action:
            target_player = self.players.get(detective_action)
            if target_player:
                alignment = "mafia" if target_player.get_role() == "mafia" else "not mafia"
                self.announce(f"Detective checked {detective_action} and found that they are {alignment}.")
                detective_player.get_kg().update_player_role(detective_action, alignment)
            else:
                self.announce("Detective's target was invalid.")

    def eliminate_player(self, name):
        """
        Mark a player as eliminated and update all players' knowledge graphs.
        """
        if name in self.players and self.players[name].alive:
            self.players[name].alive = False
            self.announce(f"{name} has been eliminated.")
            for player in self.players.values():
                player.get_kg().update_player_alive(name, False)

    def check_game_over(self):
        """
        Check if the game is over and return (game_over, winning_team).
        """
        alive = self.get_alive_players()
        mafia_alive = [p.get_name() for p in self.players.values() if p.alive and p.get_role() == "mafia"]
        town_alive = [p.get_name() for p in self.players.values() if p.alive and p.get_role() != "mafia"]

        if not mafia_alive:
            return True, "Town"
        if len(mafia_alive) >= len(town_alive):
            return True, "Mafia"
        return False, None

    def run_game(self):
        """
        Run the game loop until a win condition is met.
        Returns the winning team as a string.
        """
        game_over = False
        while not game_over:
            self.day_phase()
            game_over, winner = self.check_game_over()
            if game_over:
                break
            self.night_phase()
            game_over, winner = self.check_game_over()
        self.announce(f"\nGame Over! The {winner} have won!")
        return winner
