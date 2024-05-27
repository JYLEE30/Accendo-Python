# Import required libraries
import requests
from tkinter import Tk, filedialog
from fpdf import FPDF
import datetime
import re

# Set up Generative AI API key
headers = {'x-api-key': 'sec_j2XeIF23GoFGd54IawzFiNVqTkGTP3f3'}

# Select PDF
def select_pdf_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    if file_path:
        return file_path
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
                print('\nStatus: PDF Successfully Uploaded')
                print('\nGenarating Summary ...')
                
                # Call the function to summarize the data
                summary = generate_summary(source_id)
        
                return summary

            else:
                print("\nError: No source ID returned.")
        else:
            print('\nStatus:', response.status_code)
            print('Error:', response.text)
    except FileNotFoundError:
        print("\nError: File not found.")
    except Exception as e:
        print("\nAn error occurred:", str(e))

# Summarize PDF
def generate_summary(source_id):
    
    prompt_data = {
        "stream": True,
        "sourceId": source_id,
        "messages": [
            {
                "role": "user",
                "content": 
                f'''
                    Summarize the context below section by section with the following prompt:
                    Section 1: Retrieve the name of the report, the candidate name, the candidate overall score and candidate score in the 3 main element.
                    Section 2: Retrieve all scores in quickview.
                    Section 3: Retrieve the motivators, demotivators and work styles of the candidate.
                    Section 4: Give a very short summary for each of the 4 element in the leadership section regarding their comment in the about the candidate and implications and retrieve 1 most important question to ask the candidate from the CBI section for each of the 4 element in the leadership section and the CBI section.
                    Section 5: For each of the 2 element in the agility section, give a very short summary on their about you comments and for each of the 3 elements in the cognitive agility breakdown, retrieve the scores and give a short summary on the definition and the about you comments of each breakdown.
                    Section 6: For each of the 3 element in the cultural fit section, give a short summary on their definition and comment. 
                    Section 7: Analyze and provide 3 possible hogan derailers of the candidate with a very short explanation.
                ''',
            }
        ]
    }
    response = requests.post('https://api.chatpdf.com/v1/chats/message', json=prompt_data, headers=headers)
    return response.text  # Return raw text data
    
# Function to save text as a PDF
def save_text_as_pdf(summary, output_path):
    
    # Create an instance of FPDF class with A4 page size
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("times", size=10)

    # Set margins: left, top, right (bottom is handled automatically)
    pdf.set_left_margin(20)
    pdf.set_top_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Replace leading asterisks and hashes with dashes or remove them
    text = re.sub(r'\#\#\# (.*)', r'\1', text)  # Remove '###'
    text = re.sub(r'\#\# (.*)', r'\1', text)  # Remove '##'
    text = re.sub(r'\* \**', '', text)  # Remove '* **'
    text = re.sub(r'\*\*', '', text)  # Remove '**'
    text = re.sub(r'\* ', '', text)  # Remove '* '
    text = re.sub(r'\*', '', text)  # Remove '*'
    text = re.sub(r'(?<=\w)\**', '', text) # Remove '*' after
    text = re.sub(r'(?<=\w)\*', '', text) # Remove '*' after

    # Add the processed text to the PDF
    pdf.multi_cell(0, 5, txt=summary)  # cell_width set to 0 to use the full page width (within margins)
    
    # Save the PDF to the specified output path
    pdf.output(output_path)

def main():

    file_path = select_pdf_file()
    
    if file_path:
        print("Uploading PDF ...")
        summary = upload_file(file_path)
        print("\nSummary:")
        print(summary)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\ExecRep AI-02 ChatPDF_chatgpt-3.0_M1_{timestamp}.pdf'
    save_text_as_pdf(summary, output_path)
    print(f"\nSummary saved to: {output_path}")

if __name__ == "__main__":
    main()