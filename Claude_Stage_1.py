# Import required libraries
# import request
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from anthropic import Anthropic
import datetime
from fpdf import FPDF

# Define repetitive function to select pdf file from host
def select_pdf():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        return file_path
    else:
        return None

# Select, read and print the pdf
pdf_path = select_pdf() # Call the predefined function

if pdf_path:
    # Read the PDF file
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    text = ''.join(page.extract_text() for page in reader.pages)
    print(text)
else:
    print("No file selected.")

# Set up for Generative AI & API
# API_URL = "https://www.anthropic.com/claude/v1/complete"

MODEL_NAME = "claude-3-haiku-20240307"

# Connecting to the AI with specified settings
def get_completion(client, prompt):
    return client.messages.create(
        model=MODEL_NAME,
        max_tokens=400,
        messages=[{
            "role": 'user', "content":  prompt
        }]
    ).content[0].text

# Prompt the AI for desired output
completion = get_completion(client,
    f"""Here is an assessment result report: <paper>{text}</paper>

Please do the following:
1. In Page 1, retrieve the name of the REPORT, name of the Candidate and the Overall Score.
2. Exclude Page 2.
3. In Page 3, retrieve all the name and the score of each quality and arrange the retrieved content in a multi-level list format.
4. In Page 4 to 7, retrieve the name of the quality. Then, analyze and give a very short summary on the "About the Candidate: …" section of each quality including the "Implications" section of each quality one by one in a multi-level list format.
5. In Page 8, retrieve the name of each quality and give a very short summary on the "About You: …" section of each quality one by one. Then, retrieve all information in the "Score Breakdown: …" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the "About You: …" section of each breakdown and arrange the retrieved content in a multi-level list format.
6. In Page 9, retrieve all information in the "Score Breakdown: …" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the "About You: …" section of each breakdown and arrange the retrieved content in a multi-level list format.
7. In Page 10, retrieve the name of each sub quality under the main quality and summarize each of the sub qualities’ definitions one by one. Then, interpret the persona of the Candidate and give a short summary.
8. In Page 11, retrieve the main tittle. Then, retrieve the candidate's 3 primary motivators (Most motivated by:) and 3 demotivators (Least motivated by:).
9. In Page 12, retrieve the main tittle. Then, list the candidate's first 3 behavioural preferences as (Most likely:) and last 3 behavioural preferences as (Least likely).
10. In Page 13, retrieve the information and summarize it to explain CBI in a short paragraph not more than 30 words.
11. In Page 14 to 17, retrieve the main tittle, analyze all the question and pick one most important question to ask the Candidate regarding the main tittle of that page.
12. Exclude last page.
13. Analyze all information and give 3 Hogan Derailers.
14. Analyze all information and suggest which domain is this candidate suitable to work in such as education, financial etc.
15. Make sure the summarized content can fit in one page.
"""
)

# Print summarized content for verification
print(completion)

# Generate a timestamp to append to the file name
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Set the desired output path with the timestamp appended to the file name
output_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Claude_ExecRep_{timestamp}.pdf'

# Define repetitive function to save text as a PDF
def save_text_as_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    
    # Encode the text using UTF-8
    encoded_text = text.encode('latin-1', 'replace').decode('latin-1') 
    
    pdf.multi_cell(0, 5, encoded_text)
    pdf.output(output_path)

# Save the generated summary as a PDF
save_text_as_pdf(completion, output_path)

print("Successfully Saved")
print("Output Path:", output_path)