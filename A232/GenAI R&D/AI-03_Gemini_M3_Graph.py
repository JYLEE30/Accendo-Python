# Import required libraries
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import os
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import google.generativeai as genai
import datetime
from fpdf import FPDF
import re

# Open a file dialog to select a PDF file.
# Returns the file path if a file is selected, otherwise returns None.
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_path

# Extract text from a specific page in the PDF
def extract_text_from_range(pdf, start_page, end_page):
    text = ""
    for page_num in range(start_page - 1, end_page):  # Page numbers are 0-based in PyMuPDF
        page = pdf[page_num]
        text += page.get_text() + "\n"
    
    return text

def extract_chunks(file_path, chunks):
    extracted_chunks = {chunk: "" for chunk in chunks}
    # Open the PDF file
    pdf_document = fitz.open(file_path)
    # Extract text for each defined chunk
    for chunk_name, page_ranges in chunks.items():
        for start_page, end_page in page_ranges:
            extracted_chunks[chunk_name] += extract_text_from_range(pdf_document, start_page, end_page)
    # Close the PDF document
    pdf_document.close()
    
    return extracted_chunks

# Summarize the given text chunk using gemini model with a specific prompt and full context
def generate_summary(full_text, text_chunk, prompt):
    
    # Set up Generative AI API
    genai.configure(api_key="AIzaSyCsDH3BueKT9Eu-gPnne7I7wzaQqqgoCVU")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    context_prompt = f"Full document context:\n\n{full_text}\n\nSpecific section:\n\n{text_chunk}\n\n{prompt}"
    response = model.generate_content(context_prompt)
    
    return response.text

# Function to generate the radar chart and save it as an image
def generate_radar_chart(candidate, average, categories, output_dir):
    
    N = len(categories)

    plt.rcParams['font.family'] = 'Times New Roman'

    # What will be the angle of each axis in the plot? (we divide the plot / number of variables)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Append the first value to the end to close the circle
    candidate += candidate[:1]
    average += average[:1]

    # Initialise the spider plot
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=12)

    # Draw y-labels
    plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], color="grey", size=8)
    plt.ylim(0, 10)

    # Plot data
    ax.plot(angles, candidate, linewidth=2, linestyle='solid', label='Candidate', color='blue')
    ax.fill(angles, candidate, 'b', alpha=0.1)

    ax.plot(angles, average, linewidth=2, linestyle='solid', label='Average below 90th percentile', color='red')
    ax.fill(angles, average, 'r', alpha=0.1)

    # Add a legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.45, 0.07))

    # Add labels for each point slightly away from the actual points
    label_offset = 0.5
    for i in range(N):
        angle_rad = angles[i]

        candidate_x = (candidate[i] + label_offset) * np.cos(angle_rad)
        candidate_y = (candidate[i] + label_offset) * np.sin(angle_rad)
        plt.text(angle_rad, candidate[i] + label_offset, str(candidate[i]), horizontalalignment='center', size=16, color='blue', weight='semibold')

        average_x = (average[i] + label_offset) * np.cos(angle_rad)
        average_y = (average[i] + label_offset) * np.sin(angle_rad)
        plt.text(angle_rad, average[i] + 2 * label_offset, str(average[i]), horizontalalignment='center', size=16, color='red', weight='semibold')

    # Save the radar chart as an image
    plt.title('Candidate vs Average below 90th percentile Performance', size=16, weight='bold', y=1.1)
    chart_path = os.path.join(output_dir, "radar_chart.png")
    plt.savefig(chart_path, dpi=600, bbox_inches='tight')
    plt.close()  # Close the plot to prevent display

    return chart_path

# Function to save text as a PDF
def save_text_as_pdf(text, output_path, chart_path):
    
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
    text = re.sub(r':\**', ': ', text)
    text = re.sub(r':\*', ': ', text)

    # Add the processed text to the PDF
    pdf.multi_cell(0, 5, text)  # cell_width set to 0 to use the full page width (within margins)

    # Add the radar chart as an image
    pdf.image(chart_path, x=pdf.get_x(), y=pdf.get_y() + 10, w=90)
    
    # Save the PDF to the specified output path
    pdf.output(output_path)

# Main function to run the PDF text extraction and summarization process
def main():
    
    file_path = select_pdf_file()

    if file_path:
        print(f"Selected file: {file_path}")

        try:
            # Define the page ranges to extract for each chunk
            chunks = {
                "Chunk_1": [(1, 1), (3, 3), (12, 12)],
                "Chunk_2": [(4, 7), (13, 17)],
                "Chunk_3": [(8, 9)],
                "Chunk_4": [(10, 10)],
            }
            
            # Extract the chunks
            extracted_chunks = extract_chunks(file_path, chunks)
            full_text = "\n".join(extracted_chunks.values())  # Combine all chunks for full context
            
            # Output the extracted text for each chunk
            for chunk_name, text in extracted_chunks.items():
                print(f"\n{chunk_name}:\n\n{text}{'-'*40}")
            
            # Define specific prompts for each chunk (customize as needed)
            prompts = {
                "Chunk_1": """
                    Extract the following information:
                    - Report name
                    - Candidate's name
                    - Overall score
                    - 3 main elements and their scores
                    - Sub-elements of the 3 main elements and their scores in 'Quickview'
                    - Most motivated by
                    - Least motivated by
                    - 3 work styles with highest scores

                    Format the output as below:
                    {Report Name}
                    Candidate Name: {Candidate Name}
                    Overall Score: {Overall Score}

                    {Main Element 1}: {Main Element 1's Score}
                            + {Main Element 1's sub-element 1}: {Main Element 1's sub-element 1 Score}
                            + {Main Element 1's sub-element 2}: {Main Element 1's sub-element 2 Score}
                            + {Main Element 1's sub-element 3}: {Main Element 1's sub-element 3 Score}
                            + {Main Element 1's sub-element 4}: {Main Element 1's sub-element 4 Score}
                    {Main Element 2}: {Main Element 2's Score}
                            + {Main Element 2's sub-element 1}: {Main Element 2's sub-element 1 Score}
                            + {Main Element 2's sub-element 2}: {Main Element 2's sub-element 2 Score}
                    {Main Element 3}: {Main Element 3's Score}
                            + {Main Element 3's sub-element 1}: {Main Element 3's sub-element 1 Score}
                            + {Main Element 3's sub-element 2}: {Main Element 3's sub-element 2 Score}
                            + {Main Element 3's sub-element 3}: {Main Element 3's sub-element 3 Score}
                    
                    Most motivated by: {Most motivated by 1, Most motivated by 2, Most motivated by 3}
                    Least motivated by: {Least motivated by 1, Least motivated by 2, Least motivated by 3}

                    Preferable work styles: {Work style 1, Work style 2, Work style 3}
                    """,
                "Chunk_2": """
                    For each of the sub-elements in the {Main Element 1} section:
                    - Summarize the comment in the "About the Candidate" section and the implications as a single paragraph in less than or equal to 36 words.
                    - Retrieve only the most important main question to ask the candidate from the CBI section for each of the sub-elements in the {Main Element 1} section, excluding sub-questions.

                    Format the output as follows:
                    {Main Element 1}
                    {Main Element 1's sub-element 1}: {Summary of Comment in the "About the Candidate" Section and Implications}
                    CBI Question: {Most Important Main Question from CBI Section}
                        
                    {Main Element 1's sub-element 2}: {Summary of Comment in the "About the Candidate" Section and Implications}
                    CBI Question: {Most Important Question from CBI Section}
                        
                    {Main Element 1's sub-element 3}: {Summary of Comment in the "About the Candidate" Section and Implications}
                    CBI Question: {Most Important Question from CBI Section}
                        
                    {Main Element 1's sub-element 4}: {Summary of Comment in the "About the Candidate" Section and Implications}
                    CBI Question: {Most Important Question from CBI Section}
                    """,
                "Chunk_3": """
                    For each of the sub-elements in the {Main Element 2} section:
                    - Summarize the comment in the "About You" section in less than or equal to 30 words.

                    For each of the 3 breakdowns in the {Main Element 2's sub-element 2} Breakdown:
                    - Retrieve their scores and Summarize their definition and comment in the "About You" section as a single paragraph in less than 22 words.

                    Format the output as follows:
                    {Main Element 2}
                    {Main Element 2's sub-element 1}: {Summary of "About You" Comments}
                    
                    {Main Element 2's sub-element 2}: {Summary of "About You" Comments}. {Main Element 2's sub-element 2} breakdown:
                    {Breakdown 1}  ({Breakdown 1's Score}): {Summary of Definition and "About You" Comments}
                    {Breakdown 2}  ({Breakdown 2's Score}): {Summary of Definition and "About You" Comments}
                    {Breakdown 3}  ({Breakdown 3's Score}): {Summary of Definition and "About You" Comments}
                    """,
                "Chunk_4": """
                    For each of the sub-elements in the {Main Element 3} section:
                    - Retrieve their scores.
                    - Summarize their definition and comment as a single paragraph in less than or equal to 28 words.

                    Format the output as follows:
                    {Main Element 3}
                    {Main Element 3's sub-element 1} ({Main Element 3's sub-element 1 Score}): {Summary of Definition and Comment}
                    {Main Element 3's sub-element 2} ({Main Element 3's sub-element 2 Score}): {Summary of Definition and Comment}
                    {Main Element 3's sub-element 3} ({Main Element 3's sub-element 3 Score}): {Summary of Definition and Comment}
                """
            }   

            print("\nGenerating Summary:...")

            summary=""
            # Summarize each chunk with context
            for chunk_name, text in extracted_chunks.items():
                prompt = prompts.get(chunk_name, "Please summarize the above section.")
                response = generate_summary(full_text, text, prompt)
                summary += response + "\n"

            # Add an additional prompt to analyze the full context for possible derailers
            derailers_prompt = """
                Analyze the full document context to suggest 3 possible derailers of the candidate with a brief description in less than or equal to 28 words.

                Format the output as follows:
                Possible derailers
                1. {Derailer 1 Title}: {Brief Description}
                2. {Derailer 2 Title}: {Brief Description}
                3. {Derailer 3 Title}: {Brief Description}
                """
            
            derailers_summary = generate_summary(full_text, "", derailers_prompt)
            summary += f"{derailers_summary}"

            print("\nSummarized Report:\n")
            print(f"{summary}\n{'-'*40}")

            # Generate radar chart data
            categories = ['Agility', 'Leadership', 'Cultural Fit']
            candidate = [6, 7, 5]  # Example data, replace with actual scores
            average = [6, 6, 6]  # Example data, replace with actual scores
            output_dir = os.path.dirname(file_path)  # Output directory for saving chart image

            # Generate and save radar chart as image
            chart_path = generate_radar_chart(candidate, average, categories, output_dir)

            # Save summarized report as PDF
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_pdf_path = rf'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\ExecRep AI-03 Google_Gemini-1.5-Flash_M3_Graph_{timestamp}.pdf'
            save_text_as_pdf(summary, output_pdf_path, chart_path)
            print(f"\nSummary saved to: {output_pdf_path}")

        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("\nNo file selected.")

if __name__ == "__main__":
    main()