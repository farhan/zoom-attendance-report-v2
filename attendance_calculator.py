"""
Attendance calculator for computing individual and team attendance metrics.
"""
from typing import List, Dict
from collections import defaultdict
from models import Meeting


class AttendanceCalculator:
    """Calculates attendance statistics from meeting data."""
    
    def __init__(self, meetings: List[Meeting]):
        self.meetings = meetings
    
    def calculate_individual_attendance(self) -> Dict[str, dict]:
        """
        Calculates attendance percentage for each participant.
        
        Returns:
            Dictionary mapping participant identifier to attendance data:
            {
                'participant_name/email': {
                    'name': str,
                    'email': str or None,
                    'meetings_attended': int,
                    'total_meetings': int,
                    'attendance_percentage': float
                }
            }
        """
        # Count total meetings (excluding meetings with only bots)
        total_meetings = self._count_real_meetings()
        
        # Track attendance for each participant
        participant_attendance = defaultdict(lambda: {
            'name': '',
            'email': None,
            'meetings_attended': 0,
            'total_meetings': total_meetings
        })
        
        for meeting in self.meetings:
            # Get unique participants in this meeting (excluding bots)
            unique_participants = meeting.get_unique_participants()
            
            # Only count this meeting if it has at least 2 real participants
            if len(unique_participants) >= 2:
                for participant in meeting.participants:
                    identifier = participant.email if participant.email else participant.name
                    
                    # Skip bot participants
                    if self._is_bot(identifier):
                        continue
                    
                    # Update attendance record
                    if not participant_attendance[identifier]['name']:
                        participant_attendance[identifier]['name'] = participant.name
                        participant_attendance[identifier]['email'] = participant.email
                    
                    # Only count once per meeting (in case participant appears multiple times)
                    if identifier in unique_participants:
                        participant_attendance[identifier]['meetings_attended'] += 1
                        # Remove from set so we don't count again
                        unique_participants.remove(identifier)
        
        # Calculate percentages
        for identifier, data in participant_attendance.items():
            attended = data['meetings_attended']
            total = data['total_meetings']
            data['attendance_percentage'] = round((attended / total * 100) if total > 0 else 0, 2)
        
        return dict(participant_attendance)
    
    def calculate_team_attendance(self) -> dict:
        """
        Calculates overall team attendance statistics.
        
        Returns:
            Dictionary with team-level metrics:
            {
                'total_meetings': int,
                'total_participants': int (unique),
                'average_attendance_percentage': float,
                'average_participants_per_meeting': float
            }
        """
        individual_stats = self.calculate_individual_attendance()
        
        total_meetings = self._count_real_meetings()
        total_unique_participants = len(individual_stats)
        
        # Calculate average attendance percentage
        if individual_stats:
            avg_attendance = sum(
                data['attendance_percentage'] for data in individual_stats.values()
            ) / len(individual_stats)
        else:
            avg_attendance = 0
        
        # Calculate average participants per meeting (only count meetings with 2+ participants)
        total_participant_count = sum(
            len(meeting.get_unique_participants()) for meeting in self.meetings
            if len(meeting.get_unique_participants()) >= 2
        )
        avg_participants = total_participant_count / total_meetings if total_meetings > 0 else 0
        
        return {
            'total_meetings': total_meetings,
            'total_unique_participants': total_unique_participants,
            'average_attendance_percentage': round(avg_attendance, 2),
            'average_participants_per_meeting': round(avg_participants, 2)
        }
    
    def _count_real_meetings(self) -> int:
        """
        Counts meetings that have at least 2 real participants (not just bots).
        """
        count = 0
        for meeting in self.meetings:
            unique_participants = meeting.get_unique_participants()
            if len(unique_participants) >= 2:
                count += 1
        return count
    
    def _is_bot(self, identifier: str) -> bool:
        """Checks if an identifier belongs to a bot."""
        identifier_lower = identifier.lower()
        return 'textalize' in identifier_lower or 'bot@' in identifier_lower

