"""Run this script ONCE locally to authenticate with Google Calendar.

Steps before running:
  1. Go to https://console.cloud.google.com/
  2. Create a project, enable "Google Calendar API"
  3. Configure the OAuth consent screen (External; add your gmail as test user).
  4. Create OAuth client credentials of type "Desktop app"
  5. Download credentials.json into this folder
  6. pip install -r requirements.txt
  7. python setup_google_auth.py

The script will open a browser, ask you to log in with leoshancx@gmail.com,
and create a token.json file. Then:

  cat token.json   # paste the contents as the GOOGLE_TOKEN_JSON secret in GitHub
"""
from __future__ import annotations

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main() -> None:
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    print("\n[+] token.json written.")
    print("[+] Copy its contents into the GOOGLE_TOKEN_JSON GitHub secret.")


if __name__ == "__main__":
    main()
