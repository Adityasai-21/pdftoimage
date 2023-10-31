
import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from urllib.parse import urljoin

# Function to download PDFs from a URL
def download_pdfs_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_links = []

    # Find PDF links on the webpage
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        if link.endswith('.pdf'):
            pdf_links.append(urljoin(url, link))

    return pdf_links

# Function to convert a PDF to images
def convert_pdf_to_images(pdf_url, output_folder):
    pdf_filename = os.path.basename(pdf_url)
    pdf_name_without_extension = os.path.splitext(pdf_filename)[0]
    image_folder = os.path.join(output_folder, pdf_name_without_extension)
    os.makedirs(image_folder, exist_ok=True)

    try:
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()  # Check for request errors

        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)

        pdf_document = fitz.open(pdf_filename)
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            image = page.get_pixmap()
            image.save(os.path.join(image_folder, f"page_{page_number + 1}.jpg"))
        pdf_document.close()
    except Exception as e:
        print(f"Failed to convert PDF: {pdf_url} - {e}")
    finally:
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)  # Remove the downloaded PDF

# Main function
if __name__ == '__main__':
    # Set the URL of the webpage with the PDF links
    webpage_url = "https://scert.telangana.gov.in/e-Textbooks.htm"

    # Set the output folder where images will be stored
    output_folder = 'output_images/'

    pdf_links = download_pdfs_from_url(webpage_url)

    for pdf_url in pdf_links:
        convert_pdf_to_images(pdf_url, output_folder)
