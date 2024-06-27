# Import required libraries
import tkinter as tk
from tkinter import simpledialog, filedialog
import fitz  # PyMuPDF
import os
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import google.generativeai as genai
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
        end_page = len(document) - 1  # Exclude the last page
    else:
        end_page = min(end_page, len(document) - 1)  # Exclude the last page if end_page exceeds the number of pages
    extracted_text = ""
    for i in range(start_page, end_page):
        page = document.load_page(i)  # Load the page
        text = page.get_text()  # Extract text
        extracted_text += text + "\n\n"
    document.close()  # Close the document after extraction
    return extracted_text

# Replace special characters that can't be encoded in 'latin-1'
def replace_special_characters(text):
    replacements = {
        '\ufb01': 'fi',
        '\ufb02': 'fl',
        # Add more replacements as needed
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text

# Connect & Generate summary using Generative AI.
def generate_summary(extracted_text):
    
    # Define specific prompts for each part (customize as needed)
    prompt = """
        Extract the following information:
        - Report name
        - Candidate's name
        - Overall score
        - 3 main elements and their scores
        - Sub-elements of the 3 main elements and their scores in 'Quickview'
        - Most motivated by
        - Least motivated by
        - 3 work styles with highest scores

        Format the output as below:
        {Report Name}
        Candidate Name: {Candidate Name}
        Overall Score: {Overall Score}

        {Main Element 1}: {Main Element 1's Score}
                + {Main Element 1's sub-element 1}: {Main Element 1's sub-element 1 Score}
                + {Main Element 1's sub-element 2}: {Main Element 1's sub-element 2 Score}
                + {Main Element 1's sub-element 3}: {Main Element 1's sub-element 3 Score}
                + {Main Element 1's sub-element 4}: {Main Element 1's sub-element 4 Score}
        {Main Element 2}: {Main Element 2's Score}
                + {Main Element 2's sub-element 1}: {Main Element 2's sub-element 1 Score}
                + {Main Element 2's sub-element 2}: {Main Element 2's sub-element 2 Score}
        {Main Element 3}: {Main Element 3's Score}
                + {Main Element 3's sub-element 1}: {Main Element 3's sub-element 1 Score}
                + {Main Element 3's sub-element 2}: {Main Element 3's sub-element 2 Score}
                + {Main Element 3's sub-element 3}: {Main Element 3's sub-element 3 Score}
                
        Most motivated by: {Most motivated by 1, Most motivated by 2, Most motivated by 3}
        Least motivated by: {Least motivated by 1, Least motivated by 2, Least motivated by 3}

        Preferable work styles: {Work style 1, Work style 2, Work style 3}

        For each of the sub-elements in the {Main Element 1} section:
        - Summarize the comment in the "About the Candidate" section and the implications as a single paragraph in less than or equal to 36 words.
        - Retrieve only the most important main question to ask the candidate from the CBI section for each of the sub-elements in the {Main Element 1} section, excluding sub-questions.

        Format the output as follows:
        {Main Element 1}
        {Main Element 1's sub-element 1}: {Summary of Comment in the "About the Candidate" Section and Implications}
        CBI Question: {Most Important Main Question from CBI Section}
                    
        {Main Element 1's sub-element 2}: {Summary of Comment in the "About the Candidate" Section and Implications}
        CBI Question: {Most Important Question from CBI Section}
                    
        {Main Element 1's sub-element 3}: {Summary of Comment in the "About the Candidate" Section and Implications}
        CBI Question: {Most Important Question from CBI Section}
                    
        {Main Element 1's sub-element 4}: {Summary of Comment in the "About the Candidate" Section and Implications}
        CBI Question: {Most Important Question from CBI Section}

        For each of the sub-elements in the {Main Element 2} section:
        - Summarize the comment in the "About You" section in less than or equal to 30 words.

        For each of the 3 breakdowns in the {Main Element 2's sub-element 2} Breakdown:
        - Retrieve their scores and Summarize their definition and comment in the "About You" section as a single paragraph in less than 22 words.

        Format the output as follows:
        {Main Element 2}
        {Main Element 2's sub-element 1}: {Summary of "About You" Comments}
                
        {Main Element 2's sub-element 2}: {Summary of "About You" Comments}. {Main Element 2's sub-element 2} breakdown:
        {Breakdown 1}  ({Breakdown 1's Score}): {Summary of Definition and "About You" Comments}
        {Breakdown 2}  ({Breakdown 2's Score}): {Summary of Definition and "About You" Comments}
        {Breakdown 3}  ({Breakdown 3's Score}): {Summary of Definition and "About You" Comments}

        For each of the sub-elements in the {Main Element 3} section:
        - Retrieve their scores.
        - Summarize their definition and comment as a single paragraph in less than or equal to 28 words.

        Format the output as follows:
        {Main Element 3}
        {Main Element 3's sub-element 1} ({Main Element 3's sub-element 1 Score}): {Summary of Definition and Comment}
        {Main Element 3's sub-element 2} ({Main Element 3's sub-element 2 Score}): {Summary of Definition and Comment}
        {Main Element 3's sub-element 3} ({Main Element 3's sub-element 3 Score}): {Summary of Definition and Comment}

        Analyze the full document context to suggest 3 possible derailers of the candidate with a brief description in less than or equal to 28 words.

        Format the output as follows:
        Possible derailers
        1. {Derailer 1 Title}: {Brief Description}
        2. {Derailer 2 Title}: {Brief Description}
        3. {Derailer 3 Title}: {Brief Description}

        Then, generate a shorter version of summary base on your generated response with important scores and suggest his strangth and weakpoint.
               
        Lastly, summarize your generated response into a shorter version in email format with essential details.

        Format the output as follows:
        Subject: Recruitment Report for {Candidate Name}

        Dear Hiring Manager,

        This email summarizes the assessment results for candidate {Candidate Name}. 
        
        Overall score: {Overall Score}
        
        {Main Element 1}: {Main Element 1's Score}
        {Main Element 2}: {Main Element 2's Score}
        {Main Element 3}: {Main Element 3's Score}

        Key Highlights:
        Strengths: {From your response}
        Areas for Development: {From your response}
        Possible Derailers: {From your response}

        Motivators: {From your response}
        Demotivators: {From your response}
        Preferable Work Styles: {From your response}

        For a detailed analysis of his/her sub skills and other components, please review his/her Executive Report attached to this email.

        Thank you for using our product.

        Best regards,
        Accendo Technologies
    """
    
    # Set up Generative AI API
    genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    full_prompt = f"Full document context:\n\n{extracted_text}\n\n{prompt}"
    response = model.generate_content(full_prompt)

    return response.text

# Function to save text as a PDF
def save_text_as_pdf(summary, output_path):

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
    summary = re.sub(r'\#\#\# (.*)', r'\1', summary)  # Remove '###'
    summary = re.sub(r'\#\# (.*)', r'\1', summary)  # Remove '##'
    summary = re.sub(r'\* \**', '', summary)  # Remove '* **'
    summary = re.sub(r'\*\*', '', summary)  # Remove '**'
    summary = re.sub(r'\* ', '', summary)  # Remove '* '
    summary = re.sub(r'\*', '', summary)  # Remove '*'
    summary = re.sub(r':\**', ': ', summary)
    summary = re.sub(r':\*', ': ', summary)

    # Add the processed text to the PDF
    pdf.multi_cell(0, 5, summary)  # cell_width set to 0 to use the full page width (within margins)
    
    # Save the PDF to the specified output path
    pdf.output(output_path)

# Main function to call sub-function and return content needed 
def main():
    
    file_path = select_pdf_file()
    
    if file_path:

        print(f"Selected file: {file_path}")

        try:
            extracted_text = extract_text_from_pdf(file_path)
            
            print("\nGenerating Summary:...")
            summary = generate_summary(extracted_text)
            print("\nSummarized Report:\n")
            print(summary)

            # Save summarized report as PDF
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\ExecRep AI-03 Google_Gemini-1.5-Flash_M2_{timestamp}.pdf'
            save_text_as_pdf(summary, output_path)
            print(f"\nSummary saved to: {output_path}")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()