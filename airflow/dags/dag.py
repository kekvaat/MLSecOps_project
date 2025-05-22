from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Alap értékek beállítása
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Modelltanítás logikája
def train_model():
    import pandas as pd
    import os
    import joblib
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    df = pd.read_csv('/opt/airflow/data/healthcare_dataset.csv')
    features = ["Age", "Gender", "Medical Condition", "Medication", "Blood Type", "Admission Type"]
    df = df[features + ["Test Results"]].dropna()

    df_encoded = pd.get_dummies(df, columns=["Gender", "Medical Condition", "Medication", "Blood Type", "Admission Type"])
    X = df_encoded.drop("Test Results", axis=1)
    y = df_encoded["Test Results"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs("/opt/airflow/models", exist_ok=True)
    joblib.dump(model, "/opt/airflow/models/trained_model.pkl")

# DAG definíció
dag = DAG(
    'healthcare_model_retraining',
    default_args=default_args,
    description='Egészségügyi modell újratanítás heti gyakorisággal',
    schedule_interval='@weekly',
    catchup=False
)

retrain_task = PythonOperator(
    task_id='train_model_task',
    python_callable=train_model,
    dag=dag
)
