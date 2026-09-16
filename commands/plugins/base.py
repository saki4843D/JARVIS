class BasePlugin:
    """
    Base class for all Jarvis plugins.
    """

    def can_handle(self, command: str) -> bool:
        raise NotImplementedError

    def handle(self, command: str):
        raise NotImplementedError