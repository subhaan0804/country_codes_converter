import streamlit as st
from script import find_country_code
from script import load_country_dict_from_csv


st.text("CountryName to CountryCode Converter")
st.text_input("Country name", key="name")

if st.button("Convert"):
    all_countries_alpha2 = load_country_dict_from_csv('country_codes.csv')

    if not st.session_state.name:
        st.write("Please enter a country name.")
        st.stop()

    result = find_country_code(st.session_state.name, all_countries_alpha2)
    if result:
        st.write(f"{result[0]} : {result[1]}")
    else:
        st.write("Country not found")

