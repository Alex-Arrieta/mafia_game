class KnowledgeGraph:
    """
    A very simple knowledge graph implementation. This is the internal memory
    for an AI player. It stores facts about players and the game state.
    """
    def __init__(self):
        # We simply store facts as key-value pairs
        self.facts = {}

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
