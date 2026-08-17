import os

class Config:
    """Central configuration for Booking.com Automation Testing Framework."""
    
    BASE_URL = "https://www.booking.com"
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"  # Default to visible browser UI
    DEFAULT_TIMEOUT = 15  # Explicit wait default timeout in seconds
    PAGE_LOAD_TIMEOUT = 30
    
    # Directory paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")
    SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")

    @classmethod
    def ensure_directories(cls):
        """Ensure report, screenshot, and log directories exist."""
        for path in [cls.REPORTS_DIR, cls.SCREENSHOTS_DIR, cls.LOGS_DIR]:
            os.makedirs(path, exist_ok=True)

Config.ensure_directories()
