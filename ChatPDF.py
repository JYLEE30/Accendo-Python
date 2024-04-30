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
                                Execute the following command in order:
                                Retrieve the Name of the Report.
                                Retrieve the Candidate Name.
                                Skip "Introduction" page.
                                Retrieve the Overall Score.
                                Retrieve the name and score of each quality in markdown format.
                                Retrieve the name of each behaviour tendencies under the leadership quality. Analyze and give a short summary on their “About the Candidate:” and "Implications" section in 1 sentence. 
                                Retrive the candidate's 2 major componenets in agility and summarize their "About You:" section including the three breakdown under cognitive ability (Inductive-Logical Reasoning, Numerical Reasoning, Verbal Reasoning) and then summarize each of their "About You:" sections. Retrieve the score of the three breakdowns too.
                                Summarize the candidate's agility (Major componenets) for all the 2 key aspects with brief definitions.
                                Summarize the candidate's cultural fit (Preference) for all the 3 key aspects with brief definitions.
                                Retrieve the candidate's 3 primary motivators (Most motivated by:) and 3 demotivators (Least motivated by:). 
                                Retrieve the candidate's 3 (Most likely) Work Styles and 3 (Least likely) Work Styles.
                                Briefly explain the purpose of the CBI Guide. 
                                Retrieve one question most tailored to the candidate's quality from the Suggested Questions for each of the quality in the CBI section.
                                Skip "About Us" page.
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