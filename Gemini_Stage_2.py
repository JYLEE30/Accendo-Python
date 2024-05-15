import google.generativeai as genai
from PyPDF2 import PdfReader
from fpdf import FPDF
import datetime

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
print("Number of pages:", len(reader.pages), "\n")

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
    
    # Print the extracted text for the current page
    print(f"Page {i+1}:\n{text}\n")

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

# Generate a timestamp to append to the file name
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Set the desired output path with the timestamp appended to the file name
output_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Executive_Report_{timestamp}.pdf'

# Save the generated summary as a PDF
save_text_as_pdf(summary, output_path)

print("Successfully Saved")