import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class LLMInterface:
    """
    An interface to the LLM assistant that uses a persistent thread per player.
    """
    def __init__(self, player_name):
        self.player_name = player_name
        # Initialize the client with the organization and project IDs.
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), 
            organization='org-SmlbKQVG4YpQ3ZyWss1uG0Iu',
            project='proj_Qeh1WBMfbeqqktKMn24e2quf',
        )
        # Retrieve the assistant instance
        self.assistant_id = "asst_U2jta9E4BcrUmu9zFWvXvFG3"
        self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
        # Create a new thread for this player (the thread will keep the chat history)
        thread_response = self.client.beta.threads.create(
            messages=[
                {
                    "role": "assistant",
                    "content": f"Initializing thread for player {self.player_name}."
                }
            ]
        )
        # Save the thread id
        self.thread_id = thread_response.id
        # self._send_run()

    def _send_message(self, role, content):
        """
        Sends a message to the persistent thread and returns the created message.
        """
        msg = self.client.beta.threads.messages.create(
            self.thread_id,
            role=role,
            content=content,
        )
        self._send_run()

    def _get_latest_assistant_message(self):
        """
        Retrieve the list of messages and return the most recent assistant message.
        """
        thread_messages = self.client.beta.threads.messages.list(self.thread_id)
        # Assume that the assistant’s reply is the last message with role "assistant"
        # last_message_id = len(thread_messages.data) - 1
        if thread_messages.data[0].role == "assistant":
            message = thread_messages.data[0].content[0].text.value
            return message
        return None
    
    def _send_run(self):

        run = self.client.beta.threads.runs.create(
            assistant_id=self.assistant_id,
            thread_id=self.thread_id,
        )
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id,
            )
            time.sleep(0.1)
        return run

    def generate_action(self, phase, context):
        """
        Build a prompt based on phase and context, send it to the assistant thread,
        and return the parsed action as a dictionary.
        """
        # Build the prompt according to phase.
        if phase == "day_message":
            prompt = (
                f"Player {self.player_name} ({context.get('role')}) update:\n"
                f"Knowledge Graph:\n{context.get('kg')}\n"
                f"Game context:\n{json.dumps(context, indent=2)}\n"
                "Generate a JSON object with an 'action' key. For example, \n"
                "if posting a message, return {\"action\": \"post_message\", \"message\": \"...\"}. "
                "If nothing to say, return {\"action\": \"no_message\"}.\n"
                
            )
        elif phase == "day_vote":
            prompt = (
                f"Player {self.player_name} ({context.get('role')}) update:\n"
                f"Knowledge Graph:\n{context.get('kg')}\n"
                f"Messages from players:\n{json.dumps(context.get('messages', {}), indent=2)}\n"
                f"Game context:\n{json.dumps(context, indent=2)}\n"
                "Generate a JSON object with a 'target' key indicating the name of the player to vote out, "
                "or return {\"target\": \"no_vote\"} if not voting."
            )
        elif phase == "night":
            # Customize the prompt for night actions based on role.
            role = context.get("role")
            alive = json.dumps(context.get("alive_players"))
            if role == "mafia":
                prompt = (
                    f"Player {self.player_name} (Mafia) update:\n"
                    f"Alive players: {alive}\n"
                    "Choose a target to kill. Return a JSON object like {\"action\": \"mafia_vote\", \"target\": \"PlayerName\"}."
                )
            elif role == "doctor":
                prompt = (
                    f"Player {self.player_name} (Doctor) update:\n"
                    f"Alive players: {alive}\n"
                    "Choose a player to save. Return a JSON object like {\"action\": \"doctor_save\", \"target\": \"PlayerName\"}."
                )
            elif role == "detective":
                prompt = (
                    f"Player {self.player_name} (Detective) update:\n"
                    f"Alive players: {alive}\n"
                    "Choose a player to investigate. Return a JSON object like {\"action\": \"check_alignment_detective\", \"target\": \"PlayerName\"}."
                )
            else:
                prompt = "No night action required."
        else:
            prompt = "Invalid phase."

        # Send the prompt as a user message.
        self._send_message(role="user", content=prompt)
        # (Assuming the assistant responds synchronously.)
        # Retrieve the latest assistant message.
        assistant_response = self._get_latest_assistant_message()
        # Try to parse the response as JSON.
        try:
            action = json.loads(assistant_response)
        except (json.JSONDecodeError, TypeError):
            action = {"action": "error", "message": assistant_response}
        return action
