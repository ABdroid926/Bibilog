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

else radiobutton == "✏️ Sign Up !"  
    with st.form("SignUp_Page"):
      new_user = st.text_input("Please do enter your username! :")
      new_pass = st.text_input("Please do enter your password! :",type="password")
      Submit = st.form_submit_button("🚀 Sign Up!")
      
    if Submit :   
      payload = {"action":"register","username":new_user,"password":user_pass}
      response = rq.post(sheet_url,json = payload)
      result = response.text 
       if result == "User Exists" : 
         st.error("❌ Oh dear.. that username is already taken! How about a new one!") 

       else : 
         st.success("✅ Alright! your new account is created! Please do Log In!!")
      
      
      

 
      


   
