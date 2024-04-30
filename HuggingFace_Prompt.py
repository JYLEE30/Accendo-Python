# HuggingFace Falconsai Summarization Code with prompt (Executable but not as desired)
import PyPDF2
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

# Function to extract text from a PDF file and print it page by page
def extract_and_print_text_from_pdf(pdf_path):
    text_per_page = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            print(f"Page {page_num + 1} Text:")
            print(text)
            text_per_page.append(text)  # Append extracted text to the list
    return text_per_page  # Return the list of extracted text

# Function to summarize text with a given prompt
def summarize_with_prompt(text, prompt):
    # Adjust max_length based on the input_length
    input_length = len(text)
    max_length = min(input_length // 2, 512)  # Set max_length to half of the input_length or 512, whichever is smaller
    summary = summarizer(prompt + text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Path to the PDF file
pdf_path = r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(1) JYLEE_TPRecruitmentExtensive.pdf'

# Extract text from each page of the PDF
text_per_page = extract_and_print_text_from_pdf(pdf_path)

# Prompt to use for summarization
prompt = "Summarize the following text: "

# Summarize each page separately with the prompt
summaries = []
for page_num, text in enumerate(text_per_page):
    summary = summarize_with_prompt(text, prompt)
    summaries.append(summary)

# Save the summaries to a text file
output_file = "summaries_with_prompt.txt"
with open(output_file, "w") as f:
    for page_num, summary in enumerate(summaries):
        f.write(summary + "\n\n")

print(f"Summaries with prompt saved to {output_file}")