#!/usr/bin/env python3
"""
Open the generated visual report in the default browser
"""

import webbrowser
import os
from pathlib import Path

def main():
    # Get the path to the report
    base_path = Path(__file__).parent.parent
    report_path = base_path / "outputs" / "COMPREHENSIVE_WORKFLOW_REPORT.html"

    if not report_path.exists():
        print("❌ Report not found!")
        print(f"   Expected at: {report_path}")
        print("\n   Please run 'python run_realistic_workflow.py' first to generate the report.")
        return False

    # Convert to file URL
    file_url = f"file://{report_path.absolute()}"

    print("=" * 70)
    print("OPENING COMPREHENSIVE WORKFLOW REPORT")
    print("=" * 70)
    print(f"\nReport location: {report_path}")
    print(f"Report size: {report_path.stat().st_size:,} bytes")
    print(f"\nOpening in default browser...")

    # Open in browser
    webbrowser.open(file_url)

    print("✓ Report opened in browser")
    print("\nIf the browser didn't open, you can manually open:")
    print(f"  {file_url}")

    return True

if __name__ == "__main__":
    main()