import PyPDF2
from tkinter import TK, filedialog
from pypdf import PdfReader
from groq import Groq
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

# Set up for API & Connect to Generative AI
client = Groq(api_key="")
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": f"Summarize the report in detail with Hogan derailers: <paper>{text}</paper>\n\nPlease do the following:\n1. In Page 1, retrieve the name of the REPORT, name of the Candidate and the Overall Score.\n2. Exclude Page 2.\n3. In Page 3, retrieve all the name and the score of each quality and arrange the retrieved content in a multi-level list format.\n4. In Page 4 to 7, retrieve the name of the quality. Then, analyze and give a very short summary on the \"About the Candidate: …\" section of each quality including the \"Implications\" section of each quality one by one in a multi-level list format.\n5. In Page 8, retrieve the name of each quality and give a very short summary on the \"About You: …\" section of each quality one by one. Then, retrieve all information in the \"Score Breakdown: …\" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the \"About You: …\" section of each breakdown and arrange the retrieved content in a multi-level list format.\n6. In Page 9, retrieve all information in the \"Score Breakdown: …\" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the \"About You: …\" section of each breakdown and arrange the retrieved content in a multi-level list format.\n7. In Page 10, retrieve the name of each sub quality under the main quality and summarize each of the sub qualities’ definitions one by one. Then, interpret the persona of the Candidate and give a short summary.\n8. In Page 11, retrieve the main tittle. Then, retrieve the candidate's 3 primary motivators (Most motivated by:) and 3 demotivators (Least motivated by:).\n9. In Page 12, retrieve the main tittle. Then, list the candidate's first 3 behavioural preferences as (Most likely:) and last 3 behavioural preferences as (Least likely).\n10. In Page 13, retrieve the information and summarize it to explain CBI in a short paragraph not more than 30 words.\n11. In Page 14 to 17, retrieve the main tittle, analyze all the question and pick one most important question to ask the Candidate regarding the main tittle of that page.\n12. Exclude last page.\n13. Analyze all information and give 3 Hogan Derailers.\n14. Analyze all information and suggest which domain is this candidate suitable to work in such as education, financial etc.\n15. Make sure the summarized content can fit in one page."
        }
    ],
    temperature=1,
    max_tokens=8192,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")