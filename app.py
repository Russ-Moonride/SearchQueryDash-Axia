import pandas as pd
import streamlit as st

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")


def password_protection():
  if 'authenticated' not in st.session_state:
      st.session_state.authenticated = False
      
  if not st.session_state.authenticated:
      password = st.text_input("Enter Password:", type="password")
      
      if st.button("Login"):
          if password == correct_hashed_password:
              st.session_state.authenticated = True
              main_dashboard()
          else:
              st.error("Incorrect Password. Please try again or contact the administrator.")
  else:
      main_dashboard()

  def mainmain_dashboard():

    st.markdown(f"<h1 style='text-align: center;'>{Account} Search Query Analysis</h1>", unsafe_allow_html=True)

    data = pd.read_csv("Search terms report.csv")

    st.write(data)
