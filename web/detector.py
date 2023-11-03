import streamlit as st
import subprocess
import pandas as pd
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
    </style>
    """,
    unsafe_allow_html=True,
)


# Add the navigation links with white text to the right side
with header_container:
# Create a row
    col1,col2,col3,col4=st.columns([1,1,1,1])

# Add a button to the row
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



# Input text box with custom style
wallet_address = st.text_input("Wallet Address", key="wallet_input", value="")


if wallet_address:
    if wallet_address in df2['Address'].unique():
        st.write(f"Entered Wallet Address: {wallet_address}")
        
        df3 = df2.loc[df2['Address'] == wallet_address] 
        st.write(df3)
    else:
        st.write(df2)