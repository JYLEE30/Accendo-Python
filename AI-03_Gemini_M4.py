# Import required libraries
import tkinter as tk
from tkinter import simpledialog, filedialog
import json
import google.generativeai as genai
import re
import datetime
import os
from fpdf import FPDF

# Ask how many JSON files to process
def ask_number_of_files():
    root = tk.Tk()
    root.withdraw()
    num_files = simpledialog.askinteger("Input", "How many JSON files do you want to process?", minvalue=1, maxvalue=100)
    root.destroy()
    return num_files

# Open a file dialog to select JSON files.
# Returns the file paths if files are selected, otherwise returns None.
def select_json_files(num_files):
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select JSON files", filetypes=[("JSON Files", "*.json")])
    root.destroy()
    if len(file_paths) != num_files:
        raise ValueError(f"Expected {num_files} files but selected {len(file_paths)}.")
    return file_paths

# Function to process the selected JSON files with data extraction
def process_json_files(file_path):
    try:
        with open(file_path, 'r') as file:  # Open the file here once
            context = json.load(file)
            return context
    except FileNotFoundError:
        print(f"\nError: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"\nError: Invalid JSON format in file '{file_path}'.")

# Summarize the given text chunk using gemini model with a specific prompt and full context
def generate_summary(json_context, prompt):
    
    # Set up Generative AI API
    genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    full_prompt = f"Full document context:\n\n{json_context}\n\n{prompt}"
    response = model.generate_content(full_prompt)
    
    return response.text

# Replace leading asterisks and hashes with dashes or remove them
def clear_GenAI_format(summarized_context):
    cleaned_context = re.sub(r'\#\#\# (.*)', r'\1', summarized_context)  # Remove '###'
    cleaned_context = re.sub(r'\#\# (.*)', r'\1', summarized_context)  # Remove '##'
    cleaned_context = re.sub(r'\* \**', '', summarized_context)  # Remove '* **'
    cleaned_context = re.sub(r'\*\*', '', summarized_context)  # Remove '**'
    cleaned_context = re.sub(r'\**', '', summarized_context)  # Remove '**'
    cleaned_context = re.sub(r'\* ', '', summarized_context)  # Remove '* '
    cleaned_context = re.sub(r'\*', '', summarized_context)  # Remove '*'
    cleaned_context = re.sub(r':\**', ': ', summarized_context)
    cleaned_context = re.sub(r':\*', ': ', summarized_context)

    return cleaned_context

# Split ExecRep context and ExecRep context in response
def split_response(cleaned_context):
    parts = cleaned_context.split("Subject: Recruitment Report for ", 1)  # Split only at the first occurrence
    if len(parts) == 1:
        raise ValueError("Report text doesn't contain the split marker.")

    return {
        "ExecRep Context": parts[0].rstrip(),  # Remove trailing whitespace
        "Email Context": "Subject: Recruitment Report for " + parts[1].strip()  # Re-add the split marker and remove leading/trailing whitespace
    }

# Function to save formatted text to a PDF
def save_text_as_pdf(input_context, output_path):

    # Create an instance of FPDF class with A4 page size
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("times", size=8)

    # Set margins: left, top, right (bottom is handled automatically)
    pdf.set_left_margin(15)
    pdf.set_top_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=10)
    
    # Add the processed text to the PDF
    pdf.multi_cell(0, 2, input_context)  # cell_width set to 0 to use the full page width (within margins)
    
    # Save the PDF to the specified output path
    pdf.output(output_path)

# Main function to run the JSON file selection and processing
def main():
    num_files = ask_number_of_files()

    if num_files:
        file_paths = select_json_files(num_files)

        if len(file_paths) == num_files:
            print(f"Selected files: {file_paths}")
        
        try:
            json_array = []

            # Loop through each file to extract text and save as a chunk
            for i, file_path in enumerate(file_paths):
                print(f"\nProcessing file {i+1}/{len(file_paths)}: {file_path}")
                json_context = process_json_files(file_path)
                json_array.append(json_context)

            # Define specific prompts for each text (customize as needed)
            prompt = """
                Retrieve the following information:
                    - Report Type, Project Name, Project Level
                    - Candidate ID, Candidate Email , Candidate name, Overall Average
                    - All competencies and their sten, exclude Cognitive Tools Percentile
                    - All sub-competencies belong to each of the 3 main competencies and their sten
                    - 3 motivating factors with highest score as motivators
                    - 3 motivating factors with lowest score demotivators
                    - 3 work related behaiviours with highest score

                For each of the sub-competencies in the {Main Competency 1} section:
                    - Summarize their comments in score description, implications, and development tips into a paragraph less than or equal to 24 words.
                    - Retrieve one important question from the cbi questions section for each of the sub-competencies in this section, excluding sub-questions.
                    - Replace all (Name) with Candidate

                For each of the sub-competencies in the {Main Competency 2} section:
                    - Summarize their comments in description into a sentence less than or equal to 20 words.
                    - For each of the 3 breakdowns in sub-competency 2, retrieve their sten and summarize their score description in less than 20 words.
                    - Replace all (Name) with Candidate

                For each of the sub-competencies in the {Main Competency 3} section:
                    - Summarize category description for low if the sten of that sub-competency is 5 or lower in 20 words.
                    - Summarize category description for high if the sten of that sub-competency is 6 or higher in 20 words.
                    - Replace all (Name) with Candidate

                Analyze the full json context to suggest 3 possible derailers of the candidate with a brief description in less than or equal to 24 words.
                
                Lastly, summarize your generated response into a shorter version in email format with essential details.

                Must structure the output as below:

                Report Type: {Report Type}                      Project Name: {Project Name}                    Project Level: {Project Level}
                Candidate Name: {Candidate Name}                Candidate ID: {Candidate ID}                Candidate Email: {Candidate Email}
                
                Overall Average: {Overall Average}
                {Main Competency 1}: {Main Competency 1's Sten}
                    + {Main Competency 1's sub-competecy 1}: {Main Competency 1's sub-competecy 1's Sten}
                    + {Main Competency 1's sub-competecy 2}: {Main Competency 1's sub-competecy 2's Sten}
                    Continue to add remaining {Main Competency 1}'s sub-competecies.
                {Main Competency 2}: {Main Competency 2's Sten}
                    + {Main Competency 2's sub-competecy 1}: {Main Competency 2's sub-competecy 1's Sten}
                    + {Main Competency 2's sub-competecy 2}: {Main Competency 2's sub-competecy 2's Sten}
                Stop here.
                {Main Competency 3}: {Main Competency 3's Sten}
                    + {Main Competency 3's sub-competecy 1}: {Main Competency 3's sub-competecy 1's Sten}
                    + {Main Competency 3's sub-competecy 2}: {Main Competency 3's sub-competecy 2's Sten}
                Ignore the None for {Main Competency 3's Sten} and continue to add remaining {Main Competency 3}'s sub-competecies.
                
                Motivators: {motivator 1, motivator 2, motivator 3}
                Demotivators: {demotivator 1, demotivator 2, demotivator 3}
                Preferable work styles: {work related behaviour 1, work related behaviour 2, work related behaviour 3}

                {Main Competency 1}
                {Main Competency 1's sub-competecy 1}: Summarized paragraph.
                CBI Question: {Most Important Main Question from CBI Question}
                Continue to add remaining sub-competencies in the {Main Competency 1} section using the format above.

                {Main Competency 2}
                {Main Competency 2's sub-competecy 1}: Summarized comment paragraph.
                {Main Competency 2's sub-competecy 2}: Summarized comment paragraph.
                    + {Main Competency 2's sub-competecy 2's Breakdown 1} ({Sten}): Summarized paragraph of breakdown.
                    + {Main Competency 2's sub-competecy 2's Breakdown 2} ({Sten}): Summarized paragraph of breakdown.
                    + {Main Competency 2's sub-competecy 2's Breakdown 3} ({Sten}): Summarized paragraph of breakdown.

                {Main Competency 3}
                {Main Competency 3's sub-competecy 1}: Summarized definition and comment.
                Continue to add remaining sub-competencies in the {Main Competency 3} section using the format above.
                
                Possible derailers
                1. {Derailer 1 Title}: {Brief Description}
                2. {Derailer 2 Title}: {Brief Description}
                3. {Derailer 3 Title}: {Brief Description}

                Subject: Recruitment Report for {Candidate Name}

                Dear Hiring Manager,
                this email summarizes the assessment results for candidate {Candidate Name}. 
                
                Overall score: {Overall Average}
                
                {Main Competency 1}: {Main Competency 1's Sten}
                {Main Competency 2}: {Main Competency 2's Sten}
                {Main Competency 3}: {Main Competency 3's Sten}

                Key Highlights:
                Strengths: {From your response}
                Areas for Development: {From your response}
                Possible Derailers: {From your response}

                Motivators: {From your response}
                Demotivators: {From your response}
                Preferable Work Styles: {From your response}

                For a detailed analysis of his/her sub skills and other components,
                please review his/her Executive Report or Full Report attached to this email.

                Thank you for using our product.

                Best regards,
                Accendo Technologies
            """

            for i, json_context in enumerate(json_array):
                summarized_context = generate_summary(json_context, prompt)
                cleaned_context = clear_GenAI_format(summarized_context)
                splitted_context = split_response(cleaned_context)
                ExecRep_Context = splitted_context["ExecRep Context"]
                print(ExecRep_Context)
                Email_Context = splitted_context["Email Context"]
                print(Email_Context)

                # Save summarized report as PDF
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                ExecRep_name = f"ExecRep AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.pdf"
                ExecRep_pdf_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', ExecRep_name)
                save_text_as_pdf(ExecRep_Context, ExecRep_pdf_path)
                print(f"\nSummary saved to: {ExecRep_pdf_path}")

                Email_name = f"Email AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.pdf"
                Email_pdf_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', Email_name)
                save_text_as_pdf(Email_Context, Email_pdf_path)
                print(f"\nSummary saved to: {Email_pdf_path}")
                
        except FileNotFoundError as e:
            print(f"\nError: File '{e.filename}' not found.")
        
        except json.JSONDecodeError as e:
            print(f"\nError: Invalid JSON format in file '{e.filename}'.")
        
        return None  # Return None if an error occurs

    else:
        print("\nNo file selected.")

if __name__ == "__main__":
    main()