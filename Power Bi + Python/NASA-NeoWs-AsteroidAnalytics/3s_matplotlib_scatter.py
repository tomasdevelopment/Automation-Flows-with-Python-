import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

plt.style.use('_mpl-gallery')

# Ensure the necessary columns are numeric
dataset['Diameter_Max_KM'] = dataset['Diameter_Max_KM'].astype(float)
dataset['Miss_Distance_KM'] = dataset['Miss_Distance_KM'].astype(float)
dataset['Threat_Rank'] = dataset['Threat_Rank'].astype(int)

# Separate dangerous and non-dangerous asteroids
dangerous = dataset[dataset['Hazard_Classification'] == 'Dangerous']
non_dangerous = dataset[dataset['Hazard_Classification'] == 'Not Dangerous']

# Create a figure and 3D axis
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot non-dangerous asteroids (larger size)
ax.scatter(non_dangerous['Diameter_Max_KM'],
           non_dangerous['Miss_Distance_KM'],
           non_dangerous['Threat_Rank'],
           c='green', label='Not Dangerous', s=20, alpha=0.3)  # Increased marker size

# Plot dangerous asteroids (larger size)
scatter = ax.scatter(dangerous['Diameter_Max_KM'],
                     dangerous['Miss_Distance_KM'],
                     dangerous['Threat_Rank'],
                     c=dangerous['Threat_Rank'],
                     cmap='YlOrRd_r',  # Reversed colormap
                     label='Dangerous',
                     s=200)  # Increased marker size

# Add name tags and ranks for dangerous asteroids
for idx, row in dangerous.iterrows():
    ax.text(row['Diameter_Max_KM'], 
            row['Miss_Distance_KM'], 
            row['Threat_Rank'], 
            f"{row['Name.1']} (Rank: {row['Threat_Rank']})", 
            fontsize=10)

# Set labels
ax.set_xlabel('Diameter (km)')
ax.set_ylabel('Miss Distance (km)')
ax.set_zlabel('Threat Rank')

# Custom legend with color patches reflecting reversed threat ranks
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=12, label='High Threat Rank (Rank 1)'),  # Increased marker size
    Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=11, label='Medium Threat Rank (Rank 5-6)'),  # Increased marker size
    Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10, label='Low Threat Rank (Rank 7-8)'),  # Increased marker size
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='No Threat (Rank 9)')  # Increased marker size
]
ax.legend(handles=legend_elements, title='Threat Rank Categories')

plt.show()
