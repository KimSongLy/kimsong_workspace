import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Correct the file path
file_path = r'[Enter_File_Path]'

# Read the CSV file
df = pd.read_csv(file_path)
df_copy = df

# Dataset Overview 
df_copy.info()

# Calculate WCSS (Within-Cluster Sum of Squares) for different number of clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i)
    kmeans.fit(rfm_scaled)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Method graph
plt.plot(range(1, 11), wcss)
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method')
plt.show()

# Calculate Recency, Frequency, and Monetary values

current_date = pd.to_datetime('2024-01-01')
rfm_df = paying_df.groupby('ID',).agg({
    'TRANSACTION_DATE': lambda x: (current_date - x.max()).days,
    'NUMBER_OF_TRANSACTION': 'sum',
    'TOTAL SALES': 'sum'
})

# Rename columns
rfm_df.columns = ['Recency', 'Frequency', 'Monetary']

# Display the RFM DataFrame
rfm_df.head()

# Check for None values
print(rfm_df.isnull().sum())

# Perform KMeans clustering
kmeans = KMeans(n_clusters=4)
rfm_df['Cluster'] = kmeans.fit_predict(rfm_df)

# Plot the clusters
plt.scatter(rfm_df['Recency'], rfm_df['Frequency'], c=rfm_df['Cluster'], cmap='viridis')
plt.xlabel('Recency')
plt.ylabel('Monetary')
plt.title('RFM Clusters')
plt.show()

# Display the RFM DataFrame with clusters
rfm_df.head()
