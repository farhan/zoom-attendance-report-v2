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

## Prerequisites

### Getting Zoom Meeting Data

Before using this tool, you need to download your Zoom meeting attendance reports:

1. Go to [Zoom Reports](https://zoom.us/account/report/meeting) in your Zoom account
2. Navigate to **Reports** → **Usage Reports** → **Meeting**
3. Select the date range for your meetings
4. Click on a meeting and select **Generate Report** or **Participants Report**
5. Download the CSV file (format: `meetinglistdetails_YYYY_MM_DD_YYYY_MM_DD.csv`)
6. Place the downloaded CSV file(s) in your input folder

> **Note:** You need admin or owner privileges to access meeting reports in Zoom.

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file to specify your input folder:

```bash
# Create .env file and set INPUT_FOLDER_PATH to your actual data folder
echo "INPUT_FOLDER_PATH=input" > .env
```

## Usage

1. Place your Zoom attendance CSV file(s) in your desired folder (e.g., `input/`)
2. (Optional) Set the input folder path in `.env` file using `INPUT_FOLDER_PATH` variable
   - If not set, defaults to `sample-input/` folder
3. Run the script:

```bash
python main.py
```

4. The script will process all CSV files in the input folder and generate reports in the `output/` directory:
   - Each CSV file will create its own report folder named `{month}_{year}_report/`
   - Inside each folder:
     - `attendance_report_{month}_{year}.xlsx` - Excel file with two sheets:
       - **Individual Attendance**: Sorted list of all participants with their attendance percentages
       - **Team Summary**: Overall team statistics
     - `attendance_report_{month}_{year}_individual.csv` - Individual attendance data in CSV format
     - `attendance_report_{month}_{year}_team.csv` - Team summary in CSV format

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

### Input Folder Configuration

You can specify the input folder in two ways:

1. **Using .env file (Recommended)**: Create a `.env` file and set:
   ```
   INPUT_FOLDER_PATH=input
   ```

2. **Direct modification**: Edit the `input_folder` variable in `main.py`:
   ```python
   input_folder = os.getenv('INPUT_FOLDER_PATH', 'sample-input')
   ```

If no `.env` file is found or `INPUT_FOLDER_PATH` is not set, the script defaults to the `sample-input/` directory which contains template files.

### Batch Processing

The script automatically processes all CSV files in the input folder. Each file will generate a separate report based on its filename. The filename format should be:
```
meetinglistdetails_YYYY_MM_DD_YYYY_MM_DD.csv
```
This will generate a report named `{month}_{year}_report/`

## Notes

- **Meeting Validation**: A meeting is only considered valid if at least 2 real participants attended
- Bot participants (e.g., Textalize AI, bot@textalize.ai) are automatically excluded from attendance calculations
- Participants are identified by email when available, otherwise by name
- Attendance percentage is calculated based on actual meetings attended vs. total meetings held
- Input files should be placed in the `input/` directory
- Generated reports will be saved in the `output/` directory

