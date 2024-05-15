import PyPDF2
from transformers import LlamaForCausalLM, LlamaTokenizer
from tkinter import Tk, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def select_pdf_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

def extract_text_from_pdf_in_chunks(pdf_path, page_ranges):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        chunks = []
        for start_page, end_page in page_ranges:
            text = ''
            for page_number in range(start_page - 1, end_page):
                if page_number < len(reader.pages):
                    page = reader.pages[page_number]
                    text += page.extract_text()
            chunks.append(text)
    return chunks

def summarize_text_with_llama(text):
    model_name = 'meta-llama/Meta-Llama-3-70B-Instruct'  # Use the appropriate model name
    tokenizer = LlamaTokenizer.from_pretrained(model_name)
    model = LlamaForCausalLM.from_pretrained(model_name)

    inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

def save_summary_as_pdf(summaries, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    for i, summary in enumerate(summaries):
        c.drawString(100, height - 100, f"Summary of Chunk {i + 1}:")
        text = c.beginText(100, height - 120)
        text.setTextOrigin(100, height - 120)
        text.setFont("Helvetica", 12)
        
        for line in summary.split('\n'):
            text.textLine(line)
        
        c.drawText(text)
        c.showPage()
    
    c.save()

def main():
    pdf_path = select_pdf_file()
    if pdf_path:
        # Define the specific page ranges for each chunk
        page_ranges = [
            (1, 3),
            (4, 7),
            (8, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (13, 13),
            (14, 17)
        ]
        
        # Extract text from PDF in chunks
        chunks = extract_text_from_pdf_in_chunks(pdf_path, page_ranges)
        
        summaries = []
        
        for i, chunk in enumerate(chunks):
            print(f"\nFull text of Chunk {i + 1}:\n")
            print(chunk)
            summary = summarize_text_with_llama(chunk)
            print(f"\nSummary of Chunk {i + 1}:\n")
            print(summary)
            summaries.append(summary)
        
        # Merge summaries and save as a new PDF
        output_pdf_path = 'summarized_document.pdf'
        save_summary_as_pdf(summaries, output_pdf_path)
        print(f"Summarized document saved as {output_pdf_path}")
    else:
        print("No file selected.")

if __name__ == '__main__':
    main()