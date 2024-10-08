# -*- coding: utf-8 -*-
"""App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZA8vDmFTJlboZga2A6Yctb8eiOkw6AAZ
"""

#!pip install tensorflow

#!pip install gdown

#pip install --upgrade tensorflow

#!pip install --upgrade keras
#!pip install streamlit

import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import gdown
import os

# Direct download link of the model file from Google Drive
@st.cache_data  # Caching the model so it doesn't download every time the app reloads
url = 'https://drive.google.com/uc?id=1hQ_gEuno0tOtAIx3ReKhS1SnQ4OEdXqx'

# Path to save the downloaded model file
model_path = 'my_model.keras'

# Download the model if it does not exist
if not os.path.exists(model_path):
    with st.spinner('Downloading model...'):
        gdown.download(url, model_path, quiet=False)

# Load the species classification model
model = tf.keras.models.load_model(model_path)

# Define the species names
species_names = [
    "Mantled Howler",
    "Patas Monkey",
    "Bald Monkey",
    "Japanese Macaque",
    "Pygmy Marmoset",
    "White Headed Capuchin",
    "Silver Marmoset",
    "Common Squirrel Monkey",
    "Black Headed Night Monkey",
    "Nilgiri Langur"
]

# Define a function to preprocess the image for the model
def preprocess_image(image, target_size=(64, 64)):
    image = image.resize(target_size)
    image = image.convert("RGB")
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    return image

# Define a function to make species predictions
def predict_species(image):
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    return prediction

# Custom CSS for background and other elements
st.markdown("""
    <style>
    .main {
        background-color: blue;
    }
    .title {
        color: red;
        font-family: 'Arial';
        text-align: center;
    }
    .uploader {
        text-align: center;
    }
    .prediction {
        font-size: 20px;
        color: indigo;
        font-weight: bold;
        text-align: center;
    }
    .uploaded-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border: 5px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit interface with custom styles
st.markdown('<h1 class="title">Monkeys Species Classification Application</h1>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True, output_format='JPEG', channels='RGB')
    st.write("")
    st.markdown('<div class="prediction">Classifying...</div>', unsafe_allow_html=True)

    # Make species prediction
    prediction = predict_species(image)

    # Get the index of the highest probability and the confidence score
    predicted_index = np.argmax(prediction, axis=1)[0]
    confidence_score = np.max(prediction, axis=1)[0]

    # Set a confidence threshold
    confidence_threshold = 0.8  # You can adjust this value

    # Check if the confidence score exceeds the threshold
    if confidence_score > confidence_threshold:
        predicted_species = species_names[predicted_index]
        st.markdown(f'<div class="prediction">Prediction: {predicted_species} (Confidence: {confidence_score:.2f})</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="prediction">The uploaded image is not recognized confidently as a monkey species.</div>', unsafe_allow_html=True)
