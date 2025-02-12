import random

class LLMInterface:
    """
    A stub for the LLM interface. In an actual implementation, this class
    would call out to a large language model API using the current narrative
    and knowledge graph information. Here, we simulate a response by choosing
    a valid action at random.
    """
    def __init__(self, player_name):
        self.player_name = player_name

    def generate_action(self, phase, context):
        """
        Generate an action based on the phase and context.
        'context' is a dict containing the narrative and current game state.
        The output is a dict representing the desired action.
        """
        # For simplicity, we choose an action based on phase.
        if phase == "day":
            # For the day, a player may vote or post a message.
            action_choice = random.choice(["vote", "no_vote", "post_message", "no_message"])
            if action_choice == "vote":
                # choose a target at random from alive players other than self:
                alive = context.get("alive_players", [])
                # Remove self from candidate targets.
                candidates = [p for p in alive if p != self.player_name]
                if candidates:
                    target = random.choice(candidates)
                else:
                    target = None
                return {"action": "vote", "target": target}
            elif action_choice == "post_message":
                message = f"{self.player_name} says: I suspect someone!"
                return {"action": "post_message", "message": message}
            elif action_choice == "no_vote":
                return {"action": "no_vote"}
            else:  # "no_message"
                return {"action": "no_message"}

        elif phase == "night":
            role = context.get("role", "townsperson")
            if role == "mafia":
                # Mafia vote for a target to kill.
                alive = context.get("alive_players", [])
                candidates = [p for p in alive if p != self.player_name]
                if candidates:
                    target = random.choice(candidates)
                else:
                    target = None
                return {"action": "mafia_vote", "target": target}
            elif role == "doctor":
                # Doctor saves a target.
                alive = context.get("alive_players", [])
                target = random.choice(alive) if alive else None
                return {"action": "doctor_save", "target": target}
            elif role == "detective":
                # Detective checks someone.
                alive = context.get("alive_players", [])
                candidates = [p for p in alive if p != self.player_name]
                if candidates:
                    target = random.choice(candidates)
                else:
                    target = None
                return {"action": "check_alignment_detective", "target": target}
            else:
                # Townsperson have no night action.
                return {"action": "no_action"}
        else:
            # Unknown phase
            return {"action": "no_action"}
