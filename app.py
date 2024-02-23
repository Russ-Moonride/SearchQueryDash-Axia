import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")


def password_protection():
  if 'authenticated' not in st.session_state:
      st.session_state.authenticated = False
      
  if not st.session_state.authenticated:
      password = st.text_input("Enter Password:", type="password")
      
      if st.button("Login"):
          if password == "SQR":
              st.session_state.authenticated = True
              main_dashboard()
          else:
              st.error("Incorrect Password. Please try again or contact the administrator.")
  else:
        main_dashboard()

def get_top_ngrams(corpus, n=None, ngram_range=(1,1)):
    vec = CountVectorizer(stop_words='english', ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]

def main_dashboard():

    st.markdown(f"<h1 style='text-align: center;'>Search Query Analysis</h1>", unsafe_allow_html=True)

    data = pd.read_csv("Search terms report.csv", skiprows=2)

    Unadded_data = data[data["Added/Excluded"] == "None"]

    # N-Gram Analysis
    st.subheader('Top N-Grams from Search Terms')
    col1, col2,_,_ = st.columns(4)
    with col1:
        ngram_start = st.number_input('N-Gram Start', min_value=1, max_value=5, value=1)
    with col2:
        ngram_end = st.number_input('N-Gram End', min_value=1, max_value=5, value=2)
    col3,col4 = st.columns(2)
    with col3:
        top_ngrams = get_top_ngrams(Unadded_data['Search term'], n=10, ngram_range=(ngram_start, ngram_end))
        fig, ax = plt.subplots()
        ax.barh([x[0] for x in top_ngrams], [x[1] for x in top_ngrams])
        ax.set_xlabel('Frequency')
        ax.set_title('Top N-Grams from Search Terms')
        st.pyplot(fig)
    
    with col4:
        top_click = Unadded_data.nlargest('Impr.', 20)
        st.write(top_click)
    


if __name__ == '__main__':
    password_protection()
