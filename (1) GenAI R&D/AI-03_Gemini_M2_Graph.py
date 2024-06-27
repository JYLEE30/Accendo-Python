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

# Ask how many PDF files to summarize
def ask_number_of_files():
    root = tk.Tk()
    root.withdraw()
    num_files = simpledialog.askinteger("Input", "How many PDF files do you want to summarize?", minvalue=1, maxvalue=100)
    root.destroy()
    return num_files

# Open a file dialog to select a PDF file.
# Returns the file path if a file is selected, otherwise returns None.
def select_pdf_files(num_files):
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
    root.destroy()
    if len(file_paths) != num_files:
        raise ValueError(f"Expected {num_files} files but selected {len(file_paths)}.")
    return file_paths

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

# Summarize the given text chunk using gemini model with a specific prompt and full context
def generate_summary(full_context, prompt):
    
    # Set up Generative AI API
    genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    full_prompt = f"Full document context:\n\n{full_context}\n\n{prompt}"
    response = model.generate_content(full_prompt)
    
    return response.text

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
    text = re.sub(r':\**', ': ', text)
    text = re.sub(r':\*', ': ', text)

    # Add the processed text to the PDF
    pdf.multi_cell(0, 5, text)  # cell_width set to 0 to use the full page width (within margins)
    
    # Save the PDF to the specified output path
    pdf.output(output_path)

# Main function to run the PDF text extraction and summarization process
def main():
    num_files = ask_number_of_files()

    if num_files:
        file_paths = select_pdf_files(num_files)
        
        if len(file_paths) == num_files:
            print(f"Selected files: {file_paths}")

        try:
            context_chunks = []

            # Loop through each file to extract text and save as a chunk
            for i, file_path in enumerate(file_paths):
                print(f"\nProcessing file {i+1}/{len(file_paths)}: {file_path}")
                extracted_text = extract_text_from_pdf(file_path)
                context_chunks.append(extracted_text)
            
            # Define specific prompts for each chunk (customize as needed)
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
            """
            
            print("\nGenerating Summaries:")
            for i, chunk in enumerate(context_chunks):
                print(f"\nProcessing chunk {i+1}/{len(context_chunks)}")
                summarized_context = generate_summary(chunk, prompt)
                print(f"\nSummary {i+1}:\n")
                print(summarized_context)
                
                # Save summarized report as PDF
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"ExecRep AI-03 Google_Gemini-1.5-Flash_M2_Graph_{timestamp}.pdf"
                output_pdf_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report', file_name)
                save_text_as_pdf(summarized_context, output_pdf_path)
                print(f"\nSummary saved to: {output_pdf_path}")

        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("\nNo file selected.")

if __name__ == "__main__":
    main()