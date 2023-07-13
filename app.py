import streamlit as st #pip install streamlit
import pandas as pd #pip install pandas openpyxl
import plotly.express as px #pip install plotly-express
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu


st.set_page_config(page_title="MarketIQ", page_icon=":tada:")

#user authentication
names = ["Osman Irfan","Nazeem Ahmed"]
usernames = ['osman','nahmed']

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":hashed_passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":hashed_passwords[1]
                }            
            }
        }

authenticator = stauth.Authenticate(credentials,
    "marketiq", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

if authentication_status == None:
    st.warning("Please enter username and password")

if authentication_status:
    st.sidebar.title(f"Welcome {name}")
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options = ["Profile","Previous Orders","Settings"],
            icons = ["person","book","gear"],
            menu_icon = "cast",
        )

    #header section
    st.title("Welcome to MarketIQ")
    st.subheader("Where you can predict prices for various products!")
    st.write("We are a service that shows you which products prices you would like to view today.")
    table_content = ['Product ID','Product Name','Suggested Prices','Days in stock','Expeted profit margin','Recommended bundle']

    df = pd.read_excel(
        io='laptop_price.xlsx',
        engine = 'openpyxl',
        usecols='A:O',
        nrows=100,
    )

    st.sidebar.header("Filter products here:")
    product = st.sidebar.multiselect(
        "Select the name of Laptop:",
        options=df["Product"].unique(),
    )

    cpu = st.sidebar.multiselect(
        "Select type of CPU:",
        options=df["Cpu"].unique(),
    )

    typename = st.sidebar.multiselect(
        "Select type of Laptop:",
        options=df["TypeName"].unique(),
    )

    ram = st.sidebar.multiselect(
        "Select how much RAM is required:",
        options=df["Ram"].unique(),
    )

    gpu = st.sidebar.multiselect(
        "Select type of GPU:",
        options=df["Gpu"].unique(),
    )

    memory = st.sidebar.multiselect(
        "Select how much Memory is required:",
        options=df["Memory"].unique(),
    )

    df_select = df.query(
        "Product == @product | Cpu == @cpu | TypeName == @typename | Ram == @ram | Gpu == @gpu | Memory == @memory"
    )

    if (st.sidebar.button("Show Products")):
        st.dataframe(df_select)
    else:
        st.dataframe(df)
    
    authenticator.logout("Logout","sidebar")

    # Load the dataset into a DataFrame
    df2 = pd.read_excel('Recommendation.xlsx')

    # Remove leading and trailing spaces from the column names
    df2.columns = df2.columns.str.strip()


    # Initialize an empty list to store the selected items
    selected_items = []

    for _ in range(3):
        # Sort the DataFrame by 'Days_on_Stock' column in descending order
        sorted_df2 = df2.sort_values(by='Days_on_Stock', ascending=False)
        
        # Iterate through the sorted DataFrame and select a unique item
        for _, row in sorted_df2.iterrows():
            # Check if the current item is already selected
            if row['Product'] not in selected_items:
                # Add the current item to the selected items list
                selected_items.append(row['Product'])
                
                # Remove the selected item from the DataFrame
                df2 = df2[df2['Product'] != row['Product']]
                
                break

    # Print the selected items
    st.subheader("Additionally, would you also like to view the recommended product bundle")
    if st.button("Generate bundle"):
        st.dataframe({
            'Items':selected_items
        })