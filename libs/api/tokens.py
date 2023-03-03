from apps import GLOBAL_REDIS_CLIENT


class Tokens:
    """
    For handling multiple tokens
    """
    def add_token(self, key: str, token: int) -> None:
        """
        Adds a history list to the conversations dict with the id as the key
        """
        GLOBAL_REDIS_CLIENT.hset("tokens", key, token)

    def get_token(self, key: str) -> int:
        """
        Retrieves the history list from the conversations dict with the id as the key
        """
        token = GLOBAL_REDIS_CLIENT.hget("tokens", key)
        if not token:
            token = 0
        return int(token)

    def remove_token(self, key: str) -> None:
        """
        Removes the history list from the conversations dict with the id as the key
        """
        GLOBAL_REDIS_CLIENT.hdel("tokens", key)
