import requests
from tkinter import Tk, filedialog
from fpdf import FPDF
from datetime import datetime

# Set up Generative AI API key
headers = {'x-api-key': ''}

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
                                Summarize the extracted text in order: 

                                In Page 1, retrieve the name of the REPORT, name of the Candidate and the Overall Score. 
                                Exclude Page 2.
                                In Page 3, retrieve all the name and score of each quality in markdown format.
                                In Page 4 to 7, retrieve the name of the quality. Then, analyze and give a very short summary on the "About the Candidate: …" section including the implications section.
                                In Page 8, retrieve the name of each quality and give a very short summary on the "About You: …" section of each quality one by one. Then, retrieve all information in the "Score Breakdown: …" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the "About You: …" section of each breakdown.
                                In Page 9, retrieve all information in the "Score Breakdown: …" section and show the Name of each Breakdown with the score, give a short summary on the definition  and  the "About You: …" section of each breakdown.
                                In Page 10, retrieve the name of each sub quality under the main quality and summarize each of the sub qualities’ definitions one by one. Then, interpret the persona of the Candidate and give a short summary.
                                In Page 11, retrieve the main tittle. Then, retrieve the candidate's 3 primary motivators (Most motivated by:) and 3 demotivators (Least motivated by:).
                                In Page 12, retrieve the main tittle. Then, list the candidate's first 3 behavioural preferences as (Most likely:) and last 3 behavioural preferences as (Least likely).
                                In Page 13, retrieve the information and summarize it to explain CBI in a short paragraph not more than 30 words.
                                In Page 14 to 17, retrieve the main tittle, analyze all the question and pick one most important question to ask the Candidate regarding the main tittle of that page.
                                Exclude last page.
                                Analyze all information and give 3 Hogan Derailers. 
                                Make sure the summarized content can fit in one page.
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
    pdf.multi_cell(0, 5, txt=text_content)
    
    # Save the PDF
    pdf.output(file_path)
    
    print("Summarized data saved as PDF")

# Call the function to select a file
select_file()