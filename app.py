import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# FastAPI server URL
BASE_URL = "http://34.173.46.220:9000"

# Initialize data variable
data = None

# Fetch dataset from FastAPI
try:
    response = requests.get(f"{BASE_URL}/data")
    response.raise_for_status()
    json_data = response.json()
    
    # Validate if the response contains valid data
    if isinstance(json_data, list) and len(json_data) > 0:
        data = pd.DataFrame(json_data)
    else:
        st.error("Received data is empty or invalid.")
        st.stop()
except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch data from server: {e}")
    st.stop()

# Validate that `data` is not empty
if data.empty:
    st.error("The dataset is empty. Please check the server or data source.")
    st.stop()

# User interface
st.title("Obesity Data Dashboard")
# Limit the selection to Height, Age, and Weight columns
selected_column = st.selectbox(
    "Select a column for statistics",
    options=["Height", "Age", "Weight"],
    key="selectbox_statistics"
)

if st.button("Fetch Statistics"):
    payload = {"column": selected_column}
    try:
        stats_response = requests.post(
            f"{BASE_URL}/statistics",
            json=payload
        )
        stats_response.raise_for_status()
        stats = stats_response.json()

        if "error" in stats:
            st.error(stats["error"])
        else:
            # Only display mean, standard deviation, and median
            st.write(f"**Mean of {selected_column}:** {stats['mean']}")
            st.write(f"**Standard Deviation of {selected_column}:** {stats['std']}")
            st.write(f"**Median of {selected_column}:** {stats['median']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch statistics: {e}")

# Display dataset
st.subheader("Dataset")
st.dataframe(data)

# Visualization 1: Line Plot (Age)
if "Age" in data.columns:
    st.subheader("Line Plot of Age")
    plt.figure(figsize=(8, 5))
    plt.plot(data['Age'], marker='o')
    plt.title("Line Plot of Age")
    plt.xlabel("Index")
    plt.ylabel("Age")
    st.pyplot(plt)
    st.caption("This plot shows the variation in age across the dataset.")
else:
    st.error("The dataset does not contain the 'Age' column.")

# Visualization 2: Scatter Plot (Height vs. Weight)
if "Height" in data.columns and "Weight" in data.columns:
    st.subheader("Scatter Plot of Height vs. Weight")
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="Height", y="Weight", data=data)
    plt.title("Scatter Plot of Height vs. Weight")
    plt.xlabel("Height")
    plt.ylabel("Weight")
    st.pyplot(plt)
    st.caption("This scatter plot compares height and weight.")
else:
    st.error("The dataset does not contain 'Height' and 'Weight' columns.")

# Visualization 3: Histogram (Age)
if "Age" in data.columns:
    st.subheader("Histogram of Age")
    plt.figure(figsize=(8, 5))
    sns.histplot(data['Age'], bins=20, kde=True)
    plt.title("Histogram of Age")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    st.pyplot(plt)
    st.caption("This histogram visualizes the distribution of age.")
else:
    st.error("The dataset does not contain the 'Age' column.")

# Visualization: Box Plot by Age Group (Under 30 vs. 30 and Above)
if "Age_Group_30" in data.columns:
    st.subheader("Box Plot of Weight by Age Group (Under 30 vs. 30 and Above)")
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="Age_Group_30", y="Weight", data=data)
    plt.title("Box Plot of Weight by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Weight")
    st.pyplot(plt)
    st.caption("Box plot by age group: Under 30 vs. 30 and Above.")
else:
    st.error("The dataset does not contain the 'Age_Group_30' column.")

# Visualization 5: Regression Plot (Height vs. Weight)
if "Height" in data.columns and "Weight" in data.columns:
    st.subheader("Linear Relationship of Height vs. Weight")
    sns.lmplot(x="Height", y="Weight", data=data, ci=None)
    plt.title("Height vs. Weight Linear Relationship")
    st.pyplot(plt)
    correlation = data['Height'].corr(data['Weight'])
    st.write(f"**Correlation Coefficient:** {correlation:.2f}")
    st.caption("The hypothesis suggests taller people are usually heavier.")
else:
    st.error("The dataset does not contain 'Height' and 'Weight' columns.")
