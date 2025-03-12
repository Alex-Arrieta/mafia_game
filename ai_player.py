"""
AIPlayer Module

This module defines the AIPlayer class that encapsulates an AI-controlled player's attributes,
its private knowledge graph, and its LLM interface.
"""

from knowledge_graph import KnowledgeGraph
from llm_interface import LLMInterface


class AIPlayer:
    """
    Represents an AI-controlled player.
    Each player maintains its own knowledge graph and persistent LLM thread.
    """
    def __init__(self, name, role, player_id):
        self.name = name
        self.role = role  # e.g. "mafia", "doctor", "detective", "townsperson"
        self.id = player_id
        self.alive = True
        self.kg = KnowledgeGraph(self.name)
        self.llm = LLMInterface(self.name, self.id)

    def get_kg(self):
        """Return the player's KnowledgeGraph instance."""
        return self.kg

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def act_day_message(self, context):
        """
        Prompt the LLM to generate a day-phase message.
        """
        return self.llm.generate_action("day_message", context)

    def act_day_vote(self, context):
        """
        Prompt the LLM to decide on a day-phase vote.
        """
        return self.llm.generate_action("day_vote", context)

    def act_night(self, context):
        """
        Prompt the LLM to decide on a night-phase action.
        """
        context = context.copy()
        context["player_name"] = self.name
        context["role"] = self.role
        return self.llm.generate_action("night", context)

    def __str__(self):
        return f"{self.name} ({self.role}){' [dead]' if not self.alive else ''}"
