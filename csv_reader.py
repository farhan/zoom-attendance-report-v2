"""
CSV Reader for parsing Zoom meeting attendance data.
"""
import csv
from datetime import datetime
from typing import List
from models import Meeting, Participant


class ZoomCSVReader:
    """Reads and parses Zoom meeting attendance CSV files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read_meetings(self) -> List[Meeting]:
        """
        Reads the CSV file and returns a list of Meeting objects.
        Groups rows by empty lines to identify separate meetings.
        """
        meetings = []
        current_meeting_rows = []
        
        # First, read all lines to identify empty lines
        with open(self.file_path, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        
        # Parse CSV manually to handle empty lines
        reader = csv.DictReader(lines)
        header = reader.fieldnames
        
        for i, line in enumerate(lines[1:], start=1):  # Skip header
            # Check if line is truly empty or just whitespace
            if line.strip() == '':
                # Empty line found - process accumulated rows
                if current_meeting_rows:
                    meeting = self._parse_meeting(current_meeting_rows)
                    if meeting:
                        meetings.append(meeting)
                    current_meeting_rows = []
            else:
                # Parse the line as CSV
                row_reader = csv.DictReader([','.join(header)] + [line])
                for row in row_reader:
                    current_meeting_rows.append(row)
        
        # Don't forget the last meeting if file doesn't end with empty line
        if current_meeting_rows:
            meeting = self._parse_meeting(current_meeting_rows)
            if meeting:
                meetings.append(meeting)
        
        return meetings
    
    def _is_empty_row(self, row: dict) -> bool:
        """Checks if a row is empty."""
        return all(value.strip() == '' for value in row.values())
    
    def _parse_meeting(self, rows: List[dict]) -> Meeting:
        """Parses a group of rows into a Meeting object."""
        if not rows:
            return None
        
        # First row contains meeting-level information
        first_row = rows[0]
        
        # Parse participants from all rows
        participants = []
        for row in rows:
            participant = self._parse_participant(row)
            if participant:
                participants.append(participant)
        
        # Create meeting object
        meeting = Meeting(
            topic=first_row['Topic'],
            meeting_id=first_row['ID'].replace(' ', ''),
            host_name=first_row['Host name'],
            host_email=first_row['Host email'],
            start_time=self._parse_datetime(first_row['Start time']),
            end_time=self._parse_datetime(first_row['End time']),
            total_participants=int(first_row['Participants']),
            duration_minutes=int(first_row['Duration (minutes)']),
            participants=participants
        )
        
        return meeting
    
    def _parse_participant(self, row: dict) -> Participant:
        """Parses a row into a Participant object."""
        name = row['Name (original name)']
        if not name:
            return None
        
        # Determine if this is the host
        is_host = '(Host)' in name or '(host)' in name.lower()
        
        # Parse guest status
        is_guest = row['Guest'].strip().lower() == 'yes'
        
        participant = Participant(
            name=name,
            email=row['Email'].strip() if row['Email'].strip() else None,
            join_time=self._parse_datetime(row['Join time']),
            leave_time=self._parse_datetime(row['Leave time']),
            duration_minutes=int(row['Duration (minutes)']) if row['Duration (minutes)'] else 0,
            is_guest=is_guest,
            is_host=is_host
        )
        
        return participant
    
    def _parse_datetime(self, date_str: str) -> datetime:
        """Parses datetime string in format: MM/DD/YYYY HH:MM:SS AM/PM"""
        return datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')

