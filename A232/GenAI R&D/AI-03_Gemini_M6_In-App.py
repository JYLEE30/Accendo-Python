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
        with open(file_path, 'r', encoding='utf-8') as file:
            context = json.load(file)
            return context
    except FileNotFoundError:
        print(f"\nError: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"\nError: Invalid JSON format in file '{file_path}'.")

# Summarize the given text chunk using gemini model with a specific prompt and full context
def generate_summary(json_input, input, output_sample, retries=3, delay=5):
    
    # Set up Generative AI API
    for attempt in range(retries):
        try:
            # Set up Generative AI API
            genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            full_prompt = f"Input:{input}\n\nContext:{json_input}\n\nOutput Sample:{output_sample}"
            print(full_prompt)
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
    cleaned_context10 = re.sub('\u2022', '', cleaned_context9)  # This removes the ZWNJ character
    cleaned_context11 = re.sub('\u2013', '', cleaned_context10)  # This removes the ZWNJ character
    cleaned_context = re.sub(r':\*', ': ', cleaned_context11)
    return cleaned_context

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
    pdf.set_font("Arial", size=8)

    # Set margins: left, top, right (bottom is handled automatically)
    pdf.set_left_margin(10)
    pdf.set_top_margin(10)
    pdf.set_right_margin(10)
    pdf.set_auto_page_break(auto=True, margin=10)

    # Convert the text to UTF-8 encoding
    utf8_text = input_context.encode('utf-8', 'replace').decode('utf-8')
    
    # Add the processed text to the PDF
    pdf.multi_cell(0, 5, utf8_text)  # cell_width set to 0 to use the full page width (within margins)
    
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
            input = """
                (1) Can you pinpoint the report details (Type, Project Name, Level) and candidate info (ID, Email, Name)?
                (2) Prerequisite:
                    - You're a recruiter analyzing a candidate's assessment for hiring.
                    - sten score (not sten9 or sten5): 1-10 scale, avg 5.5, SD 2. Low group (1-3): 16%, Medium group (4-7): 68%, High group (8-10): 16%
                    - Do not use the (Name), keep it very concise and short, remove filler words like "a" or "the". Example: instead of "The candidate values transparency and open communication" write "Values transparency and open communication".
                (3) Analysis:
                    A. Strengths: Can you pinpoint the 3 competencies with the highest sten score and arrange them from highest to lowest?
                    B. Derailers: Can you pinpoint the 3 competencies with extreme sten score (Low or High), 2 competencies from Low group with lowest sten score, 1 competency from High group with highest sten score? (Leave it blank if no competencies fit the condition)
                    C. CBI Questions: 3 questions from Leadership's sub-competencies, 2 based on lowest and 1 based on highest. Try addressing several competencies in one question if the scores are the same.
                    D. Onboarding Plan: 3 strategies based on Learning Agility and Cognitive Ability score's level.
                (4) Can you pinpoint the top 3 motivators, demotivators, and work-related behaviors?
                (5) Leadership competency:
                    - Analyze sub-competencies' descriptions, scores, implications, and tips.
                    - Provide 2-3 bullet-point concise summary for each sub-competency, prioritize bullet-points by relevance.
                (6) Agility competency:
                    A. Learning Agility: Analyze description, score, implications, and tips.
                        - Bullet-point 1 explaining how willing candidate is to learn.
                        - Bullet-point 2 explaining the first bullet-point considering the score level.
                    B. Cognitive Ability: Summarize the key insights of the sub-components (Inductive-Logical, Numerical, Verbal Reasoning).
                        - Bullet-point 1 explain the summary.
                        - Bullet-point 2 explain what it means for learning speed.
                (7) Cultural Fit competency:
                    - Analyze sub-competencies' descriptions and scores.
                    - Provide 2-3 bullet-point concise summary for each sub-competency, prioritize bullet-points by relevance.
                    - The summary should describe the how well the candidate's behaviour will fit into the working environment.
            """
            
            output_sample = """
                Report Type: {Report Type}
                Project Name: {Project Name}
                Project Level: {Project Level}

                Candidate Name: {Candidate Name}
                Candidate ID: {Candidate ID}
                Candidate Email: {Candidate Email}

                KEY HIGHLIGHTS

                Strengths:
                - {Sub-competency addressed}: {Strength 1}
                - {Sub-competency addressed}: {Strength 2}
                - {Sub-competency addressed}: {Strength 3}

                Possible Derailers:
                - {Derailer 1 title}: {Brief description of why this is a potential risk or challenge}
                - {Derailer 2 title}: {Brief description of why this is a potential risk or challenge}
                - {Derailer 3 title}: {Brief description of why this is a potential risk or challenge}

                CBI Questions:
                - {Sub-competency addressed}: {CBI Question 1}
                - {Sub-competency addressed}: {CBI Question 2}
                - {Sub-competency addressed}: {CBI Question 3}

                Onboarding Plans:
                - {Onboarding Plan 1}
                - {Onboarding Plan 2}
                - {Onboarding Plan 3}
                
                Motivators:
                - {Motivator 1}
                - {Motivator 2}
                - {Motivator 3}

                Demotivators:
                - {Demotivator 1}
                - {Demotivator 2}
                - {Demotivator 3}

                Preferable work styles:
                - {Work related behavior 1}
                - {Work related behavior 2}
                - {Work related behavior 3}

                LEADERSHIP - {Leadership's sten}
                + {Leadership's sub-competency 1's name}: {Leadership's sub-competency 1's sten}
                    • {Leadership's sub-competency 1's bullet point 1}
                    • {Leadership's sub-competency 1's bullet point 2}
                    • {Leadership's sub-competency 1's bullet point 3}
                Continue to add remaining sub-competencies of Leadership.

                AGILITY - {Agility's sten}
                + Learning Agility ({Learning Agility's sten}):
                    • {Learning Agility's bullet point 1}
                    • {Learning Agility's bullet point 2}
                + Cognitive Ability ({Cognitive Ability's sten}):
                    • {Cognitive Ability's bullet point 1}
                    • {Cognitive Ability's bullet point 2}
                    • {Cognitive Ability's bullet point 3}

                CULTURAL FIT - {Cultural Fit's sten}
                + {Cultural Fit's sub-competency 1's name}: {Cultural Fit's sub-competency 1's sten}
                    • {Cultural Fit's sub-competency 1's bullet point 1}
                    • {Cultural Fit's sub-competency 1's bullet point 2}
                Continue to add remaining sub-competencies of Cultural Fit.
            """

            for i, json_context in enumerate(json_array):
                try:
                    generated_summary = generate_summary(json_context, input, output_sample, retries=3, delay=5)
                except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
                    print(f"Failed to generate summary after retries: {e}")
                    continue

                cleaned_context = clear_GenAI_format(generated_summary)
                
                # Generate JSON
                try:
                    json_InApp_Gen = generate_json(cleaned_context, retries=3, delay=5)
                except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
                    print(f"Failed to generate JSON for InApp context after retries: {e}")
                    continue
                
                 # Cleaned and Parsed as JSON format
                parsed_json_InApp = clean_and_parse_json(json_InApp_Gen)

                # Print out each parsed JSON object
                for parsed_json in parsed_json_InApp:
                    print("\n" + json.dumps(parsed_json, indent=4))  # Print the parsed JSON with indentation for readability

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Save summarized context as PDF
                InApp_pdf_name = f"InApp AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.pdf"
                InApp_pdf_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\(1) Accendo\Executive Report\Sample Report', InApp_pdf_name)
                save_text_as_pdf(cleaned_context, InApp_pdf_path)

                print(f"InApp PDF saved to: {InApp_pdf_path}")

                # Save summarized context as JSON
                InApp_json_name = f"InApp AI-03 Google_Gemini-1.5-Flash-Latest_M4_{timestamp}.json"
                InApp_json_path = os.path.join(r'C:\Users\leeji\OneDrive\Desktop\(1) Accendo\Executive Report\Sample Report', InApp_json_name)
                save_text_as_json(parsed_json_InApp, InApp_json_path)

                print(f"InApp JSON saved to: {InApp_json_path}")
                
        except FileNotFoundError as e:
            print(f"\nError: File '{e.filename}' not found.")
        
        except json.JSONDecodeError as e:
            print(f"\nError: Invalid JSON format in file '{e.filename}'.")
        
        return None  # Return None if an error occurs

    else:
        print("\nNo file selected.")

if __name__ == "__main__":
    main()