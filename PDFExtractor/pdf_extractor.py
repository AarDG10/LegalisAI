import io
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PyPDF2 import PdfReader

# Constants
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
PDF_FOLDER_ID = '1q8RPAbKjAlw25hs_C-XGm2h8smseTeFP'  # Update this with your folder ID
OUTPUT_JSON_PATH = 'data/extracted_pdf_texts.json'

# Google Drive Authentication
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Function to retrieve all PDF file IDs in the specified folder
def get_pdf_file_ids(folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/pdf'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    if not files:
        print("No PDF files found in the specified folder.")
    else:
        print(f"Found {len(files)} PDF file(s) in the specified folder.")
    return [(file.get('id'), file.get('name')) for file in files]

# Function to download PDF file and extract text
def download_and_extract_text(file_id, file_name):
    try:
        request = drive_service.files().get_media(fileId=file_id)
        file_io = io.BytesIO()
        downloader = MediaIoBaseDownload(file_io, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()
        file_io.seek(0)

        # PDF text extraction
        reader = PdfReader(file_io)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return {"file_name": file_name, "text": text.strip()}
    except Exception as e:
        print(f"Failed to process {file_name}: {e}")
        return None

# Main function to process all PDFs and save to JSON
def process_pdfs_to_json():
    pdf_file_data = []
    pdf_files = get_pdf_file_ids(PDF_FOLDER_ID)

    for file_id, file_name in pdf_files:
        print(f"Processing: {file_name}")
        pdf_data = download_and_extract_text(file_id, file_name)
        if pdf_data and pdf_data["text"]:
            pdf_file_data.append(pdf_data)
        else:
            print(f"No text extracted from {file_name}")

    # Save extracted text data to JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(pdf_file_data, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {OUTPUT_JSON_PATH}")

# Run the extraction process
if __name__ == "__main__":
    process_pdfs_to_json()