import google.generativeai as genai
from PyPDF2 import PdfReader
from fpdf import FPDF
import datetime

# Set up Generative AI API
genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
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

prompt = f"""
Summarize the extracted text (One Page): {extracted_text}

* Show the report name.

* Show the candidate name. 

* Introduce the usage of the report

* Retrieve the score of the each quality in the report.

* Summarize every sub quality of the candidate leadership quality, highlight their key comment and their implications.

* Summarize every breakdown of the candidate's agility, including cognitive ability (Cognitive, Learning, Social) and "about you" sections.
    * Retrieve the score of the three breakdown

* Summarize the candidate's cultural fit (Preference) for the three key aspects with brief definitions.

* Highlight the candidate's primary motivators ("Most motivated by:") and demotivators ("Least motivated by:").

* Analyze and summarize the candidate's work styles in one short sentence.

* Briefly explain the purpose of the CBI Guide.
    * Retrieve one question most tailored to the candidate's profile for each of the quality with suggested questions

**Note:**
* Strive to condense the information into a single page while maintaining clarity.

"""

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

# Section 2: Extract all the aspects under each subskill and their scores.
# Section 5: Summarize the motivation factors.