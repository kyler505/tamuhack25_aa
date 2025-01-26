from flask import session
import random
import pandas as pd
from database import get_user_data
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler # this for scaling the data to normalize
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# def generate_past_flights(trend, num_flights=25):
#     flights = []
#     for _ in range(num_flights):
#         if trend == "early_flight_time":
#             flight_time = round(random.uniform(1.0, 3.0), 2)  # Short flight times (1-3 hours)
#             price = round(random.uniform(200.0, 400.0), 2)    # Moderate price
#             distance = round(random.uniform(300.0, 600.0), 2) # Moderate distance
#         elif trend == "low_price":
#             flight_time = round(random.uniform(2.0, 6.0), 2)  # Moderate flight times
#             price = round(random.uniform(100.0, 300.0), 2)    # Low price
#             distance = round(random.uniform(200.0, 500.0), 2) # Short to moderate distance
#         elif trend == "long_distance":
#             flight_time = round(random.uniform(4.0, 10.0), 2)  # Long flight times
#             price = round(random.uniform(500.0, 1000.0), 2)   # High price
#             distance = round(random.uniform(1000.0, 2000.0), 2) # Long distance
#         else:
#             flight_time = round(random.uniform(1.0, 24.0), 2)  # Random flight times
#             price = round(random.uniform(100.0, 1000.0), 2)   # Random price
#             distance = round(random.uniform(200.0, 2000.0), 2) # Random distance

#         flights.append({
#             "flight_time": flight_time,
#             "price": price,
#             "distance": distance
#         })
#     return flights


def generate_past_flights(trend, num_flights=25):
    flights = []
    
    for _ in range(num_flights):
        if trend == "early_flight_time":
            # Cluster around early departure times (e.g., 6 AM to 9 AM)
            departure_time = round(random.gauss(7.0, 1.0), 2)  # Mean = 7:00 AM, Std Dev = 1.0
            price = round(random.gauss(300.0, 50.0), 2)        # Moderate price
            distance = round(random.gauss(450.0, 100.0), 2)    # Moderate distance
        elif trend == "low_price":
            # Cluster around midday departure times (e.g., 12 PM to 3 PM)
            departure_time = round(random.gauss(13.0, 1.0), 2) # Mean = 1:00 PM, Std Dev = 1.0
            price = round(random.gauss(200.0, 30.0), 2)        # Low price
            distance = round(random.gauss(350.0, 75.0), 2)     # Short to moderate distance
        elif trend == "long_distance":
            # Cluster around late-night departure times (e.g., 10 PM to 1 AM)
            departure_time = round(random.gauss(23.0, 1.0), 2) # Mean = 11:00 PM, Std Dev = 1.0
            price = round(random.gauss(750.0, 100.0), 2)       # High price
            distance = round(random.gauss(1500.0, 200.0), 2)   # Long distance
        else:
            # Random data without clustering
            departure_time = round(random.uniform(0.0, 24.0), 2)
            price = round(random.uniform(100.0, 1000.0), 2)
            distance = round(random.uniform(200.0, 2000.0), 2)
        
        # Ensure departure_time is within 0-24 hours
        departure_time = max(0.0, min(24.0, departure_time))
        
        
        flights.append({
            "flight_time": departure_time,
            "price": price,
            "distance": distance
        })
        
    
    return flights

def cluster(username):
    # Fetch user data using username as parameter
    user_info = get_user_data(username)
    past_flight_dict = user_info["past_flights"]
    
    # Convert to DataFrame
    df = pd.DataFrame(past_flight_dict)
    print("Original Data:")
    print(df)
    
    # Normalize the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)
    normalized_data = scaler.transform(df)

    # Convert the normalized data back to a DataFrame
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)
    print("Normalized Data:")
    print(normalized_df)
    
    # Define the number of clusters
    k = 2

    # Train the K-Means model
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    
    # Add the cluster labels to the original DataFrame
    df["Cluster"] = pd.Categorical(kmeans.labels_)

    # Calculate the mean values for each cluster (centroids)
    cluster_summary = df.groupby("Cluster", observed=True).mean()
    print("Cluster Summary (Centroids):")
    print(cluster_summary)
    
    # Convert the cluster centroids to an array of arrays
    centroids = cluster_summary.values.tolist()
    
    # Return the centroids
    return centroids

    # Plot the clusters
    # plt.subplot(1, 3, 1)
    # sns.scatterplot(data=df, x="flight_time", y="price", hue="Cluster", palette="viridis")
    # plt.title("Flight Time vs. Price")
    # plt.xlabel("Flight Time (hours)")
    # plt.ylabel("Price ($)")
    
    # # Plot 2: flight_time vs. distance
    # plt.subplot(1, 3, 2)
    # sns.scatterplot(data=df, x="flight_time", y="distance", hue="Cluster", palette="viridis")
    # plt.title("Flight Time vs. Distance")
    # plt.xlabel("Flight Time (hours)")
    # plt.ylabel("Distance (miles)")
    
    # # Plot 3: price vs. distance
    # plt.subplot(1, 3, 3)
    # sns.scatterplot(data=df, x="price", y="distance", hue="Cluster", palette="viridis")
    # plt.title("Price vs. Distance")
    # plt.xlabel("Price ($)")
    # plt.ylabel("Distance (miles)")
    
    # plt.tight_layout()
    # plt.show()
    