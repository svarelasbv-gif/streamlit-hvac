import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gsheet_client():
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

SPREADSHEET_ID = st.secrets["SHEET_ID"]
SHEET_NAME = "Sheet1"

def load_data():
    client = get_gsheet_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_sheet(df):
    client = get_gsheet_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

st.title("Prospección HVAC - Guadalajara")

df = load_data()

edited_df = st.experimental_data_editor(df, num_rows="dynamic")

if st.button("Guardar cambios en la nube"):
    update_sheet(edited_df)
    st.success("¡Datos guardados correctamente!")

st.markdown("💾 Los cambios (Estado/Notas) se guardan en tu Google Sheet.")
