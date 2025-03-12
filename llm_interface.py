"""
LLM Interface Module

This module defines the LLMInterface class that encapsulates interactions
with the OpenAI assistant via persistent threads.
"""

import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Mapping from player ID to a fixed assistant ID.
id_map = {
    0: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
    1: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
    2: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
    3: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
    4: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
    5: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
    6: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
    7: "asst_U2jta9E4BcrUmu9zFWvXvFG3",
}


class LLMInterface:
    """
    Provides an interface to the OpenAI assistant using a persistent thread per player.
    """
    def __init__(self, player_name, player_id):
        self.player_name = player_name
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization="org-SmlbKQVG4YpQ3ZyWss1uG0Iu",
            project="proj_Qeh1WBMfbeqqktKMn24e2quf",
        )
        self.assistant_id = id_map[player_id]
        self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
        # Create a new thread for this player.
        thread_response = self.client.beta.threads.create(
            messages=[
                {
                    "role": "assistant",
                    "content": f"Initializing thread for player {self.player_name}."
                }
            ]
        )
        self.thread_id = thread_response.id

    def _send_message(self, role, content):
        """
        Send a message to the persistent thread and trigger a run.
        """
        self.client.beta.threads.messages.create(
            self.thread_id,
            role=role,
            content=content,
        )
        self._send_run()

    def _get_latest_assistant_message(self):
        """
        Retrieve the most recent assistant message from the thread.
        """
        thread_messages = self.client.beta.threads.messages.list(self.thread_id)
        for msg in reversed(thread_messages.data):
            if msg.role == "assistant":
                return msg.content
        return None

    def _send_run(self):
        """
        Trigger a run for the thread and wait until it completes.
        """
        run = self.client.beta.threads.runs.create(
            assistant_id=self.assistant_id,
            thread_id=self.thread_id,
        )
        while run.status in ("queued", "in_progress"):
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id,
            )
            time.sleep(0.1)
        return run

    def generate_action(self, phase, context):
        """
        Build a prompt based on the current phase and context,
        send it to the assistant thread, and parse the JSON response.
        """
        if phase == "day_message":
            prompt = (
                f"Player {self.player_name} ({context.get('role')}) update:\n"
                f"Knowledge Graph:\n{context.get('kg')}\n"
                f"Game context:\n{json.dumps(context, indent=2)}\n"
                "Generate a JSON object with an 'action' key. For example, if posting a message, "
                "return {\"action\": \"post_message\", \"message\": \"...\"}. "
                "If nothing to say, return {\"action\": \"no_message\"}.\n"
                "Remember to include the word 'json' in your response so that the response_format is valid."
            )
        elif phase == "day_vote":
            prompt = (
                f"Player {self.player_name} ({context.get('role')}) update:\n"
                f"Knowledge Graph:\n{context.get('kg')}\n"
                f"Messages from players:\n{json.dumps(context.get('messages', {}), indent=2)}\n"
                f"Game context:\n{json.dumps(context, indent=2)}\n"
                "Generate a JSON object with a 'target' key indicating which player to vote out, "
                "or return {\"target\": \"no_vote\"} if not voting.\n"
                "Ensure your response is valid json."
            )
        elif phase == "night":
            role = context.get("role")
            alive = json.dumps(context.get("alive_players"))
            if role == "mafia":
                prompt = (
                    f"Player {self.player_name} (Mafia) update:\n"
                    f"Alive players: {alive}\n"
                    "Choose a target to kill. Return a JSON object like {\"action\": \"mafia_vote\", \"target\": \"PlayerName\"}.\n"
                    "Ensure your response is valid json."
                )
            elif role == "doctor":
                prompt = (
                    f"Player {self.player_name} (Doctor) update:\n"
                    f"Alive players: {alive}\n"
                    "Choose a player to save. Return a JSON object like {\"action\": \"doctor_save\", \"target\": \"PlayerName\"}.\n"
                    "Ensure your response is valid json."
                )
            elif role == "detective":
                prompt = (
                    f"Player {self.player_name} (Detective) update:\n"
                    f"Alive players: {alive}\n"
                    "Choose a player to investigate. Return a JSON object like {\"action\": \"check_alignment_detective\", \"target\": \"PlayerName\"}.\n"
                    "Ensure your response is valid json."
                )
            else:
                prompt = "No night action required."
        else:
            prompt = "Invalid phase."

        self._send_message(role="user", content=prompt)
        assistant_response = self._get_latest_assistant_message()
        try:
            action = json.loads(assistant_response)
        except (json.JSONDecodeError, TypeError):
            action = {"action": "error", "message": assistant_response}
        return action
