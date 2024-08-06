import pandas as pd


dataset['Hazard_Classification'] = dataset['Is_Potentially_Hazardous'].map({True: 'Dangerous', False: 'Not Dangerous'}) #add an additional column to map if its hazardous
