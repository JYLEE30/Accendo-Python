import PyPDF2
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text_per_page = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            text_per_page.append(text)
    return text_per_page

# Path to the PDF file
pdf_path = r'C:\Users\leeji\OneDrive\Desktop\Accendo Projects\Executive Report\(1) JYLEE_TPRecruitmentExtensive.pdf'

# Extract text from each page of the PDF
text_per_page = extract_text_from_pdf(pdf_path)

# Summarize each page separately
summaries = []
for page_num, text in enumerate(text_per_page):
    # Adjust max_length based on the input_length
    input_length = len(text)
    max_length = min(input_length // 2, 512)  # Set max_length to half of the input_length or 512, whichever is smaller
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    summaries.append(summary[0]['summary_text'])

# Save the summaries to a text file
output_file = "summaries.txt"
with open(output_file, "w") as f:
    for page_num, summary in enumerate(summaries):
        f.write(f"Summary of Page {page_num + 1}:\n")
        f.write(summary + "\n\n")

print(f"Summaries saved to {output_file}")


# HuggingFace Falconsai Summarization Sample Code
'''
from transformers import pipeline

# Initialize the summarization pipeline using the specified model
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# Define the input text to be summarized
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

# Use the summarizer pipeline to generate a summary of the input text
# Parameters:
# - max_length: Maximum length of the summary in tokens
# - min_length: Minimum length of the summary in tokens
# - do_sample: Whether to use sampling when generating the summary
print(summarizer(ARTICLE, max_length=1000, min_length=30, do_sample=False))
[{'summary_text': 'Hugging Face has emerged as a prominent and innovative force in NLP . From its inception to its role in democratizing AI, the company has left an indelible mark on the industry . The name "Hugging Face" was chosen to reflect the company\'s mission of making AI models more accessible and friendly to humans .'}]
'''