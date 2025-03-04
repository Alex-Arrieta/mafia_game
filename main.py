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
    # player_names = ["Alice", "Bob", "Charlie", "Dana", "Eve"]
    player_names = ["Alice", "Bob", "Charlie", "Dana", "Eve", "Frank", "Grace", "Hank"]
    role_assignment = assign_roles(player_names)
    print("Role assignments:")
    for name, role in role_assignment.items():
        print(f"  {name}: {role}")

    # Create AI players.
    players = [AIPlayer(name, role_assignment[name]) for name in player_names]

    # Optionally, update each player's knowledge graph with initial game info.
    for player in players:
        player.get_kg().initialize_KG(player_names, role_assignment[player.get_name()])

    # Initialize and run the game engine.
    engine = MafiaGameEngine(players)
    engine.run_game()
    #players[0].get_kg().get_onto().save(f"C:/Users/arrie/OneDrive - Cal Poly/Code/CSC581/mafia_game/Ontology_files/{players[0].get_name()}.rdf")

if __name__ == "__main__":
    main()