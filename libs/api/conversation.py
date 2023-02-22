import json

from apps import GLOBAL_REDIS_CLIENT


class Conversation:
    """
    For handling multiple conversations
    """

    def check_conversation(self, key):
        return GLOBAL_REDIS_CLIENT.hget("conversations", key)

    def add_conversation(self, key: str, history: list) -> None:
        """
        Adds a history list to the conversations dict with the id as the key
        """
        GLOBAL_REDIS_CLIENT.hset("conversations", key, json.dumps(history))

    def get_conversation(self, key: str) -> list:
        """
        Retrieves the history list from the conversations dict with the id as the key
        """
        history = GLOBAL_REDIS_CLIENT.hget("conversations", key)
        return json.loads(history)

    def remove_conversation(self, key: str) -> None:
        """
        Removes the history list from the conversations dict with the id as the key
        """
        GLOBAL_REDIS_CLIENT.hdel("conversations", key)


class ConversationLocal:
    """
    For handling multiple conversations
    """

    def __init__(self) -> None:
        self.conversations = {}

    def check_conversation(self, key):
        return self.conversations[key]

    def add_conversation(self, key: str, history: list) -> None:
        """
        Adds a history list to the conversations dict with the id as the key
        """
        self.conversations[key] = history

    def get_conversation(self, key: str) -> list:
        """
        Retrieves the history list from the conversations dict with the id as the key
        """
        return self.conversations[key]

    def remove_conversation(self, key: str) -> None:
        """
        Removes the history list from the conversations dict with the id as the key
        """
        del self.conversations[key]

    def __str__(self) -> str:
        """
        Creates a JSON string of the conversations
        """
        return json.dumps(self.conversations)

    def save(self, file: str) -> None:
        """
        Saves the conversations to a JSON file
        """
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(self))

    def load(self, file: str) -> None:
        """
        Loads the conversations from a JSON file
        """
        with open(file, encoding="utf-8") as f:
            self.conversations = json.loads(f.read())
