# Egészségügyi Predikciós Rendszer - MLSecOps Projekt

Ez a projekt egy komplett MLSecOps pipeline-t valósít meg egy egészségügyi osztályozó modell köré építve. A rendszer képes predikciókat adni REST API-n keresztül, naprakész monitoringot biztosít Streamlitben EvidentlyAI-al, és Airflow segítségével automatizált újratanítást is támogat.

---

## Tartalom

- `main.py`: REST API FastAPI-vel a predikcióhoz
- `mlflow_tracking.py`: Modell tanítás és MLflow tracking
- `app.py`: Streamlit dashboard adatdrift riporttal (Evidently)
- `dag.py`: Airflow DAG a modell időszakos újratanítására
- `Dockerfile`: A projekt konténerizálásához
- `data/healthcare_dataset.csv`: Referenciaadat
- `test_input.csv`: Tesztadat a dashboardhoz
- `requirements.txt`: Függőségek listája

---
## 0. package telepítése 
```bash
pip install -r requirements.txt
```


## 1. Használat: Modell tanítása, MLflow tracking és REST API indítása
```bash
# Először tanítsd meg a modellt:
python mlflow_tracking.py

# Majd indítsd el az API-t:
python -m uvicorn main:app --reload


# Dokumentáció:
http://127.0.0.1:8000/docs


### Minta input:

{
  "Age": 25,
  "Gender": "Female",
  "Medical_Condition": "None",
  "Medication": "None",
  "Blood_Type": "B+",
  "Admission_Type": "Elective"
}
```



## 2. Streamlit dashboard indítása
```bash
streamlit run app.py

Majd:http://localhost:8501

- Tölts fel egy `test_input.csv`-t
- A rendszer összehasonlítja a referenciaadatokkal
- Evidently riport automatikusan megjelenik

```

## 3. Airflow indítás Dockerrel
```bash
# A dag.py tartalmaz egy heti újratanítást
# A modell a /opt/airflow/models mappába kerül

```bash
docker compose -f docker-compose-airflow-8088.yaml run airflow-init
docker compose -f docker-compose-airflow-8088.yaml up -d

Majd: http://localhost:8088
login: admin / admin
```

## Screenshotok a beadandóhoz
API test_request body
API test_response body
Streamlit
Tested_Streamlit
DAG

---

## Fejlesztési környezet
- Python 3.10
- pip, venv vagy conda
- streamlit, evidently==0.3.3, scikit-learn, pandas, fastapi, uvicorn, mlflow

---

## Készítette: Kerner Kinga (J8JSRN)
MLSecOps beadandó - Óbudai Egyetem
2025
