import streamlit as st
import os
import time
from datetime import datetime, timedelta
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import pandas as pd
from cyprus import Scraping



# def main():
#     st.set_page_config(page_title="Corporate Registry Agent", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")
    
#     # Apply custom CSS for dark theme improvements
#     st.markdown("""
#     <style>
#         .css-1v3fvcr {  /* Input placeholder color */
#             color: #ccc !important;
#         }
#         .stTextInput input {
#             color: #fff !important;
#         }
#         .css-1v3fvcr input::placeholder {
#             color: #ccc !important;
#         }
#         html {
#             scroll-behavior: smooth;
#         }
#         h1 {
#             text-align: center;
#             color: #F89880 !important;
#             text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5);
#         }
#         .stButton button:hover {
#             background-color: white;
#             transform: scale(1.05);
#             cursor: pointer;
#         }
#         .stDataFrame {
#             box-shadow: 0 4px 8px #192734 !important; /* Add shadow to table */
#             border-radius: 8px !important;
#             overflow: hidden;
#             box-shadow: 0px 8px 16px ;
#             padding: 10px;
#         }
#         .stForm{
#             box-shadow: 0px 8px 16px #192734;
#             border-radius: 10px;
#             padding: 20px;
#         }
#     </style>
#     """, unsafe_allow_html=True)


#     st.title("Corporate Registry Agent")
#     # Create a form-like structure
#     with st.form(key='input_form'):
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("**Enter URL:**")
#             url = st.text_input(" ", placeholder="https://example.com", label_visibility="hidden")
#         with col2:
#             st.markdown("**Enter the company name:**")
#             name = st.text_input(" ", placeholder="Example Corp", label_visibility="hidden")

#         # Option to run in headless mode
#         headless = st.checkbox("Run in Headless Mode", value=True, help="Enable to run browser in background, disable to see the browser automation")

#         # Submit button for the form
#         submit_button = st.form_submit_button(label='Search')

#     # Proceed only if the user submits the form
#     if submit_button:
#         progress_bar = st.progress(0)
#         time_placeholder = st.empty()

#         with st.spinner("Processing... Please wait."):
#             task = Scraping(url, name, headless, progress_bar, time_placeholder)
#             with open(task, 'r', encoding='utf-8') as f:
#                 data = json.load(f)

#         st.header("Corporate Data")
        
#         def display_table(data, title):
#             st.subheader(title)
#             if isinstance(data, list):
#                 if data:
#                     if all(isinstance(i, str) for i in data[0]):
#                         headers = data[0]
#                         df = pd.DataFrame(data[1:], columns=headers)
#                     else:
#                         df = pd.DataFrame(data)
#                     st.dataframe(df)
#                 else:
#                     st.write("No data available")
#             elif isinstance(data, dict):
#                 df = pd.DataFrame(list(data.items()), columns=["Field", "Value"])
#                 st.dataframe(df, width=1200)

#         # Display each section of the scraped data
#         display_table(data.get("Organization details", {}), "Organization Details")
#         display_table(data.get("File Status", {}), "File Status")
#         display_table(data.get("Additional Tables", []), "Additional Tables")
#         display_table(data.get("Directors and Secretaries", []), "Directors and Secretaries")
#         display_table(data.get("HE32 Archive", []), "HE32 Archive")
#         display_table(data.get("Registered Office", {}), "Registered Office")
#         display_table(data.get("Preview File Type", []), "Preview File Type")
#         display_table(data.get("Charges and Mortgages", []), "Charges and Mortgages")
#         display_table(data.get("Translations", []), "Translations")



# if __name__ == "__main__":
#     main()


#Changed UI for Option based region enhancement.
import streamlit as st
import time
import json
import pandas as pd

def main():
    st.set_page_config(page_title="Corporate Registry Agent", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")
    
    # Apply custom CSS for dark theme improvements
    st.markdown("""
    <style>
        .css-1v3fvcr {  /* Input placeholder color */
            color: #ccc !important;
        }
        .stTextInput input {
            color: #fff !important;
        }
        .css-1v3fvcr input::placeholder {
            color: #ccc !important;
        }
        html {
            scroll-behavior: smooth;
        }
        h1 {
            text-align: center;
            color: #F89880 !important;
            text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5);
        }
        .stButton button:hover {
            background-color: white;
            transform: scale(1.05);
            cursor: pointer;
        }
        .stDataFrame {
            box-shadow: 0 4px 8px #192734 !important; /* Add shadow to table */
            border-radius: 8px !important;
            overflow: hidden;
            box-shadow: 0px 8px 16px ;
            padding: 10px;
        }
        .stForm{
            box-shadow: 0px 8px 16px #192734;
            border-radius: 10px;
            padding: 20px;
        }
        /* Custom cursor for dropdown and other interactive elements */
        .css-1v3fvcr, .stSelectbox, .stTextInput, .stButton {
            cursor: pointer !important;
        }
        /* Style for dropdown to prevent it from being editable */
        .stSelectbox select {
            cursor: pointer !important;
            -webkit-appearance: none; /* Remove default browser styling */
            -moz-appearance: none;
            appearance: none;
            padding-right: 30px; /* Optional: space for custom arrow */
        }

        /* Custom arrow for the dropdown */
        .stSelectbox select::after {
            content: '\25BC'; /* Downward arrow */
            font-size: 12px;
            color: #ccc;
            padding-left: 10px;
        }
        /* Prevent user from typing in the select box */
        .stSelectbox select:focus {
            outline: none !important;
        }
        /* Hide empty labels above text fields */
        label:has(div:empty) {
        display: none !important;
        }
        /* Style for the selectbox container */
        .stSelectbox div[data-baseweb="select"] {
            cursor: pointer !important; /* Change cursor to pointer */
        }
        /* Prevent selectbox from being editable */
        .stSelectbox input {
            pointer-events: none !important; /* Disable typing inside */
            caret-color: transparent !important; /* Hide text cursor */
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Corporate Registry Agent")
    
    # Define the country selection dropdown and URL mapping
    country_url_mapping = {
        "Cyprus": "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU",
        # Add more countries and their URLs as needed
    }

    # Create a form-like structure
    with st.form(key='input_form'):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Enter the company name:**")
            company_name = st.text_input(" ", placeholder="Example Corp", label_visibility="hidden")
        with col2:
            st.markdown("**Select the Region:**")
            country = st.selectbox(" ",list(country_url_mapping.keys()), label_visibility="hidden")
        
        # Option to run in headless mode
        headless = st.checkbox("Run in Headless Mode", value=False, help="Enable to run browser in background, disable to see the browser automation")

        # Submit button for the form
        submit_button = st.form_submit_button(label='Search')

    # Proceed only if the user submits the form
    if submit_button:
        if country != "Select the country" and company_name:
            # Get the URL based on the selected country
            url = country_url_mapping.get(country)
            
            if url:
                progress_bar = st.progress(0)
                time_placeholder = st.empty()

                with st.spinner("Processing... Please wait."):
                    task = Scraping(url, company_name, headless, progress_bar, time_placeholder)  # Assuming headless=True
                    with open(task, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                st.header("Corporate Data")
                
                def display_table(data, title):
                    st.subheader(title)
                    if isinstance(data, list):
                        if data:
                            if all(isinstance(i, str) for i in data[0]):
                                headers = data[0]
                                df = pd.DataFrame(data[1:], columns=headers)
                            else:
                                df = pd.DataFrame(data)
                            st.dataframe(df)
                        else:
                            st.write("No data available")
                    elif isinstance(data, dict):
                        df = pd.DataFrame(list(data.items()), columns=["Field", "Value"])
                        st.dataframe(df, width=1200)

                # Display each section of the scraped data
                display_table(data.get("Organization details", {}), "Organization Details")
                display_table(data.get("File Status", {}), "File Status")
                display_table(data.get("Additional Tables", []), "Additional Tables")
                display_table(data.get("Directors and Secretaries", []), "Directors and Secretaries")
                display_table(data.get("HE32 Archive", []), "HE32 Archive")
                display_table(data.get("Registered Office", {}), "Registered Office")
                display_table(data.get("Preview File Type", []), "Preview File Type")
                display_table(data.get("Charges and Mortgages", []), "Charges and Mortgages")
                display_table(data.get("Translations", []), "Translations")
        else:
            st.warning("Please select a country and enter the company name.")

if __name__ == "__main__":
    main()
