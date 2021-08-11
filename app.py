import streamlit as st
from multiApp import MultiApp
from apps import home, shortestRoute, Analysis # import your app modules here
from PIL import Image

app = MultiApp()
st.image('salesman (2).png')

# Add all your application here
#app.add_app("Welcome", home.app)
app.add_app("Minimal Route Finder", shortestRoute.app)
app.add_app("Data Analysis", Analysis.app)
# The main app
app.run()