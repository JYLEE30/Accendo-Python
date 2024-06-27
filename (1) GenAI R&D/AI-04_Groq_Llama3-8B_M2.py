# Import required libraries
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import os
from groq import Groq
import datetime
from fpdf import FPDF
import re

# Open a file dialog to select a PDF file.
# Returns the file path if a file is selected, otherwise returns None.
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_path

# Extract text from the PDF file page by page.
def extract_text_from_pdf(file_path, start_page=0, end_page=None):
    document = fitz.open(file_path)
    if end_page is None:
        end_page = len(document)
    extracted_text = ""
    for i in range(start_page, end_page):
        page = document.load_page(i)  # Load the page
        text = page.get_text()  # Extract text
        extracted_text += text + "\n\n"
    return extracted_text

# Connect & Generate summary using Generative AI.
def generate_summary(extracted_text):

    client = Groq(api_key = os.environ.get("GROQ_API_KEY"),)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": 
                    f'''
                    Summarize the context below section by section with the following prompt:
                    Section 1: Retrieve the name of the report, the candidate name, the candidate overall score and candidate score in the 3 main element.
                    Section 2: Retrieve all scores in quickview.
                    Section 3: Retrieve the motivators, demotivators and work styles of the candidate.
                    Section 4: Give a very short summary for each of the 4 element in the leadership section regarding their comment in the about the candidate and implications and retrieve 1 most important question to ask the candidate from the CBI section for each of the 4 element in the leadership section and the CBI section.
                    Section 5: For each of the 2 element in the agility section, give a very short summary on their about you comments and for each of the 3 elements in the cognitive agility breakdown, retrieve the scores and give a short summary on the definition and the about you comments of each breakdown.
                    Section 6: For each of the 3 element in the cultural fit section, give a short summary on their definition and comment. 
                    Section 7: Analyze and provide 3 possible hogan derailers of the candidate with a very short explanation.

                    {extracted_text}

                    ''',
            }
        ],
        model = "llama3-8b-8192",
    )

    summary = chat_completion.choices[0].message.content
    
    return summary

# Function to save text as a PDF
def save_text_as_pdf(text, output_path):
    
    # Create an instance of FPDF class with A4 page size
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("times", size=10)

    # Set margins: left, top, right (bottom is handled automatically)
    pdf.set_left_margin(20)
    pdf.set_top_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Replace leading asterisks and hashes with dashes or remove them
    text = re.sub(r'\#\#\# (.*)', r'\1', text)  # Remove '###'
    text = re.sub(r'\#\# (.*)', r'\1', text)  # Remove '##'
    text = re.sub(r'\* \**', '', text)  # Remove '* **'
    text = re.sub(r'\*\*', '', text)  # Remove '**'
    text = re.sub(r'\* ', '', text)  # Remove '* '
    text = re.sub(r'\*', '', text)  # Remove '*'
    text = re.sub(r'(?<=\w)\**', '', text) # Remove '*' after
    text = re.sub(r'(?<=\w)\*', '', text) # Remove '*' after

    # Add the processed text to the PDF
    pdf.multi_cell(0, 5, text)  # cell_width set to 0 to use the full page width (within margins)
    
    # Save the PDF to the specified output path
    pdf.output(output_path)

# Main function to call sub-function and return content needed
def main():
    
    file_path = select_pdf_file()
    
    if file_path:

        print(f"Selected file: {file_path}")

        try:

            extracted_text = extract_text_from_pdf(file_path)
            
            print("Generating Summary:...")
            summary = generate_summary(extracted_text)
            print("\nSummarized Report:\n")
            print(summary)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\ExecRep AI-04 Groq_Meta_Llama3-8B_M2_{timestamp}.pdf'
            save_text_as_pdf(summary, output_path)
            print(f"\nSummary saved to: {output_path}")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No file selected.")
  
if __name__ == "__main__":
    main()