from knowledge_graph import KnowledgeGraph
from llm_interface import LLMInterface

class AIPlayer:
    """
    Represents an AI-controlled player. Each player has its own knowledge graph and LLM session.
    """
    def __init__(self, name, role, id):
        self.name = name
        self.role = role  # e.g., "mafia", "doctor", "detective", "townsperson"
        self.id = id
        self.alive = True
        self.kg = KnowledgeGraph(self.name)
        self.llm = LLMInterface(self.name, self.id)

    def get_kg(self):
        return self.kg
    
    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def update_game_info(self, info):
        """
        Update the player's knowledge graph with game information.
        'info' should be a dictionary.
        """
        for key, value in info.items():
            self.kg.update_fact(key, value)

    def act_day_message(self, context):
        return self.llm.generate_action("day_message", context)

    def act_day_vote(self, context):
        return self.llm.generate_action("day_vote", context)
    
    

    def act_night(self, context):
        """
        Prompt the LLM to decide on an action.
        The context is enriched with game state information (like a list of alive players).
        """
        # Enrich context with player-specific data.
        context = context.copy()
        context["player_name"] = self.name
        context["role"] = self.role
        return self.llm.generate_action("night", context)

    def __str__(self):
        return f"{self.name} ({self.role}){' [dead]' if not self.alive else ''}"
