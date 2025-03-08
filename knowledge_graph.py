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

            class potentialRole(DataProperty):
                range = [str]
                
        self.onto_instance = Mafia_Game_Knowledge("my_game_"+self.name)

    def get_onto(self):
        return self.onto
        
    def initialize_KG(self, players, role):
        for player in players:
            other_player = self.onto.Player("player_"+player)
            self.onto_instance.has_player.append(other_player)
            other_player.alive = True
            other_player.role = "Unknown"
            other_player.potentialRole.append("mafia")
            if player == self.name:
                other_player.potentialRole.remove("mafia")
                other_player.role = role
        #self.onto.save(f"C:/Users/arrie/OneDrive - Cal Poly/Code/CSC581/mafia_game/Ontology_files/{self.name}.rdf")
                
    def update_player_alive(self, player, status):
        self.onto.search_one(iri = f"*player_{player}").alive = status

    def update_player_role(self, player, role):
        p = self.onto.search_one(iri = f"*player_{player}")
        p.role = role
        p.potentialRole = []

    def add_potential_role(self, player, role):
        self.onto.search_one(iri = f"*player_{player}").potentialRole.append(role)

    def remove_potential_role(self, player, role):
        #Check that person already has suspected role
        if role in self.onto.search_one(iri = f"*player_{player}").potentialRole:
            self.onto.search_one(iri = f"*player_{player}").potentialRole.remove(role)

    def __str__(self):
        to_return = ""
        for individual in self.onto.individuals():
            to_return = to_return + str(individual) + ": "
            for prop in individual.get_properties():
                for value in prop[individual]:
                    to_return = to_return + (".%s == %s" % (prop.python_name, value)) + ", "
            to_return = to_return + "\n"
        return to_return
