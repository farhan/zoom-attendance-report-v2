"""
Main script to process Zoom attendance data and generate reports.
"""
import sys
import os
from csv_reader import ZoomCSVReader
from attendance_calculator import AttendanceCalculator
from report_generator import ReportGenerator


def main():
    """
    Main function to process Zoom attendance CSV and generate reports.
    """
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Input CSV file - use environment variable if available, otherwise use template
    input_file = os.getenv('INPUT_FILE_PATH', 'sample-input/meetinglistdetails_template.csv')
    
    # Output report file (Excel format)
    output_file = 'output/september_2025_report/attendance_report_september_2025.xlsx'
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print("=" * 60)
    print("Zoom Attendance Report Generator")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Read CSV file
        print(f"📖 Reading data from: {input_file}")
        reader = ZoomCSVReader(input_file)
        meetings = reader.read_meetings()
        print(f"✓ Successfully parsed {len(meetings)} meetings")
        print()
        
        # Step 2: Calculate attendance statistics
        print("📊 Calculating attendance statistics...")
        calculator = AttendanceCalculator(meetings)
        individual_stats = calculator.calculate_individual_attendance()
        team_stats = calculator.calculate_team_attendance()
        print(f"✓ Calculated statistics for {len(individual_stats)} participants")
        print()
        
        # Step 3: Display summary
        print("📈 Team Summary:")
        print(f"  - Total Meetings: {team_stats['total_meetings']}")
        print(f"  - Total Unique Participants: {team_stats['total_unique_participants']}")
        print(f"  - Average Attendance: {team_stats['average_attendance_percentage']}%")
        print(f"  - Avg Participants per Meeting: {team_stats['average_participants_per_meeting']}")
        print()
        
        # Step 4: Generate report
        print(f"📝 Generating report: {output_file}")
        report_generator = ReportGenerator(output_file)
        report_generator.generate_report(individual_stats, team_stats)
        print()
        
        # Optional: Also generate CSV reports
        print("📝 Generating CSV reports...")
        report_generator.generate_csv_report(individual_stats, team_stats)
        print()
        
        print("=" * 60)
        print("✅ Report generation completed successfully!")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        print("Please ensure the CSV file is in the same directory as this script.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

