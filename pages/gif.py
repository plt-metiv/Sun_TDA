import streamlit as st
import altair as alt
import base64




st.set_page_config(
    page_title="Sun MagnetoGeram Persistanse Homology",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")



file = open(r"pages/matrix_animation.gif", 'rb')

contents = file.read()
data_url = base64.b64encode(contents).decode("utf-8")
file.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
    
)


