import streamlit as st
import pandas as pd
from datetime import date
import requests

st.write("Hello, welcome to the Daily Bible Reading Plan!")

bible = pd.read_csv("bible_reading_plan.csv")

current_year = date.today().year
bible["Date"] = pd.to_datetime(
    bible["Date"] + "-" + str(current_year),
    format="%d-%b-%Y"
).dt.date
bible["Date"] = pd.to_datetime(bible["Date"], format="%Y-%m-%d").dt.date
today = date.today()
today_reading = bible[bible["Date"] == today]

st.write("Today is: ", today)

if st.button("Today's Reading: "): 
    if not today_reading.empty:
        st.subheader("Today's Bible Reading")
        passage1 = today_reading.iloc[0]["Passage 1"]
        passage2 = today_reading.iloc[0]["Passage 2"]
        st.write(f"Reading 1: {passage1}")
        st.write(f"Reading 2: {passage2}")
    else:
        st.write("No reading scheduled for today.")