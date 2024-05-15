import google.generativeai as genai
from PyPDF2 import PdfReader
from fpdf import FPDF

# Set up Generative AI API
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-pro')

# Function to save text as a PDF
def save_text_as_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(output_path)

# Path to the PDF file
file_path = r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(1) JYLEE_TPRecruitmentExtensive.pdf'
 
# Creating a PDF reader object
reader = PdfReader(file_path)

# Printing the number of pages in the PDF file
print("Number of pages:", len(reader.pages))

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

# Construct a prompt for text summarization
prompt = f"Summarize the extracted text: {extracted_text}"

# Call the Generative AI model with the prompt
response = model.generate_content(prompt)

# Extract the generated summary from the response
summary = response.text

# Print the generated summary in the terminal
print("Generated Summary:")
print(summary)

# Create a new PDF object
pdf = FPDF()

# Add a new page to the PDF
pdf.add_page()

# Set the font style and size
pdf.set_font("Arial", size=12)

# Write the generated summary to the PDF with auto spacing down to the next row
for line in summary.split('\n'):
    pdf.cell(200, 10, txt=line, ln=True)

# Save the PDF to a file
pdf.output("Executive Report.pdf")

# Print a message to confirm that the PDF was saved
print("Successfully Saved")