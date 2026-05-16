import json
import os
from models.consultation import Consultation


class Storage:
    """Handles reading and writing consultation data to a JSON file."""

    def __init__(self, filepath: str = "clients.json"):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        """Create the JSON file if it doesn't exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def save_consultation(self, consultation: Consultation):
        """Append a finished consultation record to the JSON file."""
        data = self._load_all()
        data.append(consultation.to_dict())
        self._write_all(data)

    def get_all(self) -> list[dict]:
        """Return all saved consultations."""
        return self._load_all()

    def _load_all(self) -> list[dict]:
        """Load all records from JSON file."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_all(self, data: list[dict]):
        """Write all records to JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
