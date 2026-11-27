"""Run ONCE on your own computer to get a Drive refresh token.
  pip install google-auth-oauthlib
  python tools/get_refresh_token.py client_secret.json
Opens a browser, you approve, it prints GDRIVE_CLIENT_ID / SECRET / REFRESH_TOKEN to paste into GitHub secrets.
"""
import json, sys
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], ["https://www.googleapis.com/auth/drive.file"])
c = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nGDRIVE_CLIENT_ID     =", c.client_id)
print("GDRIVE_CLIENT_SECRET =", c.client_secret)
print("GDRIVE_REFRESH_TOKEN =", c.refresh_token)
