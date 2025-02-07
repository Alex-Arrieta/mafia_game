from collections import Counter
import random

class Mafia_Player:
    def __init__(self, name, role, alive, KG):
        self.name = name
        self.role = role
        self.alive = alive
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
    
    def get_alive(self):
        return self.alive
    
    def set_alive(self, new_status):
        self.alive = new_status

class Mafia_Game:
    def __init__(self, name, player_list):
        self.name = name
        self.player_list = player_list

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
Mafia_Game("test_game", [p1, p2, p3, p4, p5, p6, p7, p8])
votes = []
votes.append(3)
votes.append(5)
votes.append(3)
print(votes)