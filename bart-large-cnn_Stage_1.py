from transformers import pipeline
from PyPDF2 import PdfReader
from fpdf import FPDF

# Initialize the summarization pipeline with BART
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Path to the PDF
file_path = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(1) JYLEE_TPRecruitmentExtensive.pdf"

# Creating a PDF reader object
reader = PdfReader(file_path)

# Define the range of pages to extract text from
start_page = 0
end_page = len(reader.pages)

# Initialize a variable to store summarized content
summarized_content = ""

# Simplified prompt
prompt = "Summarize the page."

# Iterate through each page and summarize the content
for i in range(start_page, end_page):
    # Get text from a specific page
    page_text = reader.pages[i].extract_text()
    
    # Concatenate prompt and page text
    input_text = prompt + " " + page_text
    
    # Summarize the input text
    summary = summarizer(input_text, max_length=50, min_length=40, do_sample=False)
    
    # Append the summary text to the summarized content
    summary_text = summary[0]["summary_text"]
    summarized_content += f"Summarized Content - Page {i + 1}:\n{summary_text}\n\n"

# Print the summarized content
print("Summarized Content:")
print(summarized_content)

# Function to save text as a PDF
def save_text_as_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    
    # Encode the text using UTF-8
    encoded_text = text.encode('latin-1', 'replace').decode('latin-1') 
    
    pdf.multi_cell(0, 5, encoded_text)
    pdf.output(output_path)

# Save the PDF
output_path = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Summarized_Report.pdf"

print("PDF saved successfully.")