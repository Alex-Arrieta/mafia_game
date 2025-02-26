from owlready2 import *

# Make different ontology for each player and one maintained by the game as a ground truth
#Visualize with https://ontopea.com/
#Convert to TTL with https://www.easyrdf.org/converter

class KnowledgeGraph:
    """
    A very simple knowledge graph implementation. This is the internal memory
    for an AI player. It stores facts about players and the game state.
    """
    def __init__(self, name):
        self.name = name
        self.onto = get_ontology(f"http://{self.name}.org/onto.owl")
        with self.onto:
            class Mafia_Game_Knowledge(Thing): #Overarching central node in KG to act as anchor point
                pass
            
            class Player(Thing):
                pass

            class is_playing_in(ObjectProperty):
                domain = [Player]
                range = [Mafia_Game_Knowledge]

            class has_player(ObjectProperty):
                domain           = [Mafia_Game_Knowledge]
                range            = [Player]
                inverse_property = is_playing_in

            class alive(DataProperty, FunctionalProperty): # Each player is alive or dead
                domain    = [Player]
                range     = [bool]

            class role(DataProperty, FunctionalProperty):
                domain = [Player]
                range = [str]
        self.onto_instance = Mafia_Game_Knowledge("my_game_"+self.name)
        
    def initialize_KG(self, players, role):
        for player in players:
            other_player = self.onto.Player("player_"+player)
            self.onto_instance.has_player.append(other_player)
            other_player.alive = True
            other_player.role = "Unknown"
            if player == self.name:
                other_player.role = role
                

    def add_fact(self, key, value):
        """Add or update a fact."""
        self.facts[key] = value

    def get_fact(self, key):
        """Retrieve a fact."""
        return self.facts.get(key, None)

    def update_fact(self, key, value):
        """Update a fact."""
        self.facts[key] = value

    def __str__(self):
        return str(self.facts)
