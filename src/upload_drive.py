"""Step 4: upload the finished mp4 straight to a Google Drive folder.

Auth: service-account JSON in env GDRIVE_SERVICE_ACCOUNT_JSON. Share the target
Drive folder with the service account's email (Editor). A plain API key CANNOT
upload files to Drive -- Google requires OAuth/service-account credentials for writes.
"""
import json, os, sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def main(path: str, name: str) -> None:
    raw = os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON", "").strip()
    if not os.environ.get("GDRIVE_FOLDER_ID", "").strip():
        sys.exit("GDRIVE_FOLDER_ID secret is missing or empty")
    try:
        info = json.loads(raw)
        assert info.get("type") == "service_account" and info.get("private_key")
    except Exception:
        sys.exit(f"GDRIVE_SERVICE_ACCOUNT_JSON is not a service-account key JSON "
                 f"(length {len(raw)}, starts with {raw[:1]!r}). Paste the whole key file, starting with '{{'.")
    creds = service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/drive"])
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    f = drive.files().create(
        body={"name": name, "parents": [os.environ["GDRIVE_FOLDER_ID"]]},
        media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True),
        fields="id,webViewLink", supportsAllDrives=True).execute()
    print("uploaded:", f["webViewLink"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
