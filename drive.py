import os
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth import get_credentials

_service_instance = None

EXPORT_MIME_TYPES = {
    'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.google-apps.presentation': 'application/pdf',
    'application/vnd.google-apps.drawing': 'image/png',
}

def get_drive_service():
    global _service_instance
    if _service_instance is None:
        creds = get_credentials()
        _service_instance = build('drive', 'v3', credentials=creds)
    return _service_instance

def download_file(file_id, file_name, destination_folder):
    service = get_drive_service()
    creds = get_credentials()
    try:
        request = service.files().get(fileId=file_id, fields='webContentLink, mimeType')
        file_info = request.execute()
        mime_type = file_info.get('mimeType')
        download_url = file_info.get('webContentLink')
        os.makedirs(destination_folder, exist_ok=True)
        headers = {'Authorization': 'Bearer ' + creds.token}
        if mime_type in EXPORT_MIME_TYPES:
            export_mime = EXPORT_MIME_TYPES[mime_type]
            base, _ = os.path.splitext(file_name)
            if export_mime == 'application/pdf': 
                file_name = base + '.pdf'
            elif 'word' in export_mime: 
                file_name = base + '.docx'
            elif 'sheet' in export_mime: 
                file_name = base + '.xlsx'
            elif 'image' in export_mime: 
                file_name = base + '.png'
            download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType={export_mime}"
        if not download_url: 
            return False
        try:
            response = requests.get(download_url, headers=headers, timeout=30)
            if response.status_code == 200:
                file_path = os.path.join(destination_folder, file_name)
                counter = 1
                base, ext = os.path.splitext(file_path)
                while os.path.exists(file_path):
                    file_path = f"{base}_{counter}{ext}"
                    counter += 1
                with open(file_path, 'wb') as f: 
                    f.write(response.content)
                return True
            else: 
                return False
        except Exception: 
            return False
    except HttpError as error:
        if "notFound" in str(error): 
            return False
        return False

if __name__ == '__main__':
    print("Drive service ready.")