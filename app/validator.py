
import sqlite3
import os
from playwright.sync_api import sync_playwright

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../creds.db"))

def try_login(email, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", email)
        page.fill("#password", password)
        page.click("button[type='submit']")
        page.wait_for_timeout(1000)

        content = page.content()
        browser.close()

        if "You logged into a secure area!" in content:
            return "Success"
        elif "Your password is invalid!" in content or "Your username is invalid" in content:
            return "Fail"
        else:
            return "MFA"

def run_validator():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, email, password FROM credentials WHERE status = 'Pending'")
    rows = cursor.fetchall()

    if not rows:
        print("[i] No pending credentials.")
        return

    for cred_id, email, password in rows:
        print(f"[~] Validating {email}:{password}")
        try:
            status = try_login(email, password)
        except Exception as e:
            print(f"[!] Error during validation: {e}")
            status = "Error"
        cursor.execute("UPDATE credentials SET status = ? WHERE id = ?", (status, cred_id))
        conn.commit()

    conn.close()
    print("[✓] Validation complete.")

if __name__ == "__main__":
    run_validator()

