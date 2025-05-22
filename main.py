from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("model.joblib")

class PatientData(BaseModel):
    Age: int
    Gender: str
    Medical_Condition: str
    Medication: str
    Blood_Type: str
    Admission_Type: str

@app.post("/predict")
def predict(data: PatientData):
    input_dict = data.dict()
    df_input = pd.DataFrame([input_dict])

    # One-hot encoding to match training data structure
    df_encoded = pd.get_dummies(df_input)

    # Get the columns the model was trained on (assumed to be saved from training)
    trained_cols = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else df_encoded.columns
    for col in trained_cols:
        if col not in df_encoded.columns:
            df_encoded[col] = 0  # add missing columns with 0
    df_encoded = df_encoded[trained_cols]  # ensure column order

    prediction = model.predict(df_encoded)[0]
    return {"prediction": str(prediction)}