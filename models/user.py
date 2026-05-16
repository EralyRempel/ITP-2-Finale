class User:
    """Represents a Telegram user in a consultation session."""

    def __init__(self, telegram_id: int, username: str = None, full_name: str = None):
        self.telegram_id = telegram_id
        self.username = username or "Unknown"
        self.full_name = full_name or "Unknown"

    def to_dict(self) -> dict:
        """Serialize user data to dictionary."""
        return {
            "telegram_id": self.telegram_id,
            "username": self.username,
            "full_name": self.full_name,
        }

    def __repr__(self):
        return f"User(id={self.telegram_id}, name={self.full_name})"
