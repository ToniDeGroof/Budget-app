import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Pad naar Excel-bestand (in dezelfde map als dit script)
excel_pad = "budget_data.xlsx"

# Als bestand niet bestaat, maak een lege tabel aan
if not os.path.exists(excel_pad):
    df_init = pd.DataFrame(columns=["Datum", "Winkel", "Persoon", "Bedrag"])
    df_init.to_excel(excel_pad, index=False)

st.title("De Afrekening")

# Formulier tonen
with st.form("boodschappen_formulier"):
    datum = st.date_input("Datum", value=datetime.today())
    winkel = st.text_input("Winkel")
    persoon = st.text_input("Persoon")
    bedrag = st.number_input("Bedrag", format="%.2f", step=0.01)

    verzenden = st.form_submit_button("Toevoegen aan Excel")

    if verzenden:
        nieuwe_data = pd.DataFrame({
            "Datum": [datum.strftime("%d-%m-%Y")],
            "Winkel": [winkel],
            "Persoon": [persoon],
            "Bedrag": [bedrag]
        })

        # Gegevens opslaan
        bestaand = pd.read_excel(excel_pad)
        totaal = pd.concat([bestaand, nieuwe_data], ignore_index=True)
        totaal.to_excel(excel_pad, index=False)

        st.success("Gegevens toegevoegd aan Excel!")