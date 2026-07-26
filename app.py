import streamlit as st
import pandas as pd 
import requests as rq 

st.set_page_config(
  page_title = "Bibilog",
  page_icon = "📚",
  layout = "wide" ,
)

st.title("📚 Bibilog : Library Management System")


radiobutton = st.radio("📌 Please do choose an action!",[" 📖 Log In!","✏️ Sign Up !"],horizontal = "True")         
