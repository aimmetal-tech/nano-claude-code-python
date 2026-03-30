from typing import TypedDict

CLAUDE_MESSAGE_ROLE_USER = "user"
CLAUDE_MESSAGE_ROLE_ASSISTANT = "assistant"


class Message(TypedDict):
    role: str
    content: str


class MessageManager:
    def __init__(self):
        self.history: list[dict[str, str]] = []

    def add_user_message(self, content: str):
        self.history.append({"role": CLAUDE_MESSAGE_ROLE_USER, "content": content})

    def add_assistant_message(self, content: str):
        self.history.append({"role": CLAUDE_MESSAGE_ROLE_ASSISTANT, "content": content})

    def get_history(self) -> list[dict[str, str]]:
        return self.history
