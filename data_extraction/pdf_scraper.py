import requests
from bs4 import BeautifulSoup

def fetch_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = []
    
    # Code Added for scraping PDF Links 
    # Customize this according to the structure of the website 
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.pdf'):
            full_link = url + href if href.startswith('/') else href
            pdf_links.append(full_link)
    
    return pdf_links

# Code Added to handle downloading and text extraction
import PyPDF2
import os

# Folder where PDFs will be stored temporarily
pdf_folder = 'data_extraction/pdfs'

def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    with open(save_path, 'wb') as pdf_file:
        pdf_file.write(response.content)

def parse_pdf_text(file_path):
    text = ""
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def process_pdfs(pdf_links):
    parsed_text = {}
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    
    for i, pdf_url in enumerate(pdf_links):
        file_name = f'pdf_{i}.pdf'
        file_path = os.path.join(pdf_folder, file_name)
        
        # Download and parse
        download_pdf(pdf_url, file_path)
        parsed_text[file_name] = parse_pdf_text(file_path)
    
    return parsed_text

# Code Added for Storing Parsed Text for Model Fine-tuning  ------- <File path Models/parsed_pdf_text.json> -------
import json

def save_parsed_text(data, file_path1='Trainer/parsed_pdf_text.json'):
    with open(file_path1, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
if __name__ == "__main__":
    url = "https://maharera.maharashtra.gov.in/orders-judgements"
    pdf_links = fetch_pdf_links(url)
    parsed_text = process_pdfs(pdf_links)
    save_parsed_text(parsed_text)


