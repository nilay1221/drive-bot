from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import logging
import sys

SCOPES = ['https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT_FILE = './service.json' #PATH to service account credentials
SHARED_DRIVE_ID = '' #ADD ID of SHARED DRIVE if using SHARED DRIVE


credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)


drive = build('drive','v3',credentials=credentials,cache_discovery=False)

def uploadFile(filePath,fileName,mimeType,folderId=None):
    media = MediaFileUpload(filePath,mimetype=mimeType,resumable=True)
    file_metadata = {
        'name':fileName,
    }
    file_metadata['parents'] = [folderId] if folderId is not None else [SHARED_DRIVE_ID]
    request = drive.files().create(body=file_metadata,media_body=media,supportsAllDrives=True)

    response = None
    while response is None:
        try:
            status,response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress()) * 100}")
        except Exception as e:
            print(e)
    print("Upload complete")
    return response['id']

