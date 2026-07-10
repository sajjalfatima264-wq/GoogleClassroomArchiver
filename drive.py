import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from auth import get_credentials

_service_instance = None

EXPORT_MIME_TYPES = {
    'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.google-apps.presentation': 'application/pdf',
    'application/vnd.google-apps.drawing': 'image/png',
}

# Map export MIME types to file extensions
EXPORT_EXTENSIONS = {
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/pdf': '.pdf',
    'image/png': '.png',
}

def get_drive_service():
    global _service_instance
    if _service_instance is None:
        creds = get_credentials()
        _service_instance = build('drive', 'v3', credentials=creds)
    return _service_instance

def download_file(file_id, file_name, destination_folder):
    """
    Downloads a file from Google Drive using proper API methods.
    Handles both Google Workspace files (Docs, Sheets, etc.) and regular files.
    """
    service = get_drive_service()
    
    try:
        # Get file metadata to determine the MIME type
        file_info = service.files().get(
            fileId=file_id, 
            fields='mimeType, name'
        ).execute()
        
        mime_type = file_info.get('mimeType', '')
        
        # Skip Google Forms - they cannot be exported
        if 'application/vnd.google-apps.form' in mime_type:
            return False
        
        # Create destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)
        
        # Determine if this is a Google Workspace file that needs export
        if mime_type in EXPORT_MIME_TYPES:
            export_mime = EXPORT_MIME_TYPES[mime_type]
            extension = EXPORT_EXTENSIONS.get(export_mime, '')
            
            # Replace the original extension with the export extension
            base_name = os.path.splitext(file_name)[0]
            file_name = base_name + extension
            
            # Use the export endpoint for Google Workspace files
            request = service.files().export(
                fileId=file_id, 
                mimeType=export_mime
            )
        else:
            # Use get_media for regular files (PDFs, images, Word docs, etc.)
            request = service.files().get_media(fileId=file_id)
        
        # Handle duplicate filenames
        file_path = os.path.join(destination_folder, file_name)
        counter = 1
        base, ext = os.path.splitext(file_path)
        while os.path.exists(file_path):
            file_path = f"{base}_{counter}{ext}"
            counter += 1
        
        # Download the file using proper Google API method
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        
        while not done:
            status, done = downloader.next_chunk()
        
        # Verify the file was downloaded and has content
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            os.remove(file_path)
            return False
            
        return True
        
    except HttpError as error:
        if "notFound" in str(error) or "accessDenied" in str(error):
            return False
        print(f"      [!] Drive API error for '{file_name}': {error}")
        return False
    except Exception as e:
        print(f"      [!] Download error for '{file_name}': {e}")
        return False

if __name__ == '__main__':
    print("Drive service ready.")