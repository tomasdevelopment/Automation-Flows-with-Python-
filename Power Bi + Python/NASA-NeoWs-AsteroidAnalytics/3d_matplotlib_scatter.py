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

# Define minimum and maximum marker sizes
min_marker_size = 500  # Increased minimum marker size by 5x
max_marker_size = 2000  # Adjusted maximum size for scaling

# Normalize diameter to size range for markers with new minimum size
def normalize_size(diameter, min_size=min_marker_size, max_size=max_marker_size):
    min_diameter = dataset['Diameter_Max_KM'].min()
    max_diameter = dataset['Diameter_Max_KM'].max()
    normalized_size = min_size + (diameter - min_diameter) / (max_diameter - min_diameter) * (max_size - min_size)
    return max(normalized_size, min_size)  # Ensure size is at least min_size

# Apply the size normalization function
non_dangerous['Marker_Size'] = non_dangerous['Diameter_Max_KM'].apply(lambda d: normalize_size(d, min_size=min_marker_size, max_size=1000))
dangerous['Marker_Size'] = dangerous['Diameter_Max_KM'].apply(lambda d: normalize_size(d, min_size=min_marker_size, max_size=max_marker_size))

# Create a figure and 3D axis
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Set background color
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Plot non-dangerous asteroids with a very light green color
ax.scatter(non_dangerous['Diameter_Max_KM'],
           non_dangerous['Miss_Distance_KM'],
           non_dangerous['Threat_Rank'],
           c='lightgreen', label='Not Dangerous',
           s=non_dangerous['Marker_Size'], alpha=0.2)  # Light color and low alpha

# Plot dangerous asteroids
scatter = ax.scatter(dangerous['Diameter_Max_KM'],
                     dangerous['Miss_Distance_KM'],
                     dangerous['Threat_Rank'],
                     c=dangerous['Threat_Rank'],
                     cmap='YlOrRd_r',  # Reversed colormap
                     label='Dangerous',
                     s=dangerous['Marker_Size'])

# Add name tags and ranks for dangerous asteroids with bold text
for idx, row in dangerous.iterrows():
    ax.text(row['Diameter_Max_KM'], 
            row['Miss_Distance_KM'], 
            row['Threat_Rank'], 
            f"{row['Name.1']} (Rank: {row['Threat_Rank']})", 
            fontsize=12.5,
            color='white',  # Light color for text
            verticalalignment='bottom',  # Align text vertically
            horizontalalignment='center',  # Center text horizontally
            fontweight='bold')  # Make text bold

# Set labels with bold fonts
ax.set_xlabel('Diameter (km)', color='white', fontsize=14, fontweight='bold')
ax.set_ylabel('Miss Distance (km)', color='white', fontsize=14, fontweight='bold')
ax.set_zlabel('Threat Rank', color='white', fontsize=14, fontweight='bold')

# Custom legend with bold text
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=15, label='High Threat Rank (Rank 1)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=15, label='Medium Threat Rank (Rank 5-6)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=15, label='Low Threat Rank (Rank 7-8)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=15, label='No Threat (Rank 9)')
]
ax.legend(handles=legend_elements, title='Threat Rank Categories', facecolor='black', edgecolor='white', fontsize='medium', title_fontsize='13')
for text in ax.get_legend().get_texts():
    text.set_color('white')
ax.get_legend().get_title().set_color('white')

plt.show()

# ##LIGHT VERSION
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from matplotlib.lines import Line2D

# plt.style.use('_mpl-gallery')

# # Ensure the necessary columns are numeric
# dataset['Diameter_Max_KM'] = dataset['Diameter_Max_KM'].astype(float)
# dataset['Miss_Distance_KM'] = dataset['Miss_Distance_KM'].astype(float)
# dataset['Threat_Rank'] = dataset['Threat_Rank'].astype(int)

# # Separate dangerous and non-dangerous asteroids
# dangerous = dataset[dataset['Hazard_Classification'] == 'Dangerous']
# non_dangerous = dataset[dataset['Hazard_Classification'] == 'Not Dangerous']

# # Define minimum and maximum marker sizes
# min_marker_size = 500  # Increased minimum marker size by 5x
# max_marker_size = 2000  # Adjusted maximum size for scaling

# # Normalize diameter to size range for markers with new minimum size
# def normalize_size(diameter, min_size=min_marker_size, max_size=max_marker_size):
#     min_diameter = dataset['Diameter_Max_KM'].min()
#     max_diameter = dataset['Diameter_Max_KM'].max()
#     normalized_size = min_size + (diameter - min_diameter) / (max_diameter - min_diameter) * (max_size - min_size)
#     return max(normalized_size, min_size)  # Ensure size is at least min_size

# # Apply the size normalization function
# non_dangerous['Marker_Size'] = non_dangerous['Diameter_Max_KM'].apply(lambda d: normalize_size(d, min_size=min_marker_size, max_size=1000))
# dangerous['Marker_Size'] = dangerous['Diameter_Max_KM'].apply(lambda d: normalize_size(d, min_size=min_marker_size, max_size=max_marker_size))

# # Create a figure and 3D axis
# fig = plt.figure(figsize=(12, 10))
# ax = fig.add_subplot(111, projection='3d')

# # Plot non-dangerous asteroids with a very light green color
# ax.scatter(non_dangerous['Diameter_Max_KM'],
#            non_dangerous['Miss_Distance_KM'],
#            non_dangerous['Threat_Rank'],
#            c='lightgreen', label='Not Dangerous',
#            s=non_dangerous['Marker_Size'], alpha=0.2)  # Light color and low alpha

# # Plot dangerous asteroids
# scatter = ax.scatter(dangerous['Diameter_Max_KM'],
#                      dangerous['Miss_Distance_KM'],
#                      dangerous['Threat_Rank'],
#                      c=dangerous['Threat_Rank'],
#                      cmap='YlOrRd_r',  # Reversed colormap
#                      label='Dangerous',
#                      s=dangerous['Marker_Size'])

# # Add name tags and ranks for dangerous asteroids
# for idx, row in dangerous.iterrows():
#     ax.text(row['Diameter_Max_KM'], 
#             row['Miss_Distance_KM'], 
#             row['Threat_Rank'], 
#             f"{row['Name.1']} (Rank: {row['Threat_Rank']})", 
#             fontsize=12.5,
#             verticalalignment='bottom',  # Align text vertically
#             horizontalalignment='center')  # Center text horizontally

# # Set labels
# ax.set_xlabel('Diameter (km)')
# ax.set_ylabel('Miss Distance (km)')
# ax.set_zlabel('Threat Rank')

# # Custom legend with color patches reflecting reversed threat ranks
# legend_elements = [
#     Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=15, label='High Threat Rank (Rank 1)'),
#     Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=15, label='Medium Threat Rank (Rank 5-6)'),
#     Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=15, label='Low Threat Rank (Rank 7-8)'),
#     Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=15, label='No Threat (Rank 9)')
# ]
# ax.legend(handles=legend_elements, title='Threat Rank Categories')

# plt.show()

