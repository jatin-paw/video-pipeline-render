"""Step 4: upload the finished mp4 straight to a Google Drive folder.

Auth: OAuth refresh token (works with a normal My Drive folder) or a service account
(only works inside a Shared Drive: service accounts have no storage quota).
"""
import json, os, sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def get_credentials():
    """OAuth refresh token (uploads as you, uses your Drive quota) or service account (Shared Drives only)."""
    if os.environ.get("GDRIVE_REFRESH_TOKEN"):
        from google.oauth2.credentials import Credentials
        cid, sec, rt = (os.environ.get(k, "") for k in ("GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET", "GDRIVE_REFRESH_TOKEN"))
        print(f"diag: client_id={cid[:22]!r}... len={len(cid)} ws={cid != cid.strip()} | "
              f"secret len={len(sec)} starts_GOCSPX={sec.startswith('GOCSPX-')} ws={sec != sec.strip()} | "
              f"refresh len={len(rt)} starts_1//={rt.startswith('1//')} ws={rt != rt.strip()}")
        return Credentials(
            None, refresh_token=rt.strip(),
            client_id=cid.strip(), client_secret=sec.strip(),
            token_uri="https://oauth2.googleapis.com/token",
            scopes=["https://www.googleapis.com/auth/drive"])
    raw = os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON", "").strip()
    try:
        info = json.loads(raw)
        assert info.get("type") == "service_account" and info.get("private_key")
    except Exception:
        sys.exit("No valid credentials: set GDRIVE_REFRESH_TOKEN (+ GDRIVE_CLIENT_ID/SECRET) or GDRIVE_SERVICE_ACCOUNT_JSON")
    return service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"])


def main(path: str, name: str) -> None:
    if not os.environ.get("GDRIVE_FOLDER_ID", "").strip():
        sys.exit("GDRIVE_FOLDER_ID secret is missing or empty")
    drive = build("drive", "v3", credentials=get_credentials(), cache_discovery=False)
    f = drive.files().create(
        body={"name": name, "parents": [os.environ["GDRIVE_FOLDER_ID"].strip()]},
        media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True),
        fields="id,webViewLink", supportsAllDrives=True).execute()
    print("uploaded:", f["webViewLink"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
