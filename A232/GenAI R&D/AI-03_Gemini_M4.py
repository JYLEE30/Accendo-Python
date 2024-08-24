import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Data
categories = ['Agility', 'Leadership', 'Cultural Fit']
N = len(categories)

candidate = [6, 7, 5]
average = [6, 6, 6]

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
plt.xticks(angles[:-1], categories, color='grey', size=8)

# Draw y-labels
plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], color="grey", size=7)
plt.ylim(0, 10)

# Plot data
ax.plot(angles, candidate, linewidth=2, linestyle='solid', label='Candidate', color='blue')
ax.fill(angles, candidate, 'b', alpha=0.1)

ax.plot(angles, average, linewidth=2, linestyle='solid', label='Average', color='red')
ax.fill(angles, average, 'r', alpha=0.1)

# Add a legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

# Add labels for each point slightly away from the actual points
label_offset = 0.5
for i in range(N):
    angle_rad = angles[i]
    
    candidate_x = (candidate[i] + label_offset) * np.cos(angle_rad)
    candidate_y = (candidate[i] + label_offset) * np.sin(angle_rad)
    plt.text(angle_rad, candidate[i] + label_offset, str(candidate[i]), horizontalalignment='center', size=10, color='blue', weight='semibold')
    
    average_x = (average[i] + label_offset) * np.cos(angle_rad)
    average_y = (average[i] + label_offset) * np.sin(angle_rad)
    plt.text(angle_rad, average[i] + 2 * label_offset, str(average[i]), horizontalalignment='center', size=10, color='red', weight='semibold')

# Show the plot
plt.title('Candidate vs Average Performance')
plt.show()