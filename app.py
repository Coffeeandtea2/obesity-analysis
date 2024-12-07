
import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# FastAPI server URL
BASE_URL = "https://alive-mallard-whole.ngrok-free.app"

# Fetch dataset from FastAPI
try:
    response = requests.get(f"{BASE_URL}/data")
    response.raise_for_status()
    data = pd.DataFrame(response.json())
    st.write("Available columns:", data.columns.tolist())  # Debugging: Show available columns
except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch data from server: {e}")
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
    st.write(f"Sending payload: {payload}")  # Debugging: Display the payload being sent
    try:
        stats_response = requests.post(
            f"{BASE_URL}/statistics",
            json=payload  # Send payload as JSON
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
st.subheader("Line Plot of Age")
plt.figure(figsize=(8, 5))
plt.plot(data['Age'], marker='o')
plt.title("Line Plot of Age")
plt.xlabel("Index")
plt.ylabel("Age")
st.pyplot(plt)
st.caption("This plot shows the variation in age across the dataset's index. The ages fluctuate rapidly, indicating a diverse range of ages without any apparent sequential trend across the indices.")

# Visualization 2: Scatter Plot (Height vs. Weight)
st.subheader("Scatter Plot of Height vs. Weight")
plt.figure(figsize=(8, 5))
sns.scatterplot(x="Height", y="Weight", data=data)
plt.title("Scatter Plot of Height vs. Weight")
plt.xlabel("Height")
plt.ylabel("Weight")
st.pyplot(plt)
st.caption("This scatter plot compares the height and weight of individuals in the dataset. The data points are scattered broadly, indicating variability in the relationship between height and weight, but there is no strong visible trend or pattern suggesting a direct linear correlation.")

# Visualization 3: Histogram (Age)
st.subheader("Histogram of Age")
plt.figure(figsize=(8, 5))
sns.histplot(data['Age'], bins=20, kde=True)
plt.title("Histogram of Age")
plt.xlabel("Age")
plt.ylabel("Frequency")
st.pyplot(plt)
st.caption("This histogram visualizes the distribution of age within the dataset. The data is spread across different age groups, with some groups having higher counts. The blue line overlays a kernel density estimate (KDE), showing the smoothed probability density of age distribution. Peaks in the histogram correspond to age groups with higher frequencies.")

# Visualization: Box Plot by Age Group (Under 30 vs. 30 and Above)
st.subheader("Box Plot of Weight by Age Group (Under 30 vs. 30 and Above)")
plt.figure(figsize=(8, 5))
sns.boxplot(x="Age_Group_30", y="Weight", data=data)
plt.title("Box Plot of Weight by Age Group (Under 30 vs. 30 and Above)")
plt.xlabel("Age Group")
plt.ylabel("Weight")
st.pyplot(plt)
st.caption("For Age 30 and Below:Median weight is higher compared to the older group. There is less variability in weight, with fewer outliers at the higher end.")
st.caption("For Age Above 30::The median weight is slightly lower. The spread of weights is wider, with more outliers on both ends, especially at the higher range.")

# Visualization 5: Regression Plot (Height vs. Weight)
st.subheader("Linear Relationship of Height vs. Weight")
st.caption("My Hypothesis: People with higher height are generally heavier.")
sns.lmplot(x="Height", y="Weight", data=data, ci=None)
plt.title("Height vs. Weight Linear Relationship")
st.pyplot(plt)
correlation = data['Height'].corr(data['Weight'])  # Compute the Pearson correlation coefficient
st.write(f"**Correlation Coefficient:** {correlation:.2f}")
st.caption("The hypothesis suggests that taller people are usually heavier, but the data does not show a strong connection between height and weight. The scatter plot may show some differences, but the low correlation means that other factors likely have a bigger impact on weight than height in this dataset.")
