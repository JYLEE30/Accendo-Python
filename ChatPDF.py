import requests
from tkinter import Tk, filedialog
from fpdf import FPDF
from datetime import datetime

# Set up Generative AI API key
headers = {'x-api-key': 'sec_j2XeIF23GoFGd54IawzFiNVqTkGTP3f3'}

# Select PDF
def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    if file_path:
        upload_file(file_path)
    else:
        print("No file selected.")

# Upload PDF
def upload_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            files = [('file', ('file', file, 'application/octet-stream'))]
            response = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

        if response.status_code == 200:
            source_id = response.json().get('sourceId')
            if source_id:
                print('Status: PDF Successfully Uploaded')
                
                # Call the function to summarize the data
                summary_response = summarize_data(source_id)
                print("Summarized Data:")
                print(summary_response)
                
                # Save the summarized data as a PDF file
                save_pdf(summary_response, 'Executive_Report')
            else:
                print("Error: No source ID returned.")
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print("An error occurred:", str(e))

# Summarize PDF
def summarize_data(source_id):
    prompt_data = {
        "stream": True,
        "sourceId": source_id,
        "messages": [
            {
                "role": "user",
                "content": """ 
                                Retrieve the Report Name and Candidate Name. Briefly Introduce the Usage of the Report.
                                Retrieve the Scores on each of the quality including their sub-qualities in Page 2 of the Report. 
                                Analyze and Summarize every sub-quality of the candidate's leadership quality, summarize each "About the Candidate:" and implication sections.
                                Summarize every sub-quality of the candidate's agility quality, including the three breakdown under cognitive ability (Inductive-Logical Reasoning, Numerical Reasoning, Verbal Reasoning) and their summarize each of their "About You:" sections. Retrieve the score of the three breakdowns too.
                                Summarize the candidate's cultural fit (Preference) for all the three key aspects with brief definitions.
                                Retrieve the candidate's primary motivators (Most motivated by:) and demotivators (Least motivated by:) together with their scores. 
                                Analyze then summarize the candidate's Work Styles. Do mention the 3 most preferred work styles and 3 least preferred work styles.
                                Briefly explain the purpose of the CBI Guide. Retrieve one question most tailored to the candidate's profile from each of the sub-quality with suggested questions.
                                **Note: Strive to condense the information into a single page while maintaining clarity.**
                            """
            }
        ]
    }
    response = requests.post('https://api.chatpdf.com/v1/chats/message', json=prompt_data, headers=headers)
    return response.text  # Return raw text data

# Save as PDF
def save_pdf(text_content, file_name_prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{file_name_prefix}_{timestamp}.pdf"
    file_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\{file_name}'
    
    # Create a new PDF instance
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    
    # Add the text content to the PDF
    pdf.multi_cell(0, 10, txt=text_content)
    
    # Save the PDF
    pdf.output(file_path)
    
    print("Summarized data saved as PDF")

# Call the function to select a file
select_file()