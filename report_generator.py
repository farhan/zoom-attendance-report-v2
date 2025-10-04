"""
Report generator for creating attendance reports in Excel format.
"""
import pandas as pd
from typing import Dict
from datetime import datetime


class ReportGenerator:
    """Generates attendance reports in Excel format."""
    
    def __init__(self, output_filename: str = None):
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'attendance_report_{timestamp}.xlsx'
        self.output_filename = output_filename
    
    def generate_report(self, individual_stats: Dict[str, dict], team_stats: dict):
        """
        Generates an Excel report with individual and team attendance data.
        
        Args:
            individual_stats: Dictionary of individual attendance statistics
            team_stats: Dictionary of team-level statistics
        """
        # Create Excel writer
        with pd.ExcelWriter(self.output_filename, engine='openpyxl') as writer:
            # Generate individual attendance sheet
            self._create_individual_sheet(writer, individual_stats)
            
            # Generate team summary sheet
            self._create_team_sheet(writer, team_stats)
        
        print(f"Report generated successfully: {self.output_filename}")
    
    def _create_individual_sheet(self, writer, individual_stats: Dict[str, dict]):
        """Creates a sheet with individual attendance data."""
        # Prepare data for DataFrame
        data = []
        for identifier, stats in individual_stats.items():
            data.append({
                'Name': stats['name'],
                'Email': stats['email'] if stats['email'] else 'N/A',
                'Meetings Attended': stats['meetings_attended'],
                'Total Meetings': stats['total_meetings'],
                'Attendance %': stats['attendance_percentage']
            })
        
        # Sort by attendance percentage (descending)
        data.sort(key=lambda x: x['Attendance %'], reverse=True)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Write to Excel
        df.to_excel(writer, sheet_name='Individual Attendance', index=False)
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Individual Attendance']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).map(len).max(),
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length
    
    def _create_team_sheet(self, writer, team_stats: dict):
        """Creates a sheet with team-level statistics."""
        # Prepare data for DataFrame
        data = [
            {'Metric': 'Total Meetings', 'Value': team_stats['total_meetings']},
            {'Metric': 'Total Unique Participants', 'Value': team_stats['total_unique_participants']},
            {'Metric': 'Average Attendance %', 'Value': f"{team_stats['average_attendance_percentage']}%"},
            {'Metric': 'Average Participants per Meeting', 'Value': team_stats['average_participants_per_meeting']}
        ]
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Write to Excel
        df.to_excel(writer, sheet_name='Team Summary', index=False)
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Team Summary']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).map(len).max(),
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length
    
    def generate_csv_report(self, individual_stats: Dict[str, dict], team_stats: dict):
        """
        Generates CSV reports (separate files for individual and team data).
        
        Args:
            individual_stats: Dictionary of individual attendance statistics
            team_stats: Dictionary of team-level statistics
        """
        # Generate individual attendance CSV
        individual_data = []
        for identifier, stats in individual_stats.items():
            individual_data.append({
                'Name': stats['name'],
                'Email': stats['email'] if stats['email'] else 'N/A',
                'Meetings Attended': stats['meetings_attended'],
                'Total Meetings': stats['total_meetings'],
                'Attendance %': stats['attendance_percentage']
            })
        
        individual_data.sort(key=lambda x: x['Attendance %'], reverse=True)
        df_individual = pd.DataFrame(individual_data)
        individual_csv = self.output_filename.replace('.xlsx', '_individual.csv')
        df_individual.to_csv(individual_csv, index=False)
        
        # Generate team summary CSV
        team_data = [
            {'Metric': 'Total Meetings', 'Value': team_stats['total_meetings']},
            {'Metric': 'Total Unique Participants', 'Value': team_stats['total_unique_participants']},
            {'Metric': 'Average Attendance %', 'Value': f"{team_stats['average_attendance_percentage']}%"},
            {'Metric': 'Average Participants per Meeting', 'Value': team_stats['average_participants_per_meeting']}
        ]
        
        df_team = pd.DataFrame(team_data)
        team_csv = self.output_filename.replace('.xlsx', '_team.csv')
        df_team.to_csv(team_csv, index=False)
        
        print(f"CSV reports generated: {individual_csv}, {team_csv}")

