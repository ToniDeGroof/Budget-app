import streamlit as st
import pandas as pd
from datetime import date
from openpyxl import load_workbook
import os

# Titel en layout
st.markdown("<h1 style='text-align: left;'>De Afrekening</h1>", unsafe_allow_html=True)

# Formulier met nette indeling
with st.form("expense_form"):
    gekozen_datum = st.date_input("Datum", value=date.today())
    datum = gekozen_datum.strftime("%d/%m/%Y")
    winkel = st.text_input("Winkel")
    persoon = st.selectbox("Persoon", ["Toni", "Hilde"])
    bedrag = st.number_input("Bedrag (€)", min_value=0.01, format="%.2f")
    
    submitted = st.form_submit_button("Toevoegen")

if submitted:
    # Pad naar Excel-bestand (in dezelfde map als script)
    bestand = "uitgaven.xlsx"

    # Nieuwe rij met gegevens
    nieuwe_data = pd.DataFrame([[datum, winkel, persoon, bedrag]],
                               columns=["Datum", "Winkel", "Persoon", "Bedrag"])

    # Bestaat het bestand al?
    if os.path.exists(bestand):
        bestaande_data = pd.read_excel(bestand)
        volledige_data = pd.concat([bestaande_data, nieuwe_data], ignore_index=True)
    else:
        volledige_data = nieuwe_data

    # Google Sheets-authenticatie
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(credentials)

# Verbind met je Google Spreadsheet (pas naam aan indien nodig)
sheet = client.open("DeAfrekening").sheet1

# Formulier
with st.form("afrekening_formulier"):
    datum = st.date_input("Datum", format="DD/MM/YYYY")
    winkel = st.text_input("Winkel")
    persoon = st.selectbox("Persoon", ["Ik", "Partner"])
    bedrag = st.number_input("Bedrag", min_value=0.0, step=0.01, format="%.2f")
    verzenden = st.form_submit_button("Toevoegen")

    if verzenden:
        datum_str = datum.strftime("%d/%m/%Y")
        nieuwe_gegevens = [datum_str, winkel, persoon, str(bedrag)]
        sheet.append_row(nieuwe_gegevens)
        st.success("Gegevens toegevoegd aan Google Sheet!")


    # Opslaan
    volledige_data.to_excel(bestand, index=False)

    st.success("Uitgave toegevoegd!")
