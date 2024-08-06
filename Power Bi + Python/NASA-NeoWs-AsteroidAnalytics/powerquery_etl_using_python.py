import pandas as pd

dataset['Hazard_Classification'] = dataset['Is_Potentially_Hazardous'].map({True: 'Dangerous', False: 'Not Dangerous'})
dataset = dataset[dataset['Is_Potentially_Hazardous'] == True]#remove this if you want all asteroids
dataset['Diameter_Max_KM'] = dataset['Diameter_Max_KM'].astype(float)

# Add ranking based on Diameter_Max_KM

# Convert Miss_Distance_KM to float if it's not already

# Convert Miss_Distance_KM to float if it's not already
dataset['Miss_Distance_KM'] = dataset['Miss_Distance_KM'].astype(float)

# Normalize Diameter_Max_KM and Miss_Distance_KM
dataset['Diameter_Normalized'] = (dataset['Diameter_Max_KM'] - dataset['Diameter_Max_KM'].min()) / (dataset['Diameter_Max_KM'].max() - dataset['Diameter_Max_KM'].min())
dataset['Miss_Distance_Normalized'] = 1 - (dataset['Miss_Distance_KM'] - dataset['Miss_Distance_KM'].min()) / (dataset['Miss_Distance_KM'].max() - dataset['Miss_Distance_KM'].min())

# Calculate combined threat score (higher score = more threatening)
dataset['Threat_Score'] = dataset['Diameter_Normalized'] + dataset['Miss_Distance_Normalized']

# Rank based on the combined threat score
dataset['Threat_Rank'] = dataset['Threat_Score'].rank(method='dense', ascending=False)
dataset['Threat_Rank'] = dataset['Threat_Rank'].astype(int)

# Sort by the new Threat_Rank
dataset.sort_values(by='Threat_Rank', ascending=True, inplace=True)

# Reset index
dataset.reset_index(drop=True, inplace=True)
