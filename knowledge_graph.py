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
        self.onto = get_ontology(f"http://test.org/onto_{self.name}.owl")
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
            other_player = self.onto.Player(f"player_{player}")
            self.onto_instance.has_player.append(other_player)
            other_player.alive = True
            other_player.role = "Unknown"
            other_player.potentialRole.append("mafia")
            if player == self.name:
                other_player.potentialRole.remove("mafia")
                other_player.role = role
        #self.onto.save(f"C:/Users/arrie/OneDrive - Cal Poly/Code/CSC581/mafia_game/Ontology_files/{self.name}.rdf")
                
    def update_player_alive(self, player, status):
        individuals = self.onto.search(iri = f"*player_{player}")
        to_change = next((s for s in individuals if f"onto_{self.name}" in str(s)), None)
        to_change.alive = status

    def update_player_role(self, player, role):
        individuals = self.onto.search(iri = f"*player_{player}")
        to_change = next((s for s in individuals if f"onto_{self.name}" in str(s)), None)
        to_change.role = role
        to_change.potentialRole = []

    def reset_potential_role(self, player):
        individuals = self.onto.search(iri = f"*player_{player}")
        to_change = next((s for s in individuals if f"onto_{self.name}" in str(s)), None)
        to_change.potentialRole = []

    def add_potential_role(self, player, role):
        individuals = self.onto.search(iri = f"*player_{player}")
        to_change = next((s for s in individuals if f"onto_{self.name}" in str(s)), None)
        to_change.potentialRole.append(role)

    def remove_potential_role(self, player, role):
        individuals = self.onto.search(iri = f"*player_{player}")
        to_change = next((s for s in individuals if f"onto_{self.name}" in str(s)), None)
        if role in to_change.potentialRole: #Check that person already has suspected role
            to_change.potentialRole.remove(role)

    def __str__(self):
        to_return = ""
        for individual in self.onto.individuals():
            to_return = to_return + str(individual) + ": "
            for prop in individual.get_properties():
                for value in prop[individual]:
                    to_return = to_return + (".%s == %s" % (prop.python_name, value)) + ", "
            to_return = to_return + "\n"
        return to_return
