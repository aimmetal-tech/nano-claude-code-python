from claude.client import ClaudeClient
from claude.message import Message


class ChatModel(ClaudeClient):
    def __init__(self, model: str, messages: list[Message] = None, **kwargs):
        super().__init__(**kwargs)
        self.messages = messages or []
        self.model = model

    def chat(self, messages: list[Message]) -> str:
        """
        向 Claude API 发送聊天消息并返回响应。
        """
        url = f"{self.base_url}/v1/messages"
        body = {
            "model": self.model,
            "messages": messages,
        }
        response = self._session.post(
            url,
            json=body,
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]


if __name__ == "__main__":
    print("正在测试 ChatModel...")
    test_client = ChatModel(base_url="https://api.phsharp.com")
    print(f"api_key:{test_client.api_key},base_url:{test_client.base_url}")
    print(test_client.chat([{"role": "user", "content": "你好！"}]))
