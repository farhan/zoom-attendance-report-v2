"""
Data models for representing meeting and participant information.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Participant:
    """Represents a participant in a meeting."""
    name: str
    email: Optional[str]
    join_time: datetime
    leave_time: datetime
    duration_minutes: int
    is_guest: bool
    is_host: bool


@dataclass
class Meeting:
    """Represents a Zoom meeting with its participants."""
    topic: str
    meeting_id: str
    host_name: str
    host_email: str
    start_time: datetime
    end_time: datetime
    total_participants: int
    duration_minutes: int
    participants: list[Participant]
    
    def get_unique_participants(self) -> set[str]:
        """
        Returns a set of unique participant identifiers.
        Uses email if available, otherwise uses name.
        """
        unique = set()
        for participant in self.participants:
            identifier = participant.email if participant.email else participant.name
            # Skip bot participants
            if 'textalize' not in identifier.lower() and 'bot@' not in identifier.lower():
                unique.add(identifier)
        return unique

