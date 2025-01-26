from flask import session
import random
import pandas as pd
from database import get_user_past_flights, get_user_data
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler # this for scaling the data to normalize
import json
import seaborn as sns
import matplotlib as plt
import numpy as np


def generate_past_flights(trend, num_flights=5):
    flights = []
    for _ in range(num_flights):
        if trend == "early_flight_time":
            flight_time = round(random.uniform(1.0, 3.0), 2)  # Short flight times (1-3 hours)
            price = round(random.uniform(200.0, 400.0), 2)    # Moderate price
            distance = round(random.uniform(300.0, 600.0), 2) # Moderate distance
        elif trend == "low_price":
            flight_time = round(random.uniform(2.0, 6.0), 2)  # Moderate flight times
            price = round(random.uniform(100.0, 300.0), 2)    # Low price
            distance = round(random.uniform(200.0, 500.0), 2) # Short to moderate distance
        elif trend == "long_distance":
            flight_time = round(random.uniform(4.0, 10.0), 2)  # Long flight times
            price = round(random.uniform(500.0, 1000.0), 2)   # High price
            distance = round(random.uniform(1000.0, 2000.0), 2) # Long distance
        else:
            flight_time = round(random.uniform(1.0, 24.0), 2)  # Random flight times
            price = round(random.uniform(100.0, 1000.0), 2)   # Random price
            distance = round(random.uniform(200.0, 2000.0), 2) # Random distance

        flights.append({
            "flight_time": flight_time,
            "price": price,
            "distance": distance
        })
    return flights

def cluster(username):
    # fetch user data using username as parameter
    user_info = get_user_data(username)
    past_flight_dict = user_info["past_flights"]
    # past flight is a list of dictionaries
    # each element is a dictionary in the past_flight_dict
    # each dictionary has keys: flight_time, price, distance
    
    
    # convert to dataframe
    df = pd.DataFrame(past_flight_dict)
    print(df)
    
    # normalize the data
    scaler = StandardScaler()
    # fit to data
    scaled_data = scaler.fit_transform(df)
    # Transform the data
    normalized_data = scaler.transform(df)

    # Convert the normalized data back to a DataFrame
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)
    print("Normalized Data:")
    print(normalized_df)
    
    
    # df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    # print(df_normalized)

    # Define the number of clusters
    k = 2

    # Train the K-Means model
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    
    df["Cluster"] = kmeans.labels_

    cluster_summary = df.groupby("Cluster").mean()
    print(cluster_summary)  
    
    # plt.figure(figsize=(8, 6))
    # sns.scatterplot(data=df, x="price", y="distance", hue="Cluster", palette="viridis")
    # plt.title("Clusters: Price vs. Distance")
    # plt.show()