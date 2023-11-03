import streamlit as st
import subprocess

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
        padding: 10px;
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

#

# Add the navigation links with white text to the right side
with header_container:
# Create a row
    col1,col2,col3,col4=st.columns([1,1,1,1])

# Add a button to the row
    with col1:
        st.image("./assets/Frame 2.png", use_column_width=169.87)
    with col2:
        button1 = st.button("HOME")
    with col3:
        button2 = st.button("DETECTOR")
    with col4:
        button3 = st.button("ABOUT")

    if button1:
        subprocess.run(["streamlit", "run", "home.py"])
    if button2:
        subprocess.run(["streamlit", "run", "detector.py"])
    if button3:
        subprocess.run(["streamlit", "run", "about.py"])

    st.markdown(
        '<ul class="nav-links">'
  
        '</ul>',
        unsafe_allow_html=True,
    )
    st.image("./Frame 7.png", use_column_width=True)

