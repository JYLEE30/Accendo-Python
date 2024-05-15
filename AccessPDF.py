import tkinter as tk
from tkinter import filedialog
import PyPDF2
from fpdf import FPDF
import datetime
import os
import openai

# Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Open a file dialog to select a PDF file.
# Returns the file path if a file is selected, otherwise returns None.
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_path

# Extract text from the selected PDF file in chunks of two pages each.
# Returns a list of text chunks.
def extract_text_chunks(file_path):
    reader = PyPDF2.PdfReader(file_path)
    text_chunks = []

    for i in range(0, len(reader.pages), 2):
        chunk = ""

        page1 = reader.pages[i]
        if i + 1 < len(reader.pages):
            page2 = reader.pages[i + 1]
        else:
            page2 = None

        text = page1.extract_text()
        chunk += text

        if page2:
            text = page2.extract_text()
            chunk += text

        text_chunks.append(chunk)

    return text_chunks

# Summarize the given text chunk using the Claude Haiku API.
# Returns the summarized text.
def summarize_chunk(text_chunk):
    response = openai.Completion.create(
        engine="claude-v1",
        prompt=f"Summarize the following text:\n\n{text_chunk}\n\nSummary:",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()
    return summary

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
            print("Summarizing text chunks...")

            summaries = []
            for i, chunk in enumerate(text_chunks, start=1):
                print(f"\nSummarizing Chunk {i}...")
                summary = summarize_chunk(chunk)
                summaries.append(summary)
                print(f"Summary for Chunk {i}:\n{summary}\n")

            output_dir = r"C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report"
            output_path = construct_output_path(output_dir)

            save_summaries_as_pdf(summaries, output_path)
            print(f"Summaries saved to '{output_path}'")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()