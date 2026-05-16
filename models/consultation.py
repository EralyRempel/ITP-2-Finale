from datetime import datetime
from models.user import User


class Consultation:
    """Manages a single consultation session for a user."""

    def __init__(self, user: User):
        self.user = user
        self.history: list[dict] = []  # [{"role": "user"/"assistant", "content": "..."}]
        self.started_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_finished: bool = False

    def add_message(self, role: str, content: str):
        """Add a message to consultation history."""
        self.history.append({"role": role, "content": content})

    def get_history(self) -> list[dict]:
        """Return full message history."""
        return self.history

    def finish(self):
        """Mark consultation as finished."""
        self.is_finished = True

    def summarize(self) -> str:
        """Generate a short summary of the consultation for the manager."""
        user_messages = [
            msg["content"]
            for msg in self.history
            if msg["role"] == "user"
        ]
        summary = " | ".join(user_messages[:5])  # first 5 user messages
        return summary[:300]  # limit length

    def to_dict(self) -> dict:
        """Serialize consultation data to dictionary for storage."""
        return {
            "user": self.user.to_dict(),
            "started_at": self.started_at,
            "finished_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": self.summarize(),
            "message_count": len(self.history),
        }

    def __repr__(self):
        return f"Consultation(user={self.user}, messages={len(self.history)})"
