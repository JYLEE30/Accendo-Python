from transformers import T5ForConditionalGeneration, T5Tokenizer
from PyPDF2 import PdfReader
from fpdf import FPDF

# Initialize the T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Define the PDF file path
file_path = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(1) JYLEE_TPRecruitmentExtensive.pdf"

# Load the PDF file
reader = PdfReader(file_path)

# Define the prompt for T5 summarization
prompt = """
summarize: "Page 1: Extract the REPORT name, Candidate name, and Overall Score.
Page 3: Retrieve names and scores of each quality in markdown format.
Pages 4-7: Extract quality names and provide a brief summary of the 'About the Candidate' section, including implications.
Page 8: For each quality, summarize the 'About You' section and provide a summary of the 'Score Breakdown' section, including definitions.
Page 9: Summarize the 'Score Breakdown' section, including definitions.
Page 10: Extract sub-quality names and summarize their definitions. Provide an interpretation of the Candidate's persona.
Page 11: Retrieve the main title, Candidate's primary motivators, and demotivators.
Page 12: Retrieve the main title and list the Candidate's top and bottom 3 behavioral preferences.
Page 13: Summarize the information to explain CBI in a short paragraph (max 30 words).
Pages 14-17: Analyze questions and select the most important one to ask the Candidate.
Exclude the last page.
Analyze all information and identify 3 Hogan Derailers."
"""

# Initialize a variable to store the summarized content
summarized_content = ""

# Iterate through each page and summarize the content
for page_num, page in enumerate(reader.pages, start=1):
    # Extract text from the page
    page_text = page.extract_text()
    
    # Prepend the prompt to the page text
    input_text = prompt + page_text
    
    # Tokenize and summarize the input text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Append the summarized text to the result
    summarized_content += f"Summarized Content - Page {page_num}:\n{summary_text}\n\n"

# Print the summarized content
print(summarized_content)

# Save as PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=8)
    
# Encode the text using UTF-8
encoded_text = summarized_content.encode('latin-1', 'replace').decode('latin-1') 
pdf.multi_cell(0, 5, encoded_text)

# Save the PDF
pdf_file_path = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(3) Falconsai_ExecRep.pdf"
pdf.output(pdf_file_path)

print("PDF saved successfully.")