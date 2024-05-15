import google.generativeai as genai
from PyPDF2 import PdfReader
from fpdf import FPDF
import datetime
import tkinter as tk
from tkinter import filedialog

# Set up Generative AI API
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Open a file dialog to select a PDF file.
# Returns the file path if a file is selected, otherwise returns None.
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
 
# Creating a PDF reader object
reader = PdfReader(file_path)

# Define the range of pages to extract text from
start_page = 0
end_page = len(reader.pages)

# Initialize a variable to store extracted text
extracted_text = ""

# Iterate through the range of pages and extract text
for i in range(start_page, end_page):
    # Get a specific page from the PDF file
    page = reader.pages[i]

    # Extract text from the page
    text = page.extract_text()
    
    # Append extracted text to the variable
    extracted_text += text

prompt = f"""
Summarize the extracted text: {extracted_text}

* In Page 1, retrieve the name of the REPORT, name of the Candidate and the Overall Score. 
* Exclude Page 2.
* In Page 3, retrieve all the name and score of each quality in markdown format.
* In Page 4 to 7, retrieve the name of the quality. Then, analyze and give a very short summary on the "About the Candidate: …" section including the implications section.
* In Page 8, retrieve the name of each quality and give a very short summary on the "About You: …" section of each quality one by one. Then, retrieve all information in the "Score Breakdown: …" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the "About You: …" section of each breakdown.
* In Page 9, retrieve all information in the "Score Breakdown: …" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the "About You: …" section of each breakdown.
* In Page 10, retrieve the name of each sub quality under the main quality and summarize each of the sub qualities’ definitions one by one. Then, interpret the persona of the Candidate and give a short summary.
* In Page 11, retrieve the main tittle. Then, retrieve the candidate's 3 primary motivators (Most motivated by:) and 3 demotivators (Least motivated by:).
* In Page 12, retrieve the main tittle. Then, list the candidate's first 3 behavioural preferences as (Most likely:) and last 3 behavioural preferences as (Least likely).
* In Page 13, retrieve the information and summarize it to explain CBI in a short paragraph not more than 30 words.
* In Page 14 to 17, retrieve the main tittle, analyze all the question and pick one most important question to ask the Candidate regarding the main tittle of that page.
* Exclude last page.
* Analyze all information and give 3 Hogan Derailers. 
* Make sure the summarized content can fit in one page.
"""

# Call the Generative AI model with the prompt
response = model.generate_content(prompt)

# Extract the generated summary from the response
summary = response.text

# Print the generated summary in the terminal
print("Generated Summary:")
print(summary)

# Generate a timestamp to append to the file name
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Set the desired output path with the timestamp appended to the file name
output_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Executive_Report_{timestamp}.pdf'

# Function to save text as a PDF
def save_text_as_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    encoded_text = text.encode('latin-1', 'replace').decode('latin-1') # Encode the text using UTF-8
    pdf.multi_cell(0, 5, encoded_text)
    pdf.output(output_path)

# Save the generated summary as a PDF
save_text_as_pdf(summary, output_path)

print("Successfully Saved")
print("Output Path:", output_path)