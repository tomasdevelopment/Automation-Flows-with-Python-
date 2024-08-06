import pandas as pd

# Convert hazard classification
dataset['Hazard_Classification'] = dataset['Is_Potentially_Hazardous'].map({True: 'Dangerous', False: 'Not Dangerous'})

# Convert columns to float
dataset['Diameter_Max_KM'] = dataset['Diameter_Max_KM'].astype(float)
dataset['Miss_Distance_KM'] = dataset['Miss_Distance_KM'].astype(float)

# Normalize Diameter_Max_KM and Miss_Distance_KM
dataset['Diameter_Normalized'] = (dataset['Diameter_Max_KM'] - dataset['Diameter_Max_KM'].min()) / (dataset['Diameter_Max_KM'].max() - dataset['Diameter_Max_KM'].min())
dataset['Miss_Distance_Normalized'] = 1 - (dataset['Miss_Distance_KM'] - dataset['Miss_Distance_KM'].min()) / (dataset['Miss_Distance_KM'].max() - dataset['Miss_Distance_KM'].min())

# Calculate combined threat score (higher score = more threatening)
dataset['Threat_Score'] = dataset['Diameter_Normalized'] + dataset['Miss_Distance_Normalized']

# Separate dangerous and non-dangerous asteroids
dangerous = dataset[dataset['Is_Potentially_Hazardous'] == True].copy()
non_dangerous = dataset[dataset['Is_Potentially_Hazardous'] == False].copy()

# Rank only the dangerous asteroids
dangerous['Threat_Rank'] = dangerous['Threat_Score'].rank(method='dense', ascending=False)
dangerous['Threat_Rank'] = dangerous['Threat_Rank'].astype(int)

# Merge rankings back into the original dataset
dataset = pd.merge(dataset, dangerous[['Threat_Rank']], how='left', left_index=True, right_index=True)

# Fill NaN values in Threat_Rank for non-dangerous asteroids with a default value (e.g., a high number)
dataset['Threat_Rank'] = dataset['Threat_Rank'].fillna(dataset['Threat_Rank'].max() + 1).astype(int)

# Sort by the new Threat_Rank
dataset.sort_values(by='Threat_Rank', ascending=True, inplace=True)

# Reset index
dataset.reset_index(drop=True, inplace=True)

# Show dataset with ranks
print(dataset.head())
