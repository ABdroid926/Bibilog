import streamlit as st 
import pandas as pd 
import requests 

SHEET = st.secrets["sheet"]
SCRIPT = st.secrets["script"]

st.set_page_config (
 page_title = "Bibilo",
 page_icon = "📚", 
 layout = "wide"
)

st.title("📚 Biblo library portal")



@st.cache_data 
def fetch_gsheet_data(tab_name) : 
 url = f"{SCRIPT}?tab={tab_name}" 
 df = pd.read_csv(url)
 return df 

with st.spinner("Great reads await you..."):
 users_df = fetch_gsheet_data("Users")
 books_df = fetch_gsheet_data("Books") 

choice = st.radio(
   "📌 Select your preferred action!",
   ('Log In!','Sign Up!'),
   index=0,
   horizontal = True    
)


if choice == 'Log In!' : 
   with st.form("Login_Form"):
      user_name = st.text_input("Please enter your username :")
      user_pass = st.text_input("Please enter your password :", type = "password")
      submit_button = st.form_submit_button(label="🚀 Log In!" ) 

   if submit_button: 
       user_row = users_df.loc[users_df['username']== user_name] 
       if not user_row.empty: 
          saved_pass = user_row['password'].iloc[0]
          if saved_pass == user_pass : 
             st.session_state['logged_in'] = True 
             st.rerun()  
          else:  
            st.error("❌ Password Incorrect!")
       else : 
         st.error("🤔 Username not found!") 

else : 
   with st.form("Sign_Up_Form"):
    USER_NAME = st.text_input("Please enter your username :")
    USER_PASS1 = st.text_input("Please enter your password : ", type = "password")
    USER_PASS2 = st.text_input("Please confirm your password :", type = "password")
    SUBMIT_BUTTON = st.form_submit_button(label= "🫆 Sign Up!") 


   if SUBMIT_BUTTON: 

      if not USER_NAME.strip() or not USER_PASS1.strip() or not USER_PASS2.strip(): 
         st.error("❌ Please fill out all of the fields!")
   
      elif USER_PASS1 != USER_PASS2 : 
          st.error("❌ Oops, Passwords do not match!") 
       
      elif not users_df.loc[users_df['username']== USER_NAME].empty :
         st.error("❌ Oops,Username already exists!")

      else :  
          payload = {'action': 'register','username':USER_NAME,'password':USER_PASS2}
          URL = st.secrets["script"] 
          response = requests.post(URL, json=payload)
                 
          if response.text == "Success" : 
            st.success( "✅ Account Created! Please do Log In!")
            st.cache_data.clear() 
            st.rerun()
          else : 
            st.error(f"❌ Oops, An Error Occurred: {response.text}")





         







  







   
