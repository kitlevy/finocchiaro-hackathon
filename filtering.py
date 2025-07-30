import pandas as pd
import numpy as np

#read in 311 data
df = pd.read_csv("full_311_2024.csv")

#filter by desired 311 report reasons
df = df[df["reason"].isin(['Graffiti', 'Alert Boston', 'Generic Noise Disturbance', 'Noise Disturbance', 'Current Events', 'Parking Complaints'])]

print(df.size)

#target university lat+long
bc_lat = 42.3355
bc_long = -71.1685

bu_lat = 42.3505
bu_long = -71.1054

nu_lat = 42.3398
nu_long = -71.0892

hu_lat = 42.3744
hu_long = -71.1182

mit_lat = 42.3601
mit_long = -71.0942

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
df['bu_distance'] = haversine(bu_lat, bu_long, df['latitude'], df['longitude'])
df['nu_distance'] = haversine(nu_lat, nu_long, df['latitude'], df['longitude'])
df['hu_distance'] = haversine(hu_lat, hu_long, df['latitude'], df['longitude'])
df['mit_distance'] = haversine(mit_lat, mit_long, df['latitude'], df['longitude'])

bc_df = df[df['bc_distance'] <=1]
bu_df = df[df['bu_distance'] <=1]
nu_df = df[df['nu_distance'] <=1]
hu_df = df[df['hu_distance'] <=1]
mit_df = df[df['mit_distance'] <=1]

filtered = pd.concat([bc_df, bu_df, nu_df, hu_df, mit_df], ignore_index=True)

filtered = filtered.drop_duplicates()

filtered.to_csv("uni_311.csv")