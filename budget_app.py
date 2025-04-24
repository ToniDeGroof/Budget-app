import streamlit as st
import pandas as pd
from datetime import date
from openpyxl import load_workbook
import os

# Titel en layout
st.markdown("<h1 style='text-align: center;'>De Afrekening</h1>", unsafe_allow_html=True)
st.markdown("### Geef je uitgave in:")

# Formulier met nette indeling
with st.form("expense_form"):
    datum = st.date_input("Datum", value=date.today())
    winkel = st.text_input("Winkel")
    persoon = st.selectbox("Persoon", ["Jan", "Els"])
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

    # Opslaan
    volledige_data.to_excel(bestand, index=False)

    st.success("Uitgave toegevoegd!")
