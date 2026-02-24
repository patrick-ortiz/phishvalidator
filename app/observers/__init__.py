from abc import ABC, abstractmethod
import threading
import subprocess
import os

class CredentialObserver(ABC):
    """
    Abstract Observer class for the Observer pattern.
    Defines the method that should be called when a subject's state changes.
    """
    @abstractmethod
    def on_credential_captured(self, credential: dict) -> None:
        pass


class CredentialSubject:
    """
    Subject class for the Observer pattern.
    Keeps a list of observers and notifies them of state changes.
    """
    def __init__(self):
        self._observers = []

    def attach(self, observer: CredentialObserver) -> None:
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: CredentialObserver) -> None:
        """Detach an observer from the subject."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, credential: dict) -> None:
        """Notify all observers about an event."""
        for observer in self._observers:
            observer.on_credential_captured(credential)


class AutoValidatorObserver(CredentialObserver):
    """
    Concrete Observer that triggers a background validation process
    when a new credential is captured.
    """
    def on_credential_captured(self, credential: dict) -> None:
        # We start it in a background thread so the HTTP response is not blocked
        thread = threading.Thread(target=self._run_validator, daemon=True)
        thread.start()

    def _run_validator(self) -> None:
        """Internal method to execute the validator script."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        validator_path = os.path.join(base_dir, 'app/validator.py')
        try:
            subprocess.run(['python3', validator_path], check=False)
        except Exception as e:
            print(f"[Observer Error] Failed to start validator: {e}")

# Global instance to be imported by db.py and app.py
credential_subject = CredentialSubject()
