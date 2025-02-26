from collections import Counter
import random
from owlready2 import *

onto = get_ontology("http://test.org/mafia_game.owl") # Make different ontology for each player and one maintained by the game as a ground truth
#Visualize with https://ontopea.com/
#Convert to TTL with https://www.easyrdf.org/converter


with onto:
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

class Mafia_Player:
    def __init__(self, name, role, alive):
        self.name = name
        self.role = role
        self.alive = alive
        self.KG = None

    def set_KG(self, KG):
        self.KG = KG

    def cast_vote(self, game):
        players = game.get_players()
        vote = 1
        if players[vote].get_alive == False:
            print("Invalid selection")
            return -1
        return vote

    def mafia_selection(self):
        return 1
    
    def get_role(self):
        return self.role
    
    def get_name(self):
        return self.name
    
    def get_alive(self):
        return self.alive
    
    def set_alive(self, new_status):
        self.alive = new_status

    def get_KG(self):
        return self.KG
    
    def print_all_props(self):
        for prop in self.KG.get_properties():
            for value in prop[self.KG]:
                print(".%s == %s" % (prop.python_name, value))

class Mafia_Game:
    def __init__(self, name, player_count):
        self.name = name
        self.player_list = []
        #Initalize all the players
        for i in range(player_count):
            self.player_list.append(Mafia_Player("Player_"+str(i), "TownsPerson", True))

        #Now for each player we initialize a KG
        for player_i in self.player_list:
            currKG = Mafia_Game_Knowledge("my_game_"+player_i.get_name())
            for player_j in self.player_list:
                other_player = Player("player_"+player_j.get_name())
                currKG.has_player.append(other_player)
                other_player.alive = True
                other_player.role = "Unknown"
                if player_i == player_j:
                    other_player.role = player_i.get_role()
            player_i.set_KG(currKG)


    def get_players(self):
        return self.player_list

    def vote(self):
        votes = []
        for player in self.player_list:
            if player.get_alive == True:
                votes.append(self.player.cast_vote(self))
        tot_votes = Counter(votes).most_common(2)
        if(tot_votes[0][1] == tot_votes [1][1]):
            print("even vote, no kill")
            return -1
        self.player_list[tot_votes[0][0]].set_alive(False)
    
    def talk():
        print("Good job talking")
        return 0
    
    def mafia_vote(self):
        votes = []
        for player in self.player_list:
            if player.get_role == "Mafia" and player.get_alive == True:
                votes.append(player.mafia_selection())
        self.player_list[votes[random.randrange(0, len(votes)-1)]].set_alive(False)
    
    def doctor_save():
        return
    
    def check_alignment_detective():
        return
    
    def run_round(self):
        while True:
            self.talk()
            self.vote()
            self.mafia_vote()
            self.doctor_save()
            self.sheriff_accuse()
            civ_alive = 0
            mafia_alive = 0
            for player in self.player_list:
                if player.get_role == "Mafia" and player.get_alive == True:
                    mafia_alive += 1
                elif player.get_alive == True:
                    civ_alive += 1
            if civ_alive <= mafia_alive:
                print("Lmaoooooo mafia got yall ass")
                return 0
            elif mafia_alive == 0:
                print("Mafia got rekt")
                return 1
    
p1 = Mafia_Player("p1", "Mafia", True)
p2 = Mafia_Player("p2", "Mafia", True)
p3 = Mafia_Player("p3", "Mafia", True)
p4 = Mafia_Player("p4", "Mafia", True)
p5 = Mafia_Player("p5", "Mafia", True)
p6 = Mafia_Player("p6", "Mafia", True)
p7 = Mafia_Player("p7", "Mafia", True)
p8 = Mafia_Player("p8", "Mafia", True)
game = Mafia_Game("test_game", 8)
player = game.get_players()[0]
KG = player.get_KG()
for prop in KG.get_properties():
    for value in prop[KG]:
        print(".%s == %s" % (prop.python_name, value))
        for prop2 in value.get_properties():
            for value2 in prop2[value]:
                print(".%s == %s" % (prop2.python_name, value2))
onto.save("C:/Users/arrie/OneDrive - Cal Poly/Code/CSC581/mafia_game/example.rdf")