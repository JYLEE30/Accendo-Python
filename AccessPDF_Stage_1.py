import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re

# Open a file dialog to select a PDF file.
# Returns the file path if a file is selected, otherwise returns None.
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_path

def extract_chunks_from_pages(file_path, page_ranges):
    reader = PyPDF2.PdfReader(file_path)
    chunks = []

    for page_range in page_ranges:
        start_page, end_page = page_range

        # Adjust for zero-based indexing
        start_page_index = start_page - 1
        end_page_index = end_page if end_page is None else end_page - 1

        # Check if the requested pages are within the range of available pages
        if 0 <= start_page_index < len(reader.pages) and 0 <= end_page_index < len(reader.pages):
            chunk = ""
            for i in range(start_page_index, end_page_index + 1):
                page = reader.pages[i]
                text = page.extract_text()
                chunk += text

                # Add a newline if there are more pages in the chunk
                if i < end_page_index:
                    chunk += "\n"
            chunks.append(chunk)
        else:
            print(f"Page range {page_range} out of range.")

    return chunks

def parse_chunk_1(chunk):
    parsed_data = {}

    # Clean up the extracted text
    cleaned_text = re.sub(r'\s*\n\s*', '\n', chunk).strip()

    # Parsing the cleaned text
    lines = cleaned_text.split('\n')

    # This list can be adjusted based on the actual structure of your PDF text
    sections = [
        "Recruitment Extensive",
        "Candidate",
        "Overall Score",
        "Leadership",
        "Agility",
        "Cultural Fit",
    ]

    # Extract individual scores
    leadership_match = re.search(r'Leadership\s+(\d+)/10', cleaned_text)
    agility_match = re.search(r'Agility\s+(\d+)/10', cleaned_text)
    cultural_fit_match = re.search(r'Cultural Fit\s+(\d+)/10', cleaned_text)
    
    # Calculate overall score as the average
    if leadership_match and agility_match and cultural_fit_match:
        leadership_score = int(leadership_match.group(1))
        agility_score = int(agility_match.group(1))
        cultural_fit_score = int(cultural_fit_match.group(1))
        overall_score = (leadership_score + agility_score + cultural_fit_score) // 3
        parsed_data["Overall Score"] = f"{overall_score}/10"
        parsed_data["Leadership"] = f"{leadership_score}/10"
        parsed_data["Agility"] = f"{agility_score}/10"
        parsed_data["Cultural Fit"] = f"{cultural_fit_score}/10"
    else:
        print("Scores not found in the parsed data.")

    for index, line in enumerate(lines):
        if line in sections:
            if line == "Candidate":
                parsed_data["Candidate"] = lines[index + 1]

    # Return a formatted string
    formatted_string = f"Recruitment Extensive REPORT"
    formatted_string += f"\n\nCandidate: {parsed_data.get('Candidate', '')}"
    formatted_string += f"\n\nOverall Score:\t{parsed_data.get('Overall Score', '')}"
    formatted_string += f"\n- Leadership:\t{parsed_data.get('Leadership', '')}"
    formatted_string += f"\n- Agility:\t{parsed_data.get('Agility', '')}"
    formatted_string += f"\n- Cultural Fit:\t{parsed_data.get('Cultural Fit', '')}"

    return formatted_string

def parse_chunk_2(chunk):
    parsed_data = []
    lines = chunk.split("\n")
    
    attributes = [
        "Leadership", "Business Acumen", "Dealing with Ambiguity", 
        "Strategic thinking", "People management and development", 
        "Agility", "Learning Agility", "Cognitive Ability", "Cultural Fit",
        "Purpose Driven", "Performance Oriented", "Principles Led"
    ]
    
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if line in attributes:
            score_line = lines[index + 1].strip()
            score_match = re.search(r'(\d+)/10', score_line)
            if score_match:
                score = score_match.group(1)
                parsed_data.append(f"{line}: {score}/10")
            index += 1  # Move to the next line after extracting the score
        elif line == "Most motivated by:":
            index += 1  # Move to the next line
            motivations = ""
            while index < len(lines) and lines[index] != "Least motivated by:":
                motivations += lines[index].strip() + " "
                index += 1
            parsed_data.append(f"Most motivated by: {motivations.strip()}")
        elif line == "Least motivated by:":
            index += 1  # Move to the next line
            motivations = ""
            while index < len(lines):
                motivations += lines[index].strip() + " "
                index += 1
            parsed_data.append(f"Least motivated by: {motivations.strip()}")
        index += 1  # Move to the next line
    
    return parsed_data

# Example usage:
chunk_2_text = """
Quickview
Leadership
Business Acumen
8/10
Dealing with Ambiguity
5/10
Strategic thinking
8/10
People management and development
6/10
Agility
Learning Agility
7/10
Cognitive Ability
5/10Cultural Fit
Purpose Driven
3/10
Performance Oriented
5/10
Principles Led
7/10
Most motivated by:
Structuring Hierarchy Integrity
Least motivated by:
Security Absence Of Stress Cooperativeness
"""

parsed_chunk_2 = parse_chunk_2(chunk_2_text)
print(parsed_chunk_2)

def parse_chunk_3(chunk):
    formatted_string = ''
    return formatted_string

def parse_chunk_4(chunk):
    formatted_string = ''
    return formatted_string

def parse_chunk_5(chunk):
    formatted_string = ''
    return formatted_string

def parse_chunk_6(chunk):
    formatted_string = ''
    return formatted_string

def parse_chunk_7(chunk):
    formatted_string = ''
    return formatted_string

def parse_chunk_8(chunk):
    formatted_string = ''
    return formatted_string

def parse_chunk_9(chunk):
    formatted_string = ''
    return formatted_string

def main():
    file_path = select_pdf_file()
    if not file_path:
        print("No file selected.")
        return

    page_ranges = [
        (1, 1),         # page 1
        (3, 3),         # page 3
        (4, 7),         # pages 4-7
        (8, 9),         # pages 8-9
        (10, 10),       # page 10
        (11, 11),       # page 11
        (12, 12),       # page 12
        (13, 13),       # page 13
        (14, 17),       # pages 14-17
    ]

    chunks = extract_chunks_from_pages(file_path, page_ranges)

    # Print the original chunk list
    if chunks:
        print("Original Chunk List:\n")
        for chunk in chunks:
            print(chunk, "\n")

    # Parsing and restructuring chunks
    restructured_chunks = []
    if chunks:
        for i, chunk in enumerate(chunks, start=1):
            if i == 1:
                restructured_chunks.append(parse_chunk_1(chunk))
            elif i == 2:
                restructured_chunks.append(parse_chunk_2(chunk))
            elif i == 3:
                restructured_chunks.append(parse_chunk_3(chunk))
            elif i == 4:
                restructured_chunks.append(parse_chunk_4(chunk))
            elif i == 5:
                restructured_chunks.append(parse_chunk_5(chunk))
            elif i == 6:
                restructured_chunks.append(parse_chunk_6(chunk))
            elif i == 7:
                restructured_chunks.append(parse_chunk_7(chunk))
            elif i == 8:
                restructured_chunks.append(parse_chunk_8(chunk))
            else:
                restructured_chunks.append(parse_chunk_9(chunk))

    # Print the restructured chunks
    if restructured_chunks:
        print("\nRestructured Chunks:\n")
        for restructured_chunk in restructured_chunks:
            print(restructured_chunk, "\n")

if __name__ == "__main__":
    main()