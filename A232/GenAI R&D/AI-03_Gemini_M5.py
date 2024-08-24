# Import required libraries
import tkinter as tk
from tkinter import simpledialog, filedialog
import json
import time
import google.api_core.exceptions
import google.generativeai as genai
import re
import datetime
import os
from fpdf import FPDF

# Ask how many JSON files to processSubject
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
def generate_summary(json_input, prompt, retries=3, delay=5):
    
    # Set up Generative AI API
    for attempt in range(retries):
        try:
            # Set up Generative AI API
            genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            full_prompt = f"Full document context:\n\n{json_input}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            return response.text
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            print(f"Attempt {attempt + 1} to generate summary failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise

# Replace leading asterisks and hashes with dashes or remove them
def clear_GenAI_format(generated_summary):
    cleaned_context1 = re.sub(r'\#\#\# (.*)', r'\1', generated_summary)  # Remove '###'
    cleaned_context2 = re.sub(r'\#\# (.*)', r'\1', cleaned_context1)  # Remove '##'
    cleaned_context3 = re.sub(r'\* \**', '', cleaned_context2)  # Remove '* **'
    cleaned_context4 = re.sub(r'\*\*', '', cleaned_context3)  # Remove '**'
    cleaned_context5 = re.sub(r'\**', '', cleaned_context4)  # Remove '**'
    cleaned_context6 = re.sub(r'\* ', '', cleaned_context5)  # Remove '* '
    cleaned_context7 = re.sub(r'\*', '', cleaned_context6)  # Remove '*'
    cleaned_context8 = re.sub(r':\**', ': ', cleaned_context7)
    cleaned_context9 = re.sub('\u200c', '', cleaned_context8)  # This removes the ZWNJ character
    cleaned_context = re.sub(r':\*', ': ', cleaned_context9)
    return cleaned_context

# Split ExecRep context and ExecRep context in response
def split_response(cleaned_context):
    # Split into three parts: before "In-App", "In-App" to before "Subject:", and after "Subject:"
    parts = cleaned_context.split("In-App", 1)
    if len(parts) < 2:
        raise ValueError("Report text doesn't contain 'In-App' section.")

    # Split second part into email context and subject
    InApp_part, Remaining_part = parts[1], parts[0]
    Email_part = InApp_part.split("Subject:", 1)
    if len(Email_part) < 2:
        raise ValueError("Report text doesn't contain 'Subject:'.")

    return {
        "ExecRep Context": Remaining_part.strip(),  # ExecRep Context is before "In-App"
        "InApp Context": Email_part[0].strip(),  # InApp Context is from "In-App" to before "Subject:"
        "Email Context": "Subject: " + Email_part[1].strip()  # Email Context starts with "Subject:"
    }

# Summarize the given text chunk using gemini model with a specific prompt and full context
def generate_json(separated_context, retries=3, delay=5):
    
    # Set up Generative AI API
    for attempt in range(retries):
        try:
            # Set up Generative AI API
            genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            full_prompt = f"Change the following text into a usable json format:\n\n{separated_context}"
            context_json = model.generate_content(full_prompt)
            return context_json.text
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            print(f"Attempt {attempt + 1} to generate JSON failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise

# Reformat JSON and parse multiple JSON objects
def clean_and_parse_json(json_Gen):
    # Clean the JSON string by removing leading/trailing characters and newlines
    cleaned_json_head = json_Gen.strip('```json')
    cleaned_json_tail = cleaned_json_head.replace('```', '').strip()
    cleaned_json = cleaned_json_tail.replace('\n', '')
    # Split the cleaned JSON string into individual JSON objects if necessary
    json_objects = cleaned_json.split('\n')

    parsed_json_objects = []
    for json_str in json_objects:
        try:
            parsed_json = json.loads(json_str)
            parsed_json_objects.append(parsed_json)
        except json.JSONDecodeError as e:
            print(f"\nError: Invalid JSON format: {e}")

    return parsed_json_objects

# Function to save formatted text to a JSON
def save_text_as_json(json_context, output_path):
    # Save the response as a JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_context, json_file, ensure_ascii=False, indent=4)

# Function to save formatted text to a PDF
def save_text_as_pdf(input_context, output_path):
    # Create an instance of FPDF class with A4 page size
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("times", size=8)

    # Set margins: left, top, right (bottom is handled automatically)
    pdf.set_left_margin(10)
    pdf.set_top_margin(10)
    pdf.set_right_margin(10)
    pdf.set_auto_page_break(auto=True, margin=10)
    
    # Add the processed text to the PDF
    pdf.multi_cell(0, 5, input_context)  # cell_width set to 0 to use the full page width (within margins)
    
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
                (1) Retrieve the following information:
                    - Report Type, Project Name, Project Level
                    - Candidate ID, Email, Name, Overall Average
                    - All competencies and their sten (exclude Cognitive Tools Percentile)
                    - All sub-competencies under the 3 main competencies and their sten
                    - Top 3 motivators, bottom 3 demotivators
                    - Top 3 work-related behaviors
                (2) For each sub-competency in main competency 1 section,
                    - summarize comments (score description, implications, development tips) in 18 words
                    - retrieve and summarize one key question from CBI questions in 10 words, excluding sub-questions
                    - replace all (Name) with Cand
                (3) For each sub-competency in main competency 2 section,
                    - summarize comments in 18 words
                    - for each breakdown in sub-competency 2, retrieve sten and summarize score description in 18 words
                    - replace all (Name) with Cand
                (4) For each sub-competency in main competency 3 section,
                    - summarize category description in 18 words for low if sten less than or equal to 5
                    - summarize category description in 18 words for high if sten greater than or equal to 6
                    - replace all (Name) with Cand
                (5) Analyze the full JSON context to suggest 3 possible derailers with brief descriptions in 18 words
                (6) Summarize each response in (2) and (4) into a point form with essential details and print with the format mentioned below
                    - Focus on explaining the candidate's strength and weakness based on each of their sub-competencies in (2), (3), (4) and (5)
                    - Use the same response in (1), just exclude the sub-competencies
                    - Use the same response in (3) and (5)
                    - replacing all (Name) with Cand
                (7) Summarize the response into a shorter email format with essential details, replace all (Name) with Cand

                Format (1) output as below: (Don't add section header on your own)
                Report Type: {Report Type}
                Project Name: {Project Name}
                Project Level: {Project Level}

                Candidate Name: {Candidate Name}
                Candidate ID: {Candidate ID}
                Candidate Email: {Candidate Email}
                
                Overall Average: {Overall Average}
                {Main Competency 1's name}: {Main Competency 1's sten}
                    + {Main Competency 1's sub-competecy 1's name}: {Main Competency 1's sub-competecy 1's sten}
                    Continue to add remaining sub-competecies of main competency 1.
                {Main Competency 2's name}: {Main Competency 2's sten}
                    + {Main Competency 2's sub-competecy 1's name}: {Main Competency 2's sub-competecy 1's sten}
                    + {Main Competency 2's sub-competecy 2's name}: {Main Competency 2's sub-competecy 2's sten}
                End here for main competency 2, exclude breakdown in cognitive ability
                {Main Competency 3's name}: {Main Competency 3's sten}
                    + {Main Competency 3's sub-competecy 1's name}: {Main Competency 3's sub-competecy 1's sten}
                Ignore the None of main competency 3's sten and continue to add remaining sub-competecies of main competency 3.
                
                Motivators: {motivator 1, motivator 2, motivator 3}
                Demotivators: {demotivator 1, demotivator 2, demotivator 3}
                Preferable work styles: {work related behaviour 1, work related behaviour 2, work related behaviour 3}

                Format (2) output as below: (Don't add section header on your own)
                {Main Competency 1's name}
                {Main Competency 1's sub-competecy 1's name}: Summarized paragraph.
                CBI Question: {Most Important Main Question from CBI Question}
                Continue to add remaining sub-competencies in the {Main Competency 1} section and Main Question from CBI Question using the format above.

                Format (3) output as below: (Don't add section header on your own)
                {Main Competency 2's name}
                {Main Competency 2's sub-competecy 1's name}: Summarized comment paragraph.
                {Main Competency 2's sub-competecy 2's name}: Summarized comment paragraph.
                    + {Main Competency 2's sub-competecy 2's Breakdown 1's name} ({Sten}): Summarized paragraph of breakdown.
                    + {Main Competency 2's sub-competecy 2's Breakdown 2's name} ({Sten}): Summarized paragraph of breakdown.
                    + {Main Competency 2's sub-competecy 2's Breakdown 3's anme} ({Sten}): Summarized paragraph of breakdown.

                Format (4) output as below: (Don't add section header on your own)
                {Main Competency 3's name}
                {Main Competency 3's sub-competecy 1's name}: Summarized definition and comment.
                Continue to add remaining sub-competencies in the {Main Competency 3} section using the format above.
                
                Format (5) output as below: (Don't add section header on your own)
                Possible derailers
                1. {Derailer 1 Title}: {Brief Description}
                2. {Derailer 2 Title}: {Brief Description}
                3. {Derailer 3 Title}: {Brief Description}

                Format (6) output as below: (Don't add section header on your own)
                In-App
                Report Type: {Report Type}
                Project Name: {Project Name}
                Project Level: {Project Level}
                
                Candidate Name: {Candidate Name}
                Candidate ID: {Candidate ID}
                Candidate Email: {Candidate Email}
                
                Overall Average: {Overall Average}
                {Main Competency 1's name}: {Main Competency 1's sten}
                {Main Competency 2's name}: {Main Competency 2's sten}
                {Main Competency 3's name}: {Main Competency 3's sten}

                Key Highlights:
                Strengths: {From your response} in 20 words
                Areas for Development: {From your response} in 20 words
                
                Possible derailers
                1. {Derailer 1 Title}: {Brief Description}
                2. {Derailer 2 Title}: {Brief Description}
                3. {Derailer 3 Title}: {Brief Description}

                Motivators: {motivator 1, motivator 2, motivator 3}
                Demotivators: {demotivator 1, demotivator 2, demotivator 3}
                Preferable work styles: {work related behaviour 1, work related behaviour 2, work related behaviour 3}

                {Main Competency 1's name}
                Summarized paragraph of (2)

                {Main Competency 2's name}
                {Main Competency 2's sub-competecy 1's name}: Summarized comment paragraph.
                {Main Competency 2's sub-competecy 2's name}: Summarized comment paragraph.
                    + {Main Competency 2's sub-competecy 2's Breakdown 1's name} ({Sten}): Summarized paragraph of breakdown.
                    + {Main Competency 2's sub-competecy 2's Breakdown 2's name} ({Sten}): Summarized paragraph of breakdown.
                    + {Main Competency 2's sub-competecy 2's Breakdown 3's anme} ({Sten}): Summarized paragraph of breakdown.

                {Main Competency 3's name}
                Summarized paragraph of (4)

                Format (7) output as below: (Don't add section header on your own)
                Subject: Recruitment Report for {Candidate Name}

                Dear Hiring Manager,
                this email summarizes the assessment results for candidate {Candidate Name}. 
                
                Overall score: {Overall Average}
                
                {Main Competency 1's name}: {Main Competency 1's sten}
                {Main Competency 2's name}: {Main Competency 2's sten}
                {Main Competency 3's name}: {Main Competency 3's sten}

                Key Highlights:
                Strengths: {From your response} in 10 words
                Areas for Development: {From your response} in 10 words
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
                try:
                    generated_summary = generate_summary(json_context, prompt, retries=3, delay=5)
                except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
                    print(f"Failed to generate summary after retries: {e}")
                    continue

                cleaned_context = clear_GenAI_format(generated_summary)
                splitted_context = split_response(cleaned_context)

                # Get splitted context
                ExecRep_Context = splitted_context["ExecRep Context"]
                InApp_Context = splitted_context["InApp Context"]
                Email_Context = splitted_context["Email Context"]

                # Generate JSON
                try:
                    json_ExecRep_Gen = generate_json(ExecRep_Context, retries=3, delay=5)
                except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
                    print(f"Failed to generate JSON for ExecRep context after retries: {e}")
                    continue

                try:
                    json_InApp_Gen = generate_json(InApp_Context, retries=3, delay=5)
                except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
                    print(f"Failed to generate JSON for InApp context after retries: {e}")
                    continue

                try:
                    json_Email_Gen = generate_json(Email_Context, retries=3, delay=5)
                except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
                    print(f"Failed to generate JSON for Email context after retries: {e}")
                    continue

                # Cleaned and Parsed as JSON format
                parsed_json_ExecRep = clean_and_parse_json(json_ExecRep_Gen)
                parsed_json_InApp = clean_and_parse_json(json_InApp_Gen)
                parsed_json_Email = clean_and_parse_json(json_Email_Gen)

                # Print out each parsed JSON object
                for parsed_json in parsed_json_ExecRep:
                    print("\n" + json.dumps(parsed_json, indent=4))  # Print the parsed JSON with indentation for readability
                
                for parsed_json in parsed_json_InApp:
                    print("\n" + json.dumps(parsed_json, indent=4))  # Print the parsed JSON with indentation for readability
                
                for parsed_json in parsed_json_Email:
                    print("\n" + json.dumps(parsed_json, indent=4))  # Print the parsed JSON with indentation for readability

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Save summarized context as PDF
                ExecRep_pdf_name = f"ExecRep AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.pdf"
                ExecRep_pdf_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', ExecRep_pdf_name)
                save_text_as_pdf(ExecRep_Context, ExecRep_pdf_path)

                InApp_pdf_name = f"InApp AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.pdf"
                InApp_pdf_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', InApp_pdf_name)
                save_text_as_pdf(InApp_Context, InApp_pdf_path)

                Email_pdf_name = f"Email AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.pdf"
                Email_pdf_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', Email_pdf_name)
                save_text_as_pdf(Email_Context, Email_pdf_path)

                print(f"\nExecRep PDF saved to: {ExecRep_pdf_path}")
                print(f"InApp PDF saved to: {InApp_pdf_path}")
                print(f"Email PDF saved to: {Email_pdf_path}")

                # Save summarized context as JSON
                ExecRep_json_name = f"ExecRep AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.json"
                ExecRep_json_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', ExecRep_json_name)
                save_text_as_json(parsed_json_ExecRep, ExecRep_json_path)
                
                InApp_json_name = f"InApp AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.json"
                InApp_json_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', InApp_json_name)
                save_text_as_json(parsed_json_InApp, InApp_json_path)

                Email_json_name = f"Email AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.json"
                Email_json_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\Production', Email_json_name)
                save_text_as_json(parsed_json_Email, Email_json_path)

                print(f"\nExecRep JSON saved to: {ExecRep_json_path}")
                print(f"InApp JSON saved to: {InApp_json_path}")
                print(f"Email JSON saved to: {Email_json_path}")

        except FileNotFoundError as e:
            print(f"\nError: File '{e.filename}' not found.")
        
        except json.JSONDecodeError as e:
            print(f"\nError: Invalid JSON format in file '{e.filename}'.")
        
        return None  # Return None if an error occurs

    else:
        print("\nNo file selected.")

if __name__ == "__main__":
    main()