from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load and preprocess the data
file_path = "obesity_data.csv"

try:
    df = pd.read_csv(file_path)
    df_cleaned = df.dropna()
    df_cleaned['Age'] = pd.to_numeric(df_cleaned['Age'], errors='coerce')
    df_cleaned['Height'] = pd.to_numeric(df_cleaned['Height'], errors='coerce')
    df_cleaned['Weight'] = pd.to_numeric(df_cleaned['Weight'], errors='coerce')
    df_cleaned['Age_Group'] = pd.cut(
        df_cleaned['Age'], bins=[0, 18, 30, 50, 100],
        labels=['Child', 'Young Adult', 'Adult', 'Senior']
    )
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="File not found: obesity_data.csv")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Request model
class StatisticsRequest(BaseModel):
    column: str

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is working!"}

# Endpoint to launch Streamlit
@app.get("/streamlit")
def launch_streamlit():
    """Run the Streamlit app."""
    streamlit_script = "app.py"  # Your Streamlit script
    streamlit.web.bootstrap.run(streamlit_script, "", [], {})
    return {"message": "Streamlit is running!"}

@app.get("/data")
def get_data():
    """
    Return the cleaned dataset with 'Age_Group_30' column.
    """
    # Ensure the column is added
    df_cleaned['Age_Group_30'] = df_cleaned['Age'].apply(lambda age: "Under 30" if age < 30 else "30 and Above")
    return df_cleaned.to_dict(orient="records")


@app.post("/statistics")
def post_statistics(request: StatisticsRequest):
    """
    Calculate mean, standard deviation, and median for a specific column.
    """
    column = request.column
    if column not in ["Height", "Age", "Weight"]:
        raise HTTPException(status_code=404, detail=f"Column '{column}' not found or not allowed")

    try:
        stats = {
            "mean": float(df_cleaned[column].mean()),  # Ensure JSON serializable
            "std": float(df_cleaned[column].std()),    # Standard Deviation
            "median": float(df_cleaned[column].median()),  # Median
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

