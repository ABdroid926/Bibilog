import streamlit as st
import pandas as pd 
import requests as rq 

st.set_page_config(
  page_title = "Bibilog",
  page_icon = "📚",
  layout = "wide" ,
)

st.title("📚 Bibilog : Library Management System")
sheet_url = st.secrets["SHEET_URL"]

radiobutton = st.radio("📌 Please do choose an action!",[" 📖 Log In!","✏️ Sign Up !"],horizontal = True) 

if radiobutton == " 📖 Log In!" : 
  with st.form("LogIn_Page"): 
    user_name = st.text_input("Please do enter your username! :") 
    user_pass = st.text_input("Please do enter your password! :",type = "password") 
    submit = st.form_submit_button("🚀 Log In!") 
    
  if submit: 
    payload = {"action":"login","username": user_name,"password":user_pass}
    response = rq.post(sheet_url,json = payload) 
    result = response.text
    st.write(result)


   
