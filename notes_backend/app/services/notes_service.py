"""Notes service module: contains in-memory storage and business logic for notes."""
from __future__ import annotations

import threading
import time
from typing import Dict, List, Optional


class NotesService:
    """Service layer managing in-memory notes.

    Notes are stored in a thread-safe in-memory dictionary keyed by ID.
    Each note is a dict with: id, title, content, created_at, updated_at.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._notes: Dict[int, Dict] = {}
        self._next_id: int = 1

    def _now_ts(self) -> float:
        """Return current epoch timestamp in seconds with fraction."""
        return time.time()

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Dict]:
        """Return a list of all notes sorted by updated_at descending."""
        with self._lock:
            return sorted(self._notes.values(), key=lambda n: n["updated_at"], reverse=True)

    # PUBLIC_INTERFACE
    def create_note(self, title: str, content: str) -> Dict:
        """Create a new note and return it."""
        now = self._now_ts()
        with self._lock:
            note_id = self._next_id
            self._next_id += 1
            note = {
                "id": note_id,
                "title": title,
                "content": content,
                "created_at": now,
                "updated_at": now,
            }
            self._notes[note_id] = note
            return note

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a single note by id or None if not found."""
        with self._lock:
            return self._notes.get(note_id)

    # PUBLIC_INTERFACE
    def update_note(self, note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Dict]:
        """Update an existing note's title and/or content. Returns updated note or None if not found."""
        with self._lock:
            note = self._notes.get(note_id)
            if not note:
                return None
            if title is not None:
                note["title"] = title
            if content is not None:
                note["content"] = content
            note["updated_at"] = self._now_ts()
            return note

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by id. Returns True if deleted, False if not found."""
        with self._lock:
            return self._notes.pop(note_id, None) is not None


# A singleton service instance for app-wide use
notes_service = NotesService()
