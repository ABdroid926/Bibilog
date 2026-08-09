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

if "username" not in st.session_state: 
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
            st.write(RESULT)
            
           
            
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
            
            if result.strip() == "User Exists":
                st.error("❌ Oh dear.. that username is already taken! How about a new one!")
            else:
                st.success("✅ Alright! your new account is created! Please do Log In!!")
                st.rerun()
else:
    if st.session_state["is_admin"] == "False":
        st.title(f"✨ Welcome {st.session_state['username']} ! ✨ ")
        payload = {"action": "get_user_books", "username": st.session_state["username"]}
        response = rq.post(sheet_url, json=payload)
         
        try:
            result = response.json() 
        except:
            result = response.text.strip()
             
        st.subheader("Your checked out books:") 
        for Books in result:
            with st.container(border=True):
                st.markdown(f"**:blue[{Books.get('title')}]**")
                st.markdown(f"- :blue[{Books.get('dueDate')[0:10]}]")
                st.markdown(f"- :blue[{Books.get('status')}]")

    elif st.session_state["is_admin"] == "True": 
        st.title("Admin Panel 🛡️") 
        st.divider()
        st.subheader("📥 Issue & Checkout Desk :")
        st.space("medium")
        left,center,right = st.columns([1,8,1])
        with center : 
         with st.form("Issue"):
             bookID = st.text_input("Enter Book ID")
             with st.container(border=True):
                lender_username = st.text_input("Enter Student Username") 
                loan_period = st.number_input("Loan Period(Days)", value=7)
                submit = st.form_submit_button("🚀 Issue book!", use_container_width = True)    

                if submit : 
                   payload = {"action": "issue_book","borrowed_by": lender_username,"bookID":bookID,"due_date":loan_period}
                   response = rq.post(sheet_url, json=payload) 
                   result = response.text 
                    
                   if result.strip() == "Success" :
                       st.success("Book Issued! Happy Reading!!") 
                   else :
                       st.error("❌ Oops, book not found! Please ensure the correct ID is entered")
        st.divider()
        st.space(size = "medium")  
        st.subheader("📋 Active Loans & Statuses")
        
        
        all_payload = {"action": "get_all_loans"} 
        all_response = rq.post(sheet_url, json=all_payload)
        all_result = all_response.text 

        with center : 
             for books in all_result : 
                 with st.container(border = True) :
                     st.markdown(f"**{books.get('title')}**")
                     st.markdown(f"- :grey[checked out by : {books.get('borrowed_by')}]")
                     st.markdown(f"- :grey[due on : {books.get('dueDate')}]")
                     st.markdown(f"- :green[ {books.get('status')}]") 
                     st.space(size = "small")
                     
                     
        
                       

                    


