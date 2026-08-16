import os
import sys
import subprocess
import time
from config.config import Config

def clean_html_report(report_path):
    """Sanitizes generated HTML report to remove legacy CSS comments and invalid @charset rules."""
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('<style type="text/css"><!--', '<style>')
        content = content.replace('-->\n</style>', '</style>')
        content = content.replace('--></style>', '</style>')
        content = content.replace('@charset "utf-8";', '')
        for empty_rule in [".passed{}", ".failed{}", ".error{}", ".skipped{}", ".undefined{}", ".summary{}", ".failed_scenarios{}", ".footer{}"]:
            content = content.replace(empty_rule, "")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)

def main():
    """Runs Behave test suite and generates HTML reports."""
    print("=" * 60)
    print(" Booking.com Test Automation Suite - Executive Test Runner ")
    print("=" * 60)

    Config.ensure_directories()
    html_report_path = os.path.join(Config.REPORTS_DIR, "report.html")
    allure_results_dir = os.path.join(Config.REPORTS_DIR, "allure-results")
    
    os.makedirs(allure_results_dir, exist_ok=True)

    # Behave execution command
    cmd = [
        sys.executable, "-m", "behave",
        "-f", "html", "-o", html_report_path,
        "-f", "allure_behave.formatter:AllureFormatter", "-o", allure_results_dir,
        "-f", "pretty"
    ]

    # Additional CLI arguments passed to run_tests.py (e.g. tags)
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])

    print(f"\nExecuting Command: {' '.join(cmd)}\n")
    start_time = time.time()
    
    result = subprocess.run(cmd, cwd=Config.BASE_DIR)
    
    clean_html_report(html_report_path)
    
    duration = round(time.time() - start_time, 2)

    print("\n" + "=" * 60)
    print(f" Test Execution Completed in {duration}s ")
    print("=" * 60)
    print(f" HTML Report generated at: {html_report_path}")
    print(f" Allure Results generated at: {allure_results_dir}")
    print("=" * 60)
    print("To view Allure report locally (if Allure CLI installed):")
    print(f"   allure serve {allure_results_dir}")
    print("=" * 60 + "\n")

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
