import streamlit as st
import subprocess
import pandas as pd
import plotly.graph_objects as go
import dash
from src.detect import detect
df=pd.read_csv("./dataset.csv")
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
df2=df[['Address', 'Sent tnx','Received Tnx','Number of Created Contracts','total Ether sent','total ether received','total ether balance','FLAG']]



# Set the page title and favicon
st.set_page_config(
    page_title="DMD",
    page_icon=":bar_chart:",
    layout="wide",
)

# Create a container for the header with a black background
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
    .sidebar .css-14ryutq {
        font-family: 'Fira Code', monospace;
    }

    /* Specify the font for the content */
    .content .css-vfskoc {
        font-family: 'Fira Code', monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#

# Add the navigation links with white text to the right side
with header_container:
# Create a row
    col1,col2,col3,col4=st.columns([1,1,1,1])

# Add a button to the row
    with col1:
        st.image("./assets/Frame 2.png", use_column_width=169.87)

    st.markdown(
        '<ul class="nav-links">'
  
        '</ul>',
        unsafe_allow_html=True,
    )
st.sidebar.write("Navigation")
page = st.sidebar.radio("Go to:", ["🏡Home", "🎯Detector", "ℹ️ About"])

# Define content for each "page"
if page == "🏡Home":
    st.title("Home Page")
    # Display an image below the header
    st.image("./Frame 12.png", use_column_width=True)


elif page == "🎯Detector":
    st.title("Detector")
    
    button1 = st.button("../")
    vert_space = '<div style="padding: 50px 5px;"></div>'
    st.markdown(vert_space, unsafe_allow_html=True)

    wallet_address = st.text_input("Wallet Address", key="wallet_input", value="")
    percentage = detect(wallet_address) # You can change this percentage value

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

elif page == "ℹ️ About":
    st.title("About")
    
    st.image("./Frame 7.png", use_column_width=True)




