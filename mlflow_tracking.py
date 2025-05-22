import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('healthcare_dataset.csv')
features = ["Age", "Gender", "Medical Condition", "Medication", "Blood Type", "Admission Type"]
df_selected = df[features + ["Test Results"]].dropna()
df_encoded = pd.get_dummies(df_selected, columns=["Gender", "Medical Condition", "Medication", "Blood Type", "Admission Type"])
X = df_encoded.drop("Test Results", axis=1)
y = df_encoded["Test Results"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("healthcare_prediction")

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)

    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")

    print(f"Model accuracy: {acc}")

joblib.dump(model, "model.joblib")