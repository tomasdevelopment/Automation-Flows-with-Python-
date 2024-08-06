import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.style.use('_mpl-gallery')

# Ensure the necessary columns are numeric
dataset['Diameter_Max_KM'] = dataset['Diameter_Max_KM'].astype(float)
dataset['Miss_Distance_KM'] = dataset['Miss_Distance_KM'].astype(float)
dataset['Threat_Rank'] = dataset['Threat_Rank'].astype(int)

# Separate dangerous and non-dangerous asteroids
dangerous = dataset[dataset['Hazard_Classification'] == 'Dangerous']
non_dangerous = dataset[dataset['Hazard_Classification'] == 'Not Dangerous']

# Plot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(12, 8))

# Plot non-dangerous asteroids (small size)
ax.scatter(non_dangerous['Diameter_Max_KM'],
           non_dangerous['Miss_Distance_KM'],
           non_dangerous['Threat_Rank'],
           c='green', label='Not Dangerous', s=10, alpha=0.3)

# Plot dangerous asteroids (larger size)
scatter = ax.scatter(dangerous['Diameter_Max_KM'],
                     dangerous['Miss_Distance_KM'],
                     dangerous['Threat_Rank'],
                     c=dangerous['Threat_Rank'],
                     cmap='YlOrRd',
                     label='Dangerous',
                     s=100)

ax.set(xticklabels=[],
       yticklabels=[],
       zticklabels=[])

# Set labels
ax.set_xlabel('Diameter (km)')
ax.set_ylabel('Miss Distance (km)')
ax.set_zlabel('Threat Rank')

# Add a color bar for dangerous asteroids
fig.colorbar(scatter, ax=ax, label='Threat Rank (Dangerous)')

# Add name tags and ranks for dangerous asteroids
for idx, row in dangerous.iterrows():
    ax.text(row['Diameter_Max_KM'], 
            row['Miss_Distance_KM'], 
            row['Threat_Rank'], 
            f"{row['Name.1']} (Rank: {row['Threat_Rank']})", 
            fontsize=10)

plt.legend()
plt.show()
