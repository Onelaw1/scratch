"""
Test Job Report Generator
Verifies the job analysis report generation functionality.
"""
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.job_report_generator import JobReportGenerator


def test_job_report_generator():
    """Test the job report generator"""
    print("Testing Job Report Generator...")
    
    # Initialize generator
    generator = JobReportGenerator()
    
    # Generate full report
    print("\n1. Generating full job analysis report...")
    try:
        output_path = generator.generate_full_report(
            filename="test_job_analysis_report.pptx",
            language="ko"
        )
        print(f"   Report generated: {output_path}")
        
        if os.path.exists(output_path):
            print("   SUCCESS: File exists.")
            file_size = os.path.getsize(output_path)
            print(f"   File size: {file_size:,} bytes")
        else:
            print("   FAILURE: File not created.")
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    generator.close()
    print("\nTest complete!")


if __name__ == "__main__":
    test_job_report_generator()
