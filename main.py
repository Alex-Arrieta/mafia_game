import random
from ai_player import AIPlayer
from game_engine import MafiaGameEngine

def assign_roles(player_names):
    """
    For a given list of player names, assign roles.
    For simplicity:
        - With more than 8 players: raise an error.
        - With fewer than 4 players: raise an error.
        - With fewer than 6 players: 1 mafia, 1 doctor, 1 detective, rest townsperson.
        - With 6 or more players: 2 mafia, 1 doctor, 1 detective, rest townsperson.
    """
    num_players = len(player_names)
    roles = []
    
    if num_players > 8:
        raise ValueError("Too many players!")
    elif num_players < 4:
        raise ValueError("Too few players!")
    elif num_players < 6:
        roles = ["mafia", "doctor", "detective"]
        roles.extend(["townsperson"] * (num_players - 3))
    else:
        roles = ["mafia", "mafia", "doctor", "detective"]
        roles.extend(["townsperson"] * (num_players - 4))
    random.shuffle(roles)
    return dict(zip(player_names, roles))

def main():
    # List of player names. In our test, these players are all AI.
    # player_names = ["Alice", "Bob", "Charlie", "Dana", "Eve", "Frank", "Grace", "Hank", "Ivy"]
    # player_names = ["Alice", "Bob", "Charlie"]
    # player_names = ["Alice", "Bob", "Charlie", "Dana"]
    player_names = ["Alice", "Bob", "Charlie", "Dana", "Eve", "Frank", "Grace", "Hank"]
    role_assignment = assign_roles(player_names)
    print("Role assignments:")
    for name, role in role_assignment.items():
        print(f"  {name}: {role}")

    # Create AI players.
    players = [AIPlayer(name, role_assignment[name]) for name in player_names]

    # Optionally, update each player's knowledge graph with initial game info.
    for player in players:
        player.get_kg().initialize_KG(player_names, player.get_role())
        if (player.get_role() == "mafia"):
            for other in players:
                player.get_kg().reset_potential_role(other.get_name())
                if (other.get_role() == "mafia"):
                    player.get_kg().update_player_role(other.get_name(), "mafia")


    # Initialize and run the game engine.
    engine = MafiaGameEngine(players)
    engine.run_game()
    # players[0].get_kg().get_onto().save(f"./Ontology_files/{players[0].get_name()}.rdf")
    print(players[0].get_kg())

if __name__ == "__main__":
    main()

#79/100 wins for mafia with 8 players
#78/100 wins for mafia with 7 players
#95/100 wins for mafia with 6 players
#65/100 wins for mafia with 5 players
#66/100 wins for mafia with 4 players