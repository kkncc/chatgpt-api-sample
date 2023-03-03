"""
A simple wrapper for the official ChatGPT API
"""
import os
import openai

from apps import app
from libs.api.conversation import Conversation

ENGINE = os.environ.get("GPT_ENGINE") or app.config.get('GPT_ENGINE')


class ChatBot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        api_key: str = None,
        buffer: int = None,
        engine: str = None,
        proxy: str = None,
    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        openai.api_key = api_key or os.environ.get("OPENAI_API_KEY") or app.config.get("OPENAI_API_KEY")
        openai.proxy = proxy or os.environ.get("OPENAI_API_PROXY")
        self.conversations = Conversation()
        self.prompt = Prompt(buffer=buffer)
        self.engine = engine or ENGINE

    def _get_completion(
        self,
        prompt: list,
        temperature: float = 0.5,
        stream: bool = False,
    ):
        """
        Get the completion function
        """
        return openai.ChatCompletion.create(
            model=self.engine,
            messages=prompt,
            temperature=temperature,
            top_p=1,
            presence_penalty=0.6,
            stream=stream,
        )

    def _process_completion(
        self,
        user_request: str,
        completion: dict,
        conversation_id: str = None,
    ) -> dict:
        if completion.get("choices") is None:
            raise Exception("ChatGPT API returned no choices")
        if len(completion["choices"]) == 0:
            raise Exception("ChatGPT API returned no choices")
        if completion["choices"][0].get("message") is None:
            raise Exception("ChatGPT API returned no message")
        # Add to chat history
        self.prompt.add_to_history(
            user_request,
            completion["choices"][0]["message"],
        )
        if conversation_id is not None:
            self.save_conversation(conversation_id)
        return completion

    def ask(
        self,
        user_request: str,
        temperature: float = 0.5,
        conversation_id: str = None,
    ) -> dict:
        """
        Send a request to ChatGPT and return the response
        """
        if conversation_id is not None:
            self.load_conversation(conversation_id)
        completion = self._get_completion(
            self.prompt.construct_prompt(user_request),
            temperature,
        )
        print(123123)
        return self._process_completion(user_request, completion, conversation_id=conversation_id)

    def make_conversation(self, conversation_id: str) -> None:
        """
        Make a conversation
        """
        self.conversations.add_conversation(conversation_id, [])

    def rollback(self, num: int) -> None:
        """
        Rollback chat history num times
        """
        for _ in range(num):
            self.prompt.chat_history.pop()

    def reset(self) -> None:
        """
        Reset chat history
        """
        self.prompt.chat_history = []

    def load_conversation(self, conversation_id) -> None:
        """
        Load a conversation from the conversation history
        """
        if not self.conversations.check_conversation(conversation_id):
            # Create a new conversation
            self.make_conversation(conversation_id)
        self.prompt.chat_history = self.conversations.get_conversation(conversation_id)

    def save_conversation(self, conversation_id) -> None:
        """
        Save a conversation to the conversation history
        """
        self.conversations.add_conversation(conversation_id, self.prompt.chat_history)


class Prompt:
    """
    Prompt class with methods to construct prompt
    """

    def __init__(self, buffer: int = None) -> None:
        """
        Initialize prompt with base prompt
        """
        self.base_prompt = [
            {"role": "system", "content": os.environ.get("CUSTOM_BASE_PROMPT") or "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."}
        ]
        # Track chat history
        self.chat_history: list = []
        self.buffer = buffer

    def add_to_chat_history(self, user_request: str, response: map) -> None:
        """
        Add chat to chat history for next prompt
        """
        chat_user = {
            "role": "user", "content": user_request,
        }
        self.chat_history.append(chat_user)
        self.chat_history.append(response)

    def add_to_history(
        self,
        user_request: str,
        response: map,
    ) -> None:
        """
        Add request/response to chat history for next prompt
        """
        self.add_to_chat_history(user_request, response)

    def history(self, custom_history: list = None):
        """
        Return chat history
        """
        return custom_history or self.chat_history

    def construct_prompt(
        self,
        new_prompt: str,
        custom_history: list = None,
    ) -> list:
        """
        Construct prompt based on chat history and request
        """
        prompt = self.base_prompt + self.history(custom_history=custom_history)
        chat_user = {
            "role": "user", "content": new_prompt
        }
        prompt.append(chat_user)
        return prompt
