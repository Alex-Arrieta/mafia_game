#!/usr/bin/env python3
"""
Mafia Simulator Main Module

This module provides a command-line interface for running the Mafia game.
It supports running a single game or evaluating the LLM agents over multiple games,
recording the win rates for the mafia team.
"""

import argparse
import random
import sys
from ai_player import AIPlayer
from game_engine import MafiaGameEngine

def assign_roles(player_names):
    """
    Assign roles to players based on the number of players.
    
    Rules:
      - Fewer than 4 players: error.
      - More than 8 players: error.
      - 4-5 players: 1 mafia, 1 doctor, 1 detective, rest townsperson.
      - 6 or more players: 2 mafia, 1 doctor, 1 detective, rest townsperson.
    
    Returns:
        dict: Mapping from player name to role.
    """
    num_players = len(player_names)
    if num_players > 8:
        raise ValueError("Too many players! Maximum allowed is 8.")
    if num_players < 4:
        raise ValueError("Too few players! Minimum required is 4.")
    
    roles = []
    if num_players < 6:
        roles = ["mafia", "doctor", "detective"]
        roles.extend(["townsperson"] * (num_players - 3))
    else:
        roles = ["mafia", "mafia", "doctor", "detective"]
        roles.extend(["townsperson"] * (num_players - 4))
    random.shuffle(roles)
    return dict(zip(player_names, roles))


class GameManager:
    """
    GameManager sets up the AI players and starts the game engine.
    It also provides an evaluation method to run multiple game simulations.
    """
    def __init__(self, player_names):
        self.player_names = player_names
        self.role_assignment = assign_roles(player_names)
        self.players = self._create_players()

    def _create_players(self):
        """
        Create AIPlayer instances for each name with a unique ID.
        """
        players = []
        for idx, name in enumerate(self.player_names):
            role = self.role_assignment[name]
            players.append(AIPlayer(name, role, idx))
        return players

    def initialize_knowledge_graphs(self):
        """
        Initialize the knowledge graphs for each player.
        Mafia players update their graph to know their fellow mafia.
        """
        for player in self.players:
            player.get_kg().initialize_KG(self.player_names, player.get_role())
            if player.get_role() == "mafia":
                for other in self.players:
                    player.get_kg().reset_potential_role(other.get_name())
                    if other.get_role() == "mafia":
                        player.get_kg().update_player_role(other.get_name(), "mafia")

    def run_game(self):
        """
        Initialize the knowledge graphs and run a single game.
        """
        self.initialize_knowledge_graphs()
        engine = MafiaGameEngine(self.players)
        engine.run_game()
        # Return the winning team for evaluation purposes.
        return engine.check_game_over()[1]

    def evaluate(self, num_games):
        """
        Run the game simulation multiple times and report mafia win percentage.
        
        Args:
            num_games (int): Number of games to simulate.
        
        Returns:
            float: Percentage of games won by mafia.
        """
        mafia_wins = 0
        for i in range(num_games):
            # Reset players for each game.
            players = []
            role_assignment = assign_roles(self.player_names)
            for idx, name in enumerate(self.player_names):
                players.append(AIPlayer(name, role_assignment[name], idx))
            # Initialize knowledge graphs
            for player in players:
                player.get_kg().initialize_KG(self.player_names, player.get_role())
                if player.get_role() == "mafia":
                    for other in players:
                        player.get_kg().reset_potential_role(other.get_name())
                        if other.get_role() == "mafia":
                            player.get_kg().update_player_role(other.get_name(), "mafia")
            engine = MafiaGameEngine(players)
            winning_team = engine.run_game()  # run_game logs the narrative and runs until game over
            if winning_team.lower() == "mafia":
                mafia_wins += 1
            # Optional: Print progress
            print(f"Game {i+1}/{num_games} complete. Winner: {winning_team}")
        win_rate = (mafia_wins / num_games) * 100.0
        print(f"\nEvaluation complete. Mafia win rate: {win_rate:.2f}% over {num_games} games.")
        return win_rate


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Mafia Simulator: Run a single game or evaluate LLM agents over multiple games."
    )
    parser.add_argument(
        "--players",
        type=str,
        default="Alice,Bob,Charlie,Dana",
        help="Comma-separated list of player names (default: Alice,Bob,Charlie,Dana)"
    )
    parser.add_argument(
        "--eval",
        type=int,
        default=0,
        help="Number of games to run for evaluation. If 0 (default), a single game is played."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    player_names = [name.strip() for name in args.players.split(",") if name.strip()]
    if len(player_names) < 4:
        print("Error: At least 4 players are required.")
        sys.exit(1)

    if args.eval > 0:
        print(f"Running evaluation over {args.eval} games...")
        gm = GameManager(player_names)
        gm.evaluate(args.eval)
    else:
        print("Starting a single game...")
        # Display role assignments.
        role_assignment = assign_roles(player_names)
        print("Role assignments:")
        for name, role in role_assignment.items():
            print(f"  {name}: {role}")

        gm = GameManager(player_names)
        gm.run_game()


if __name__ == "__main__":
    main()
