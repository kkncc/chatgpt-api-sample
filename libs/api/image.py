"""
A simple wrapper for the official ChatGPT API
"""
import os
import openai
import tiktoken

from apps import app
from libs.api.conversation import Conversation
from libs.api.tokens import Tokens

ENGINE = os.environ.get("GPT_ENGINE") or app.config.get('GPT_ENGINE')
ENCODER = tiktoken.get_encoding("gpt2")


def get_max_tokens(prompt: str) -> int:
    """
    Get the max tokens for a prompt
    """
    return 4000 - len(ENCODER.encode(prompt))


class ImageBot:
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
        self.prompt = ImagePrompt(buffer=buffer)
        self.engine = engine or ENGINE
        self.token = Tokens()

    def _get_completion(
        self,
        prompt: str,
    ):
        """
        Get the completion function
        """
        return openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )

    def _process_completion(
        self,
        user_request: str,
        completion: dict,
        conversation_id: str = None,
    ) -> dict:
        if completion.get("data") is None:
            raise Exception("ChatGPT API returned no data")
        if len(completion["data"]) == 0:
            raise Exception("ChatGPT API returned no data")
        if completion["data"][0].get("url") is None:
            raise Exception("ChatGPT API returned no url")
        # Add to chat history
        self.prompt.add_to_history(
            user_request,
        )
        if conversation_id is not None:
            self.save_conversation(conversation_id)
        return completion

    def ask(
        self,
        user_request: str,
        conversation_id: str = None,
    ) -> dict:
        """
        Send a request to ChatGPT and return the response
        """
        if conversation_id is not None:
            self.load_conversation(conversation_id)
        completion = self._get_completion(
            self.prompt.construct_prompt(user_request),
        )
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


class ImagePrompt:
    """
    Prompt class with methods to construct prompt
    """

    def __init__(self, buffer: int = None) -> None:
        """
        Initialize prompt with base prompt
        """
        self.base_prompt = (
            os.environ.get("CUSTOM_BASE_PROMPT")
            or "The following is a image generation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
            + "\n"
        )
        # Track chat history
        self.chat_history: list = []
        self.buffer = buffer

    def add_to_chat_history(self, chat: str) -> None:
        """
        Add chat to chat history for next prompt
        """
        self.chat_history.append(chat)

    def add_to_history(
        self,
        user_request: str,
    ) -> None:
        """
        Add request/response to chat history for next prompt
        """
        self.add_to_chat_history(
            user_request
            + "\n",
        )

    def history(self, custom_history: list = None) -> str:
        """
        Return chat history
        """
        return "\n".join(custom_history or self.chat_history)

    def construct_prompt(
        self,
        new_prompt: str,
        custom_history: list = None,
    ) -> str:
        """
        Construct prompt based on chat history and request
        """
        prompt = (
            self.base_prompt
            + self.history(custom_history=custom_history)
            + new_prompt
            + "\n"
        )
        # Check if prompt over 4000*4 characters
        if self.buffer is not None:
            max_tokens = 4000 - self.buffer
        else:
            max_tokens = 3200
        if len(ENCODER.encode(prompt)) > max_tokens:
            # Remove oldest chat
            if len(self.chat_history) == 0:
                return prompt
            self.chat_history.pop(0)
            # Construct prompt again
            prompt = self.construct_prompt(new_prompt, custom_history)
        return prompt
