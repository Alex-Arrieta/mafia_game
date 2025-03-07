import random
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


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
            # action_choice = random.choice(["vote", "no_vote", "post_message", "no_message"])

            actions = ["vote", "no_vote", "post_message", "no_message"]
            alive = context.get("alive_players", [])
            candidates = [p for p in alive if p != self.player_name]
            action_choice = self.query_gemini(1, f"Choose an available action: {actions}.")
            if action_choice == "vote":
                target = self.query_gemini(1, f"You have chosen to vote out a player, select a player from {candidates}.")
                return {"action": "vote", "target": target}
            elif action_choice == "post_message":
                # TODO: Add KG in to help make decisions?
                role = context.get("role", "townsperson")
                message = self.query_gemini(1, f"Based on your knowledge graph of other players and of your own role as a {role}, write a message to help other agents.")
                # message = f"{self.player_name} says: I suspect someone!"
                return {"action": "post_message", "message": message}
            elif action_choice == "no_vote":
                return {"action": "no_vote"}
            else:  # "no_message"
                return {"action": "no_message"}
            # if action_choice == "vote":
            #     # choose a target at random from alive players other than self:
            #     alive = context.get("alive_players", [])
            #     # Remove self from candidate targets.
            #     candidates = [p for p in alive if p != self.player_name]
            #     if candidates:
            #         target = random.choice(candidates)
            #     else:
            #         target = None
            #     return {"action": "vote", "target": target}
            # elif action_choice == "post_message":
            #     message = f"{self.player_name} says: I suspect someone!"
            #     return {"action": "post_message", "message": message}
            # elif action_choice == "no_vote":
            #     return {"action": "no_vote"}
            # else:  # "no_message"
            #     return {"action": "no_message"}

        elif phase == "night":
            role = context.get("role", "townsperson")
            if role == "mafia":
                # Mafia vote for a target to kill.
                alive = context.get("alive_players", [])
                candidates = [p for p in alive if p != self.player_name]
                # TODO: Add KG in to help make decisions?
                target = self.query_gemini(1, f"You are the mafia and you must eliminate a player, select a player from {candidates}.")
                return {"action": "mafia_vote", "target": target}
            elif role == "doctor":
                # Doctor saves a target.
                alive = context.get("alive_players", [])
                # TODO: Add KG in to help make decisions?
                target = self.query_gemini(1, f"You are the doctor and you must choose a player to save, select a player from {alive}.")
                return {"action": "doctor_save", "target": target}
            elif role == "detective":
                # Detective checks someone.
                alive = context.get("alive_players", [])
                candidates = [p for p in alive if p != self.player_name]
                # TODO: Add KG in to help make decisions?
                # TODO: Add absolute knoweldge KG in to get chosen agent's role?
                target = self.query_gemini(1, f"You are the detective and you can investigate a player, select a player from {candidates} to check their role.")
                return {"action": "check_alignment_detective", "target": target}
            else:
                # Townsperson have no night action.
                return {"action": "no_action"}
        else:
            # Unknown phase
            return {"action": "no_action"}

    def query_gemini(self, session_id, prompt, model="gemini-1.5-pro", max_tokens=200):
        """Query Google Gemini API and return response."""
        try:
            response = genai.GenerativeModel(model).generate_content(f"Session {session_id}: {prompt}")
            return response.text
        except Exception as e:
            return f"Error: {e}"


# test = LLMInterface("TestPlayer")
# context = {}
# test.generate_action("day", context)

# for i in range(5):
#     # response = test.query_gemini(i, "ListModels")
#
#     response = test.query_gemini(i, "Give me a one word response along with the current session id in this format: (session_is, response)")
#     print(response)

# for model in genai.list_models():
#     print(model.name)

