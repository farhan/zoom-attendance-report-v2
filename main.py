"""
Main script to process Zoom attendance data and generate reports.
"""
import sys
import os
import glob
from csv_reader import ZoomCSVReader
from attendance_calculator import AttendanceCalculator
from report_generator import ReportGenerator


def process_csv_file(input_file: str, output_base_dir: str = 'output'):
    """
    Process a single CSV file and generate reports.
    
    Args:
        input_file: Path to the input CSV file
        output_base_dir: Base directory for output files
    """
    try:
        # Extract date range from filename (e.g., meetinglistdetails_2025_06_01_2025_06_30.csv)
        filename = os.path.basename(input_file)
        if filename.startswith('meetinglistdetails_'):
            # Extract date components from filename
            parts = filename.replace('meetinglistdetails_', '').replace('.csv', '').split('_')
            if len(parts) == 6:
                # Format: YYYY_MM_DD_YYYY_MM_DD
                year = parts[0]
                month = parts[1]
                month_names = {
                    '01': 'january', '02': 'february', '03': 'march',
                    '04': 'april', '05': 'may', '06': 'june',
                    '07': 'july', '08': 'august', '09': 'september',
                    '10': 'october', '11': 'november', '12': 'december'
                }
                month_name = month_names.get(month, month)
                report_name = f"{month_name}_{year}"
            else:
                report_name = filename.replace('.csv', '')
        else:
            report_name = filename.replace('.csv', '')
        
        # Create output directory for this report
        output_dir = os.path.join(output_base_dir, f"{report_name}_report")
        os.makedirs(output_dir, exist_ok=True)
        
        # Output report file (Excel format)
        output_file = os.path.join(output_dir, f"attendance_report_{report_name}.xlsx")
        
        print(f"\n{'=' * 60}")
        print(f"Processing: {filename}")
        print(f"{'=' * 60}")
        
        # Step 1: Read CSV file
        print(f"📖 Reading data from: {input_file}")
        reader = ZoomCSVReader(input_file)
        meetings = reader.read_meetings()
        print(f"✓ Successfully parsed {len(meetings)} meetings")
        
        # Step 2: Calculate attendance statistics
        print("📊 Calculating attendance statistics...")
        calculator = AttendanceCalculator(meetings)
        individual_stats = calculator.calculate_individual_attendance()
        team_stats = calculator.calculate_team_attendance()
        print(f"✓ Calculated statistics for {len(individual_stats)} participants")
        
        # Step 3: Display summary
        print("📈 Team Summary:")
        print(f"  - Total Meetings: {team_stats['total_meetings']}")
        print(f"  - Total Unique Participants: {team_stats['total_unique_participants']}")
        print(f"  - Average Attendance: {team_stats['average_attendance_percentage']}%")
        print(f"  - Avg Participants per Meeting: {team_stats['average_participants_per_meeting']}")
        
        # Step 4: Generate report
        print(f"📝 Generating report: {output_file}")
        report_generator = ReportGenerator(output_file)
        report_generator.generate_report(individual_stats, team_stats)
        
        # Step 5: Also generate CSV reports
        print("📝 Generating CSV reports...")
        report_generator.generate_csv_report(individual_stats, team_stats)
        
        print(f"✅ Report generated successfully: {report_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {input_file}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    Main function to process all Zoom attendance CSV files from a folder.
    """
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Input folder - use environment variable if available, otherwise use sample-input
    input_folder = os.getenv('INPUT_FOLDER_PATH', 'sample-input')
    
    # Ensure folder path doesn't have trailing slash for consistency
    input_folder = input_folder.rstrip('/')
    
    print("=" * 60)
    print("Zoom Attendance Report Generator")
    print("=" * 60)
    print(f"\nScanning folder: {input_folder}")
    
    # Get all CSV files from the input folder
    csv_files = glob.glob(os.path.join(input_folder, '*.csv'))
    
    if not csv_files:
        print(f"❌ Error: No CSV files found in '{input_folder}'")
        sys.exit(1)
    
    print(f"Found {len(csv_files)} CSV file(s) to process\n")
    
    # Process each CSV file
    success_count = 0
    failed_count = 0
    
    for csv_file in sorted(csv_files):
        if process_csv_file(csv_file):
            success_count += 1
        else:
            failed_count += 1
    
    # Final summary
    print(f"\n{'=' * 60}")
    print("Processing Complete")
    print(f"{'=' * 60}")
    print(f"✅ Successfully processed: {success_count} file(s)")
    if failed_count > 0:
        print(f"❌ Failed: {failed_count} file(s)")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()

