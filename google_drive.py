import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import file_handler

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# check for creds, if none refresh or ask for login
def auth ():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return creds

# create folder
def createFolder(service):
    folder_metadata = {
        'name' : file_handler.createWindowsDate(),
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

# upload files to drive
def upload (changes,dir_path):
    creds = auth()
    service = build('drive', 'v3', credentials=creds)
    folder = createFolder()
    count = 0
    for change in changes:
        name = change.get('name')
        path = change.get('path')
        count++
        if path == dir_path:
            upload_path = name
        else:
            full_path = dir_path + '\\'
            upload_path = path.replace(full_path, '') + '\\' + name
        try:
            file_metadata = {
                'name' : upload_path,
                'parents' : [folder]
            }
            package = MediaFileUpload('{}/{}'.format(path, name))
            file = service.files().create(body=file_metadata, media_body=package, fields='id').execute()
        except HttpError as error:
            file_handler.writeLog('ERROR', error)
    return count
