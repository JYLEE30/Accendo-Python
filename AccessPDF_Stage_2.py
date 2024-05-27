import tkinter as tk
from tkinter import filedialog
import PyPDF2
from fpdf import FPDF
import datetime
import os

# Open a file dialog to select a PDF file.
# Returns the file path if a file is selected, otherwise returns None.
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_path

def extract_text_chunks(file_path):
    reader = PyPDF2.PdfReader(file_path)
    text_chunks = []

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        text_chunks.append(text)

    for idx, chunk in enumerate(text_chunks):
        print(f"Chunk {idx + 1}:\n{chunk}\n")

    return text_chunks

# Construct the output file path with a timestamp.
def construct_output_path(output_dir):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"ExecRep_Claude_{timestamp}.pdf"
    output_path = os.path.join(output_dir, output_filename)
    return output_path

# Save the summaries as a PDF file.
def save_summaries_as_pdf(summaries, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)

    for summary in summaries:
        encoded_text = summary.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 5, encoded_text)
        pdf.cell(0, 5, "", 0, 1)  # Add a blank line after each summary

    pdf.output(output_path)

# Main function to run the PDF text extraction, summarization, and saving process.
def main():
    file_path = select_pdf_file()

    if file_path:
        print(f"Selected file: {file_path}")

        try:
            text_chunks = extract_text_chunks(file_path)

            # output_dir = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report"
            # output_path = construct_output_path(output_dir)

            # save_summaries_as_pdf(summaries, output_path)
            # print(f"Summaries saved to '{output_path}'")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()