import pandas as pd
import numpy as np

#read in 311 data
df = pd.read_csv("full_311_2024.csv")

#filter by desired 311 report reasons
df = df[df["reason"].isin(['Sanitation', 'Code Enforcement', 'Graffiti', 'Alert Boston', 'Generic Noise Disturbance', 'Noise Disturbance', 'Current Events', 'Parking Complaints'])]

print(df.size)

#target university lat+long
bc_lat = 42.3355
bc_long = -71.1685

#haversine function which calculates distances over sphere
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2)**2
    return 2 * R * np.arcsin(np.sqrt(a))


df['bc_distance'] = haversine(bc_lat, bc_long, df['latitude'], df['longitude'])


bc_df = df[df['bc_distance'] <=1]

just_outside = df[df['bc_distance'] <=np.sqrt(2)]

print(len(just_outside))

just_outside = just_outside.drop(just_outside[just_outside['bc_distance'] <=1].index)

bc_df.to_csv('bc_df_1mile.csv')
just_outside.to_csv('comparison.csv')

print(len(bc_df))
print(len(just_outside))