import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# FastAPI server URL
BASE_URL = "http://34.173.46.220:9000"

# Initialize `data` variable
data = None

# Fetch dataset from FastAPI
try:
    response = requests.get(f"{BASE_URL}/data", timeout=10)  # Add timeout for safety
    response.raise_for_status()
    json_data = response.json()
    
    # Check if data is valid
    if isinstance(json_data, list) and len(json_data) > 0:
        data = pd.DataFrame(json_data)
    else:
        st.error("Received data is empty or invalid.")
        st.stop()
except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch data from server: {e}")
    st.stop()
except ValueError:
    st.error("Failed to decode server response into valid JSON format.")
    st.stop()

# Validate that `data` is not empty
if data is None or data.empty:
    st.error("The dataset is empty or not loaded properly.")
    st.stop()

# Validate required columns
required_columns = ["Height", "Age", "Weight", "Age_Group_30"]
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"The dataset is missing required columns: {', '.join(missing_columns)}")
    st.stop()

# User interface
st.title("Obesity Data Dashboard")

# Column selection for statistics
st.subheader("Statistics Selection")
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
            json=payload,
            timeout=10  # Add timeout for safety
        )
        stats_response.raise_for_status()
        stats = stats_response.json()

        if "error" in stats:
            st.error(stats["error"])
        else:
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
    try:
        plt.figure(figsize=(8, 5))
        plt.plot(data['Age'], marker='o')
        plt.title("Line Plot of Age")
        plt.xlabel("Index")
        plt.ylabel("Age")
        st.pyplot(plt)
        st.caption("This plot shows the variation in age across the dataset.")
    except Exception as e:
        st.error(f"Error generating Line Plot of Age: {e}")

# Visualization 2: Scatter Plot (Height vs. Weight)
if "Height" in data.columns and "Weight" in data.columns:
    st.subheader("Scatter Plot of Height vs. Weight")
    try:
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x="Height", y="Weight", data=data)
        plt.title("Scatter Plot of Height vs. Weight")
        plt.xlabel("Height")
        plt.ylabel("Weight")
        st.pyplot(plt)
        st.caption("This scatter plot compares height and weight.")
    except Exception as e:
        st.error(f"Error generating Scatter Plot of Height vs. Weight: {e}")

# Visualization 3: Histogram (Age)
if "Age" in data.columns:
    st.subheader("Histogram of Age")
    try:
        plt.figure(figsize=(8, 5))
        sns.histplot(data['Age'], bins=20, kde=True)
        plt.title("Histogram of Age")
        plt.xlabel("Age")
        plt.ylabel("Frequency")
        st.pyplot(plt)
        st.caption("This histogram visualizes the distribution of age.")
    except Exception as e:
        st.error(f"Error generating Histogram of Age: {e}")

# Visualization 4: Box Plot by Age Group (Under 30 vs. 30 and Above)
if "Age_Group_30" in data.columns and "Weight" in data.columns:
    st.subheader("Box Plot of Weight by Age Group (Under 30 vs. 30 and Above)")
    try:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x="Age_Group_30", y="Weight", data=data)
        plt.title("Box Plot of Weight by Age Group")
        plt.xlabel("Age Group")
        plt.ylabel("Weight")
        st.pyplot(plt)
        st.caption("Box plot comparing weight by age group.")
    except Exception as e:
        st.error(f"Error generating Box Plot of Weight by Age Group: {e}")

# Visualization 5: Regression Plot (Height vs. Weight)
if "Height" in data.columns and "Weight" in data.columns:
    st.subheader("Linear Relationship of Height vs. Weight")
    try:
        sns.lmplot(x="Height", y="Weight", data=data, ci=None)
        plt.title("Height vs. Weight Linear Relationship")
        st.pyplot(plt)
        correlation = data['Height'].corr(data['Weight'])
        st.write(f"**Correlation Coefficient:** {correlation:.2f}")
        st.caption("The hypothesis suggests taller people are usually heavier.")
    except Exception as e:
        st.error(f"Error generating Regression Plot of Height vs. Weight: {e}")
