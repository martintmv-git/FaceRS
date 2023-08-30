from PIL import Image
import numpy as np

import streamlit as st
import pickle
import yaml
import pandas as pd

cfg = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
PKL_PATH = cfg['PATH']["PKL_PATH"]
st.set_page_config(layout="wide")

# Load database
with open(PKL_PATH, 'rb') as file:
    database = pickle.load(file)

# Max image height
max_image_height = 100

# Loop through database and display records
for idx, person in database.items():
    row_container = st.container()
    
    with row_container:
        col1, col2, col3, col4 = st.columns([0.5, 0.5, 3, 3])
        
        with col1:
            st.write(idx)
            
        with col2:
            st.write(person['id'])
        
        with col3:
            st.write(person['name'])
            
        with col4:
            # Convert numpy array to PIL Image
            image = Image.fromarray(person['image'])
            
            # Calculate aspect ratio
            aspect_ratio = image.width / image.height
            
            # Calculate new dimensions based on max height
            new_height = min(max_image_height, image.height)
            new_width = int(new_height * aspect_ratio)
            
            # Resize the image while keeping aspect ratio
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            
            st.image(image, use_column_width=False, output_format='PNG')
