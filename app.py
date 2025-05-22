import streamlit as st
import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import os

st.set_page_config(layout="wide")
st.title("Egészségügyi Modell Drift Monitor")

uploaded_file = st.file_uploader("Tölts fel új adatmintát (CSV)", type="csv")

if uploaded_file:
    new_data = pd.read_csv(uploaded_file)
    st.subheader("Feltöltött új adat")
    st.dataframe(new_data)

    # Referencia adat elérési út
    ref_path = os.path.join("data", "healthcare_dataset.csv")
    if os.path.exists(ref_path):
        ref_data = pd.read_csv(ref_path)
        st.subheader("Referenciadata betöltve")

        # Csak a közös oszlopokat használjuk
        common_cols = list(set(ref_data.columns) & set(new_data.columns))
        ref_data = ref_data[common_cols]
        new_data = new_data[common_cols]

        # Drift riport generálása új Evidently API-val
        column_mapping = ColumnMapping()
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=ref_data, current_data=new_data, column_mapping=column_mapping)
        report.save_html("drift_report.html")

        # Jelentés beágyazása
        with open("drift_report.html", encoding='utf-8') as f:
            html = f.read()
            st.components.v1.html(html, height=1000, scrolling=True)

    else:
        st.warning("Nem található a referenciadata (data/healthcare_dataset.csv)")