import scrapy
import os
from pypdf import PdfReader, PdfWriter
from urllib.parse import urljoin

class DorSpiderSpider(scrapy.Spider):
    name = "dor_spider"
    allowed_domains = ["dor.wa.gov"]
    start_urls = ["https://dor.wa.gov"]

    # folder to save PDFs
    output_folder = "fillable_pdfs"
    # make this folder, unless it exists. 
    # exist_ok=True leaves existing directory unaltered.
    os.makedirs(output_folder, exist_ok=True)
    
    # parse the web page 
    def parse(self, response):
        # extract all links on the page
        for link in response.css('a::attr(href)').getall():
            full_url = urljoin(response.url, link)

            # if this links to a PDF file, send a request to download and check if it's fillable
            if full_url.endswith(".pdf"):
                yield scrapy.Request(full_url, callback=self.check_fillable_pdf)
            # if this links to another page internally, follow it and keep searching for PDFs
            elif self.allowed_domains[0] in full_url:
                yield scrapy.Request(full_url, callback=self.parse)
    
    # check if the pdf is fillable, and save it if it is
    def check_fillable_pdf(self, response):
        # the filename is the last part of the url + the output folder where it is being saved
        filename = os.path.join(self.output_folder, response.url.split("/")[-1])
        
        # save the PDF temporarily
        temp_path = "temp.pdf"
        with open(temp_path, "wb") as f:
            f.write(response.body)
        
        # check if the PDF is fillable, and if it is, move it to the final directory
        if self.is_fillable(temp_path):
            os.rename(temp_path, filename)  # Move it to the final directory
            self.log(f"Saved fillable PDF: {filename}")
        # if the PDF is not fillable, delete it
        else:
            os.remove(temp_path)
    
    # determine whether the pdf is fillable 
    def is_fillable(self, pdf_path):
        try:
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                fields = reader.get_fields()

                if fields and any(fields.values()):  # ensure fields exist and are interactive
                    return True

            return False
        except Exception as e:
            self.log(f"Error reading {pdf_path}: {e}")
            return False

