# Import necessary libraries
from transformers import pipeline
from PyPDF2 import PdfReader
from fpdf import FPDF
import datetime

# Initialize the summarization pipeline with BART
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Path to the PDF
file_path = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(1) JYLEE_TPRecruitmentExtensive.pdf"

# Creating a PDF reader object
reader = PdfReader(file_path)

# Define the range of pages to extract text from
start_page = 0
end_page = len(reader.pages)

# Initialize a variable to store extracted text
extracted_text = ""

# Initialize a variable to store summarized content
summarized_content = ""

# Modified prompt
prompt = """
Summarize the extracted text by following these instructions:

1. Page 1: Extract the REPORT name, Candidate name, and Overall Score.
2. Skip Page 2.
3. Page 3: Retrieve names and scores of each quality in markdown format.
4. Pages 4 to 7: Extract quality names and provide a brief summary of the "About the Candidate" section, including implications.
5. Page 8: For each quality, summarize the "About You" section and provide a summary of the "Score Breakdown" section, including definitions.
6. Page 9: Summarize the "Score Breakdown" section, including definitions.
7. Page 10: Extract sub-quality names and summarize their definitions. Provide an interpretation of the Candidate's persona.
8. Page 11: Retrieve the main title, Candidate's primary motivators, and demotivators.
9. Page 12: Retrieve the main title and list the Candidate's top and bottom 3 behavioral preferences.
10. Page 13: Summarize the information to explain CBI in a short paragraph (max 30 words).
11. Pages 14 to 17: Analyze questions and select the most important one to ask the Candidate.
12. Exclude the last page.
13. Analyze all information and identify 3 Hogan Derailers.
14. Ensure the summarized content fits on one page.
"""

# Iterate through each page and process the prompt
for i in range(start_page, end_page):
    # Get text from a specific page
    page_text = reader.pages[i].extract_text()
    
    # Print the extracted text for the current page
    print(f"Extracted Text - Page {i + 1}:")
    print(page_text)
    print()  # Add a blank line for separation

    # Extract the relevant prompt for the current page
    prompt_lines = prompt.split("\n")
    prompt_line = prompt_lines[i].strip()

    # Process the prompt for the current page
    if i == 0:  # Page 1
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == 2:  # Page 3
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif 3 <= i <= 7:  # Pages 4-7
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == 8:  # Page 8
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == 9:  # Page 9
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == 10:  # Page 10
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == 11:  # Page 11
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == 12:  # Page 12
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == 13:  # Page 13
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif 14 <= i <= 17:  # Pages 14-17
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)
    elif i == len(reader.pages) - 1:  # Last page
        summary = summarizer(f"{prompt_line} {page_text}", max_length=50, min_length=30, do_sample=False)

    # Append the summary text to the summarized content
    summary_text = summary[0]["summary_text"]
    summarized_content += summary_text + "\n"

# Print the summarized content for the current page
print("Summarized Content:")
print(summarized_content)

# Save as PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=8)
    
# Encode the text using UTF-8
encoded_text = summarized_content.encode('latin-1', 'replace').decode('latin-1') 
pdf.multi_cell(0, 5, encoded_text)

# Save the PDF
pdf_file_path = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(5) bart-large-cnn_ExecRep.pdf"
pdf.output(pdf_file_path)

print("PDF saved successfully.")