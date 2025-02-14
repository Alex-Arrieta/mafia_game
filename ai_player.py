from knowledge_graph import KnowledgeGraph
from llm_interface import LLMInterface

class AIPlayer:
    """
    Represents an AI-controlled player. Each player has its own knowledge graph and
    LLM session.
    """
    def __init__(self, name, role):
        self.name = name
        self.role = role  # e.g., "mafia", "doctor", "detective", "townsperson"
        self.alive = True
        self.kg = KnowledgeGraph()
        self.llm = LLMInterface(self.name)
        # Initialize the player’s knowledge with its role.
        self.kg.add_fact("role", role)

    def update_game_info(self, info):
        """
        Update the player's knowledge graph with game information.
        'info' should be a dictionary.
        """
        for key, value in info.items():
            self.kg.update_fact(key, value)

    def act(self, phase, context):
        """
        Prompt the LLM (simulated) to decide on an action.
        The context is enriched with game state information (like a list of alive players).
        """
        # Enrich context with player-specific data.
        context = context.copy()
        context["player_name"] = self.name
        context["role"] = self.role
        # Call the simulated LLM to generate an action.
        action = self.llm.generate_action(phase, context)
        return action

    def __str__(self):
        return f"{self.name} ({self.role}){' [dead]' if not self.alive else ''}"