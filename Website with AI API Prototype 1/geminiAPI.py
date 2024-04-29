'''import tkinter as tk
import requests
from bs4 import BeautifulSoup

# Define the URL for the Gemini API
gemini_url = "https://api.gemini.com/v1/content"

# Define the prompt for the report summary
prompt = "Summarize the following text in one paragraph: "

# Define a function to summarize the page
def summarize_page():
    # Get the text from the current page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()

    # Generate the summary using the Gemini API
    headers = {"Content-Type": "application/json"}
    data = {"text": text, "prompt": prompt}
    response = requests.post(gemini_url, headers=headers, json=data)

    # Print the summary
    print(response.json()["summary"])

# Define the URL for the page you want to summarize
url = "https://www.example.com"

# Create the main window
root = tk.Tk()

# Create the "Summarize Page" button
button = tk.Button(root, text="Summarize Page", command=summarize_page)
button.pack()

# Start the Tkinter event loop
root.mainloop()'''

import matplotlib.pyplot as plt
import numpy as np

# Define the sub-skills and their scores for each category
leadership_skills = {'Communication': 0.7, 'Teamwork': 0.8, 'Decision Making': 0.9}
agility_skills = {'Adaptability': 0.6, 'Learning Ability': 0.7, 'Responsiveness': 0.8}
cultural_fit_skills = {'Diversity and Inclusion': 0.6, 'Collaboration': 0.7, 'Work Ethic': 0.8}

# Define the colors for each category
category_colors = {'Leadership': 'red', 'Agility': 'yellow', 'Cultural Fit': 'blue'}

# Calculate the number of spokes in the radar chart
num_spokes = sum(len(skills) for skills in (leadership_skills, agility_skills, cultural_fit_skills))

# Calculate the angles for each spoke
angles = np.linspace(0, 2 * np.pi, num_spokes, endpoint=False)

# Create the radar chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Plot the pie chart for each category
for i, (category, skills) in enumerate(zip(['Leadership', 'Agility', 'Cultural Fit'], [leadership_skills, agility_skills, cultural_fit_skills])):
    ax.plot(angles + i * 2 * np.pi / 3, np.zeros_like(angles) + max(skills.values()), color=category_colors[category], linewidth=2)
    ax.fill(angles + i * 2 * np.pi / 3, np.zeros_like(angles) + max(skills.values()), color=category_colors[category], alpha=0.2)
    ax.text(angles[0] + i * 2 * np.pi / 3, max(skills.values()) + 0.1, category, ha='center', va='bottom', fontsize=14)

    for j, (name, score) in enumerate(skills.items()):
        angle = angles[j] + i * 2 * np.pi / 3
        ax.text(angle, score + 0.05, name, ha='center', va='bottom', fontsize=10)

# Create a list of labels for the theta grids
labels = []
for i, (category, skills) in enumerate(zip(['Leadership', 'Agility', 'Cultural Fit'], [leadership_skills, agility_skills, cultural_fit_skills])):
    for skill in skills:
        labels.append(f'{category}: {skill}')

# Set the chart properties
ax.set_rmax(10)
ax.set_thetagrids(angles * 180 / np.pi, labels)
ax.grid(True)
ax.set_facecolor('white')

plt.show()