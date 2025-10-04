# Zoom Attendance Report Generator

This Python application analyzes Zoom meeting attendance data and generates comprehensive reports showing individual and team attendance statistics.

## Features

- **Individual Attendance Reports**: Shows attendance percentage for each participant
- **Team Summary Statistics**: Provides overall team attendance metrics
- **Multiple Output Formats**: Generates both Excel (.xlsx) and CSV reports
- **Automated Bot Filtering**: Automatically excludes bot participants (like Textalize AI) from calculations
- **Object-Oriented Design**: Clean, modular code structure for easy maintenance

## Project Structure

```
.
├── main.py                     # Entry point script
├── models.py                   # Data models (Meeting, Participant)
├── csv_reader.py              # CSV parsing logic
├── attendance_calculator.py   # Attendance calculation logic
├── report_generator.py        # Report generation logic
├── requirements.txt           # Python dependencies
├── input/                     # Input CSV file(s)
│   └── meetinglistdetails_*.csv
└── output/                    # Generated reports
    ├── *.xlsx
    └── *.csv
```

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your Zoom attendance CSV file in the `input/` directory
2. Run the script:

```bash
python main.py
```

3. The script will generate reports in the `output/` directory:
   - `attendance_report_september_2025.xlsx` - Excel file with two sheets:
     - **Individual Attendance**: Sorted list of all participants with their attendance percentages
     - **Team Summary**: Overall team statistics
   - `attendance_report_september_2025_individual.csv` - Individual attendance data in CSV format
   - `attendance_report_september_2025_team.csv` - Team summary in CSV format

## CSV Input Format

The input CSV file should follow Zoom's meeting details export format:
- First row: Header row
- Subsequent rows: Grouped by meeting (separated by empty lines)
- Each row in a group represents one participant in that meeting

## Output Reports

### Individual Attendance Sheet
- **Name**: Participant's display name
- **Email**: Participant's email address
- **Meetings Attended**: Number of meetings the participant attended
- **Total Meetings**: Total number of meetings in the period
- **Attendance %**: Percentage of meetings attended

### Team Summary Sheet
- **Total Meetings**: Number of meetings held
- **Total Unique Participants**: Number of unique participants across all meetings
- **Average Attendance %**: Average attendance percentage across all participants
- **Average Participants per Meeting**: Average number of participants per meeting

## Customization

To analyze a different CSV file, edit the `input_file` variable in `main.py`:

```python
input_file = 'input/your_file_name.csv'
```

To change the output filename, edit the `output_file` variable in `main.py`:

```python
output_file = 'output/your_report_name.xlsx'
```

## Notes

- **Meeting Validation**: A meeting is only considered valid if at least 2 real participants attended
- Bot participants (e.g., Textalize AI, bot@textalize.ai) are automatically excluded from attendance calculations
- Participants are identified by email when available, otherwise by name
- Attendance percentage is calculated based on actual meetings attended vs. total meetings held
- Input files should be placed in the `input/` directory
- Generated reports will be saved in the `output/` directory

