import streamlit as st
import subprocess
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Input, Output

df=pd.read_csv("./dataset.csv")
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
df2=df[['Address', 'Sent tnx','Received Tnx','Number of Created Contracts','total Ether sent','total ether received','total ether balance','FLAG']]


st.set_page_config(
    page_title="DMD",
    page_icon=":bar_chart:",
    layout="wide"
)
app = dash.Dash(__name__)



header_container = st.container()
header_container.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css?family=Fira+Code:400,500,600,700&display=swap');
    .fira-code-font {
        font-family: 'Fira Code', monospace;
    }
    .header-container {
        background-color: #000000;
        color: #ffffff;
        position: absolute;
        top: 0;
        right: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-links {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
    }
    .nav-link {
        margin-right: 20px;
        cursor: pointer;
    }
    .text-input-container {
        width: 500px;
        border: 2px solid #ffffff;
        border-radius: 5px;
        padding: 10px;
    }
    .text-input-label {
        color: #ffffff;
        font-size: 18px;
        margin-bottom: 10px;
    
    }
        .dirt-score {
        color: #ffffff;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .center-content {
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



with header_container:

    col1,col2,col3,col4=st.columns([1,1,1,1])


    with col1:
        button1 = st.button("../")

    if button1:
        subprocess.run(["streamlit", "run", "home.py"])
    st.markdown(
        '<ul class="nav-links">'
  
        '</ul>',
        unsafe_allow_html=True,
    )
vert_space = '<div style="padding: 50px 5px;"></div>'
st.markdown(vert_space, unsafe_allow_html=True)




wallet_address = st.text_input("Wallet Address", key="wallet_input", value="")
percentage = 95  # You can change this percentage value

# Set the text color based on the percentage
if percentage > 65:
    text_color = 'red'
else:
    text_color = 'green'



if wallet_address:
    if wallet_address in df2['Address'].unique():
        st.write(f"Entered Wallet Address: {wallet_address}")
        st.markdown('<div class="fira-code-font" style="text-align: center; font-size: 20px;">Dirt Score</div>', unsafe_allow_html=True)
        st.write(f"<div class='center-content fira-code-font' style='color: {text_color}; font-size: 36px;'><b>{percentage}</b></div>", unsafe_allow_html=True)


        df3 = df2.loc[df2['Address'] == wallet_address] 
        st.write(df3)
    else:
        st.write(df2)
