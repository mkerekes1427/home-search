import streamlit as st
import pandas as pd

df = pd.read_csv("data/housing.csv")
df.index = df["County"]

st.set_page_config(page_title="HomeFinder", layout="centered")

st.markdown("<h1 style='text-align:center;'>🏡 🔎</h1>", 
            unsafe_allow_html=True)

st.markdown("<h1 style='color:#A25772; text-align:center; padding:0;'>Home Finder</h1>", 
            unsafe_allow_html=True)

# Blank Space
st.title("")

state_options = sorted(df["State"].unique())
county_options = sorted(df["County"].unique())

states = st.multiselect("Filter States", options=state_options, key="states", placeholder="State")

if len(states) == 0:
    counties = st.multiselect("Filter Counties", options=county_options, key="counties", placeholder="County")
else:
    county_options = sorted(df.query("State in @states")["County"].unique())
    counties = st.multiselect("Filter Counties", options=county_options, key="counties", placeholder="County")

price = st.slider("Price Range ($)", min_value=df["Price"].min(), max_value=df["Price"].max(), value=(df["Price"].min(), df["Price"].max()), step=1000, key="price")
population = st.slider("Population Range", min_value=df["Population"].min(), max_value=df["Population"].max(), value=(df["Population"].min(), df["Population"].max()), step=1000, key="population")

search_btn = st.button("Search", type="primary", key="search")

# blank space
st.title("")

if search_btn:

    if len(states) == 0:
        states = df["State"].unique()
    if len(counties) == 0:
        counties = df["County"].unique()

    st.dataframe(df.query("State in @states and County in @counties " + 
                        "and Price >= @price[0] and Price <= @price[1] " +
                        "and Population >= @population[0] and Population <= @population[1]").iloc[:, 2:].sort_values(by="Price"),
                        use_container_width=True)

