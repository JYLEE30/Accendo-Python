# Import required libraries
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import ollama
import datetime
from fpdf import FPDF
import re

# Open a file dialog to select a PDF file
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_path

# Extract text from a specific page in the PDF
def extract_text_from_range(pdf, start_page, end_page):
    
    text = ""
    
    for page_num in range(start_page - 1, end_page):  # Page numbers are 0-based in PyMuPDF
        page = pdf[page_num]
        text += page.get_text() + "\n"
    
    return text

def extract_chunks(file_path, chunks):

    extracted_chunks = {chunk: "" for chunk in chunks}
    
    # Open the PDF file
    pdf_document = fitz.open(file_path)
    
    # Extract text for each defined chunk
    for chunk_name, page_ranges in chunks.items():
        for start_page, end_page in page_ranges:
            extracted_chunks[chunk_name] += extract_text_from_range(pdf_document, start_page, end_page)
    
    # Close the PDF document
    pdf_document.close()
    
    return extracted_chunks

# Summarize the given text chunk using gemini model with a specific prompt and full context
def generate_summary(full_text, text_chunk, prompt):
    
    # Set up Generative AI API
    model_name = 'llama3'

    context_prompt = f"Full document context:\n\n{full_text}\n\nSpecific section:\n\n{text_chunk}\n\n{prompt}"
    response = ollama.chat(model=model_name, messages=[
        {
            'role': 'user',
            'content': context_prompt,
        },
    ])
    return response['message']['content']

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
    
    file_path = select_pdf_file()

    if file_path:
        print(f"Selected file: {file_path}")

        try:
            # Define the page ranges to extract for each chunk
            chunks = {
                "Chunk_1": [(1, 1)],
                "Chunk_2": [(3, 3)],
                "Chunk_3": [(4, 7), (13, 17)],
                "Chunk_4": [(8, 9)],
                "Chunk_5": [(10, 10)],
                "Chunk_6": [(3, 3), (12, 12)]
            }
            
            # Extract the chunks
            extracted_chunks = extract_chunks(file_path, chunks)
            full_text = "\n".join(extracted_chunks.values())  # Combine all chunks for full context
            
            # Output the extracted text for each chunk
            for chunk_name, text in extracted_chunks.items():
                print(f"\n{chunk_name}:\n\n{text}{'-'*40}")
            
            # Define specific prompts for each chunk (customize as needed)
            prompts = {
                "Chunk_1": "Retrieve the name of the report, the candidate name, the candidate overall score and candidate score in the 3 main element.",
                "Chunk_2": "Retrieve all scores in quickview.",
                "Chunk_3": "Retrieve the most motivated by, least motivated by and the three work styles with the highest score of the candidate each in a line.",
                "Chunk_4": "Give a very brief summary for each of the 4 element in the leadership section referring to their comment in the about the candidate and implications and retrieve 1 most important question to ask the candidate from the CBI section for each of the 4 element in the leadership section and the CBI section.",
                "Chunk_5": "For each of the 2 element in the agility section, give a very brief summary referring to their about you comments and for each of the 3 elements in the cognitive agility breakdown, retrieve their scores and give a very brief summary referring to their definition and about you comments of each breakdown.",
                "Chunk_6": "For each of the 3 element in the cultural fit section, give a very brief summary referring to their definition and comment."
            }

            print("\nGenerating Summary:...")

            summary=""
            # Summarize each chunk with context
            for chunk_name, text in extracted_chunks.items():
                prompt = prompts.get(chunk_name, "Please summarize the above section.")
                response = generate_summary(full_text, text, prompt)
                summary += response + "\n"

            # Add an additional prompt to analyze the full context for possible derailers
            derailers_prompt = "Analyze the full document context to suggest 3 possible derailers of the candidate with a very brief description."
            derailers_summary = generate_summary(full_text, "", derailers_prompt)
            summary += f"Possible Derailers Analysis:\n{derailers_summary}"

            print("\nSummarized Report:\n")
            print(f"{summary}\n{'-'*40}")

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\ExecRep AI-04 Ollaman_Meta_Llama3-8B_M3_{timestamp}.pdf'
            save_text_as_pdf(summary, output_path)
            print(f"\nSummary saved to: {output_path}")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()