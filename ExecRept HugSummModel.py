from fpdf import FPDF
from transformers import pipeline
import PyPDF2

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to split text into chunks
def split_text_into_chunks(text, max_chunk_length=3000):
    chunks = []
    current_chunk = ""
    for paragraph in text.split("\n"):
        if len(current_chunk) + len(paragraph) < max_chunk_length:
            current_chunk += paragraph + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Function to save text as a PDF
def save_text_as_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Encode the text as UTF-8 before passing it to FPDF
    pdf.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output(output_path)

# Path to the PDF file
pdf_path = r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\(1) JYLEE_TPRecruitmentExtensive.pdf'  # Change this to the path of your PDF file

# Extract text from the PDF
article_text = extract_text_from_pdf(pdf_path)

# Split text into chunks
text_chunks = split_text_into_chunks(article_text)

# Summarize each chunk separately
summaries = []
for chunk in text_chunks:
    summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    summaries.append(summary)

# Combine the summaries
combined_summary = ' '.join(summaries)

# Save the combined summary as a PDF
output_pdf_path = "combined_summary.pdf"  # Change this to the desired output path
save_text_as_pdf(combined_summary, output_pdf_path)

print("PDF saved successfully!")

'''from fpdf import FPDF
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

# Define the article text
ARTICLE = """ 
Hugging Face: Revolutionizing Natural Language Processing
Introduction
In the rapidly evolving field of Natural Language Processing (NLP), Hugging Face has emerged as a prominent and innovative force. This article will explore the story and significance of Hugging Face, a company that has made remarkable contributions to NLP and AI as a whole. From its inception to its role in democratizing AI, Hugging Face has left an indelible mark on the industry.
The Birth of Hugging Face
Hugging Face was founded in 2016 by Clément Delangue, Julien Chaumond, and Thomas Wolf. The name "Hugging Face" was chosen to reflect the company's mission of making AI models more accessible and friendly to humans, much like a comforting hug. Initially, they began as a chatbot company but later shifted their focus to NLP, driven by their belief in the transformative potential of this technology.
Transformative Innovations
Hugging Face is best known for its open-source contributions, particularly the "Transformers" library. This library has become the de facto standard for NLP and enables researchers, developers, and organizations to easily access and utilize state-of-the-art pre-trained language models, such as BERT, GPT-3, and more. These models have countless applications, from chatbots and virtual assistants to language translation and sentiment analysis.
Key Contributions:
1. **Transformers Library:** The Transformers library provides a unified interface for more than 50 pre-trained models, simplifying the development of NLP applications. It allows users to fine-tune these models for specific tasks, making it accessible to a wider audience.
2. **Model Hub:** Hugging Face's Model Hub is a treasure trove of pre-trained models, making it simple for anyone to access, experiment with, and fine-tune models. Researchers and developers around the world can collaborate and share their models through this platform.
3. **Hugging Face Transformers Community:** Hugging Face has fostered a vibrant online community where developers, researchers, and AI enthusiasts can share their knowledge, code, and insights. This collaborative spirit has accelerated the growth of NLP.
Democratizing AI
Hugging Face's most significant impact has been the democratization of AI and NLP. Their commitment to open-source development has made powerful AI models accessible to individuals, startups, and established organizations. This approach contrasts with the traditional proprietary AI model market, which often limits access to those with substantial resources.
By providing open-source models and tools, Hugging Face has empowered a diverse array of users to innovate and create their own NLP applications. This shift has fostered inclusivity, allowing a broader range of voices to contribute to AI research and development.
Industry Adoption
The success and impact of Hugging Face are evident in its widespread adoption. Numerous companies and institutions, from startups to tech giants, leverage Hugging Face's technology for their AI applications. This includes industries as varied as healthcare, finance, and entertainment, showcasing the versatility of NLP and Hugging Face's contributions.
Future Directions
Hugging Face's journey is far from over. As of my last knowledge update in September 2021, the company was actively pursuing research into ethical AI, bias reduction in models, and more. Given their track record of innovation and commitment to the AI community, it is likely that they will continue to lead in ethical AI development and promote responsible use of NLP technologies.
Conclusion
Hugging Face's story is one of transformation, collaboration, and empowerment. Their open-source contributions have reshaped the NLP landscape and democratized access to AI. As they continue to push the boundaries of AI research, we can expect Hugging Face to remain at the forefront of innovation, contributing to a more inclusive and ethical AI future. Their journey reminds us that the power of open-source collaboration can lead to groundbreaking advancements in technology and bring AI within the reach of many.
"""
# Split the article into smaller chunks
chunk_size = 400  # Adjust this value as needed
chunks = [ARTICLE[i:i+chunk_size] for i in range(0, len(ARTICLE), chunk_size)]

# Summarize each chunk separately
summaries = []
for chunk in chunks:
    summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
    summaries.append(summary[0]['summary_text'])

# Print the combined summary
print(' '.join(summaries))

# Create a new PDF object
pdf = FPDF()

# Add a new page to the PDF
pdf.add_page()

# Set the font style and size
pdf.set_font("Arial", size=12)

# Write the generated summary to the PDF with auto spacing down to the next row
for line in summary.split('\n'):
    pdf.cell(200, 10, txt=line, ln=True)

# Save the PDF to a file
pdf.output("Executive Report.pdf")

# Print a message to confirm that the PDF was saved
print("Successfully Saved")'''