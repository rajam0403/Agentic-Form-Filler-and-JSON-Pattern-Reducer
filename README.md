# Agentic Form Filler & JSON Pattern Reducer 

## Section 1: Agentic Form Filler

### Part 1: Conceptual Design

The objective of this component of the project is to design a system that can transform a PDF of unknown fields, structure, and page size into a filled version with labeled, editable fields containing the correct information. 

![](MainFlow.png)
![](FormFieldExtractorFlow.png)
![](FieldMatchingandFillingFlow.png)

### Part 2: Web Scraping Solution

The objective of this part of the project is to develop a web scraping solution that automatically extracts all PDFs from the Washington State Department of Revenue website, filters them to identify only those with labeled, editable fields, and fills in the fields with the "correct" answer. 

There are **two components** to this solution. The first performs the scraping and filtering and the second fills in the form fields in the PDFs. 

In order to run the first component, **you must have scrapy, pypdf, os, and urllib installed in your Python environment.** You can then run the first component using the following command in your terminal: 
```scrapy crawl dor_spider```
This will save only truly fillable PDFs from the Washington State Department of Revenue website. It will save these to the following path: "pdf_scraper/fillable_pdfs"

In order to run the second component, **you must have successfully run the first part of the solution such that there are fillable PDFs in the path "pdf_scraper/fillable_pdfs" and you must have csv, os, pypdf, and pymupdf installed in your Python environment.** You can run the second component using the following command in your terminal:
```python3 fill_pdfs.py```

*Having issues running the code? 
<br>Make sure you're in the correct directories for running these scripts and that you have the necessary libraries installed. The code has been tested and should work if these requirements are met. For component 1, make sure you are in the top-level "pdf_scraper" directory when you run the spider. For component 2, make sure you are in the top-level directory of this repository.*

## Section 2: JSON Pattern Reducer 