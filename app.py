import streamlit as st
import pandas as pd
import requests as rq

st.set_page_config(
    page_title="Bibilog",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Bibilog : Library Management System")
st.divider()
sheet_url = st.secrets["SHEET_URL"]

if "logged in" not in st.session_state:
    st.session_state["logged in"] = "False"

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = "False"

if "username" not in st.session_state : 
    st.session_state["username"] = ""

if st.session_state["logged in"] == "False":
    radiobutton = st.radio("📌 Please do choose an action!", [" 📖 Log In!", "✏️ Sign Up !"], horizontal=True)

    if radiobutton == " 📖 Log In!":
        with st.form("LogIn_Page"):
            user_name = st.text_input("Please do enter your username! :").strip()
            user_pass = st.text_input("Please do enter your password! :", type="password").strip()
            submit = st.form_submit_button("🚀 Log In!")
            
        if submit:
            payload = {"action": "login", "username": user_name, "password": user_pass}
            response = rq.post(sheet_url, json=payload)
            RESULT = response.text
            
            if RESULT == "Success":
                st.session_state["logged in"] = "True"
                st.session_state["is_admin"] = "False"
                st.session_state["username"] = user_name
                st.rerun()
                
            elif RESULT == "Admin Success":
                st.session_state["logged in"] = "True"
                st.session_state["is_admin"] = "True"
                st.rerun()
                
            else:
                st.error("❌ Oops, we couldn't find your account. Please check your credentials!!")
    
    elif radiobutton == "✏️ Sign Up !":
        with st.form("SignUp_Page"):
            new_user = st.text_input("Please do enter your username! :").strip()
            new_pass = st.text_input("Please do enter your password! :", type="password").strip()
            SUBMIT = st.form_submit_button("🚀 Sign Up!")
            
        if SUBMIT:
            payload = {"action": "register", "username": new_user, "password": new_pass}
            response = rq.post(sheet_url, json=payload)
            result = response.text
            
            if result == "User Exists":
                st.error("❌ Oh dear.. that username is already taken! How about a new one!")
            else:
                st.success("✅ Alright! your new account is created! Please do Log In!!")
                st.rerun()
else:
     if  st.session_state["is_admin"] == "False" :
         st.title(f"Welcome {st.session_state["username"]} !",text_alignment = "centre")
         st.write()
         st.write()
         st.divider() 
         







 
      


   
