import csv
import os
from pypdf import PdfReader, PdfWriter
import fitz # pymupdf

# load the AI-generated field mappings csv 
def load_field_mappings(csv_path):
    field_mapping = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            field_mapping[row["Field Name"]] = row["Value"]
            
    return field_mapping

# set human-readable labels for the form fields 
def extract_form_fields_and_labels(pdf_path):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # extract all form fields
        for field in page.widgets():
            if field.field_name:
                
                # extract text near the field to determine the label
                rect = field.rect  # get the bounding box of the form field
                x0, y0, x1, y1 = rect  # coordinates of the field
                
                # extract text near the form field (look for text around the bounding box)
                label_text = None
                nearby_text = page.get_text("dict")["blocks"]
                for block in nearby_text:
                    if block['type'] == 0:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                # check if the span is near the field (same or adjacent region)
                                text_x, text_y = span["bbox"][0], span["bbox"][1]
                                if abs(text_x - x0) < 50 and abs(text_y - y0) < 50:
                                    # don't include colons or numbers in the label
                                    label_text = span["text"].replace(":","").strip()
                                    label_text = ''.join(filter(str.isalpha, label_text))
                                
                # save the detected label
                if label_text:
                    field.field_label = label_text

# fill in the form fields in the PDF with values from the field mapping
def fill_pdf(pdf_path, output_path, field_mapping):
    
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # extract form fields on the page
        for field in page.widgets():
            # if the label was set for this form field 
            if field.field_label:
                field_label = field.field_label.lower() # normalize for matching
                field_value = "HELLO WORLD"
                # match label to corresponding value in the dictionary
                for key, value in field_mapping.items():
                    # if either the field label is in the mapping label or the mapping label is in the field label, set the value
                    if field_label in key or key in field_label:
                        field_value = value
                        break 
                
                field.field_value = field_value  # set the field value
                field.update() # must be called to actually store changes in PDF
                    

    # Save the filled PDF
    doc.save(output_path)
    print(f"Filled PDF saved to {output_path}")


# fill in the form fields for each saved PDF
def process_filled_pdfs(input_folder, output_folder, csv_path):
    # if the output folder already exists, keep it, otherwise create a new dir
    os.makedirs(output_folder, exist_ok=True)
    
    # load the field mappings from the AI-generated field mappings csv
    field_mapping = load_field_mappings(csv_path)
    
    for pdf_filename in os.listdir(input_folder):
        if pdf_filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, pdf_filename)
            output_path = os.path.join(output_folder, f"filled_{pdf_filename}")
            
            # Extract form fields and labels
            extract_form_fields_and_labels(pdf_path)
            
            fill_pdf(pdf_path, output_path, field_mapping)

input_folder = "./pdf_scraper/fillable_pdfs"  # folder containing the saved PDFs
output_folder = "filled_pdfs"  # folder to save filled PDFs
csv_path = "field_mappings.csv"  # path to the csv file with field mappings

process_filled_pdfs(input_folder, output_folder, csv_path)