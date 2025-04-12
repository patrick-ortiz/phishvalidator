import sqlite3
import random
import time
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"../creds.db"))

def simulate_login(email, password):
    """
    Simulates a login attempt and returns a state.
    This will later be replaced by Selenium/Playwright
    """
    print(f"[~] Simulating login for: {email}...")
    time.sleep(1)

    status = random.choice(["Success", "Fail", "MFA"])
    print(f"[+] Result: {status}")
    return status

def run_validator():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, email, password FROM credentials WHERE status = 'Pending'")
    rows = cursor.fetchall()

    if not rows:
        print("[i] THere are no pending credentials.")
        return

    for row in rows:
        cred_id, email, password = row
        status = simulate_login(email, password)

        cursor.execute("UPDATE credentials SET status = ? WHERE id = ?", (status, cred_id))
        conn.commit()

    conn.close()
    print ("[!] Validation completed.")

if __name__ == "__main__":
    run_validator()
