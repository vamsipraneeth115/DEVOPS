"""
Disease Prediction Streamlit Application
User Interface for disease prediction based on symptoms
"""

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Disease Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {background-color: #FF5252;}
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        margin: 20px 0;
    }
    .error-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style='text-align: center; color: #FF6B6B;'>
    🏥 Disease Prediction System
    </h1>
    <p style='text-align: center; font-size: 18px; color: #666;'>
    Intelligent symptom-based disease prediction using Machine Learning
    </p>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    st.write("**About this app:**")
    st.info("""
    This application uses a Decision Tree classifier 
    trained on medical symptom data to predict potential diseases.
    
    **Note:** This is for educational purposes and should not be 
    used as a substitute for professional medical advice.
    """)
    
    confidence_threshold = st.slider(
        "Prediction Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )

# Function to load model
@st.cache_resource
def load_model():
    """Load pre-trained model"""
    model_path = 'model.pkl'
    
    if not os.path.exists(model_path):
        return None
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model

# Function to get feature names
@st.cache_resource
def get_feature_names():
    """Get feature names from training data"""
    try:
        train_data = pd.read_csv('data/Training.csv')
        return train_data.drop('prognosis', axis=1).columns.tolist()
    except:
        return None

# Function to get disease classes
@st.cache_resource
def get_diseases():
    """Get disease classes from training data"""
    try:
        train_data = pd.read_csv('data/Training.csv')
        return sorted(train_data['prognosis'].unique().tolist())
    except:
        return None

# Load model and data info
model = load_model()
feature_names = get_feature_names()
diseases = get_diseases()

# Check if model is loaded
if model is None or feature_names is None:
    st.error("❌ Error: Model or training data not found!")
    st.markdown("""
    ### Setup Instructions:
    1. Ensure `model.pkl` exists in the current directory
    2. Ensure `data/Training.csv` exists
    3. Run the training script: `python train.py`
    """)
    st.stop()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🔍 Select Your Symptoms")
    st.write(f"**Total symptoms in dataset:** {len(feature_names)}")
    st.write("Check the symptoms you are experiencing:")

# Create symptom selection grid
st.markdown("---")

# Organize symptoms in columns for better UI
symptom_cols = st.columns(3)
selected_symptoms = {}

for idx, symptom in enumerate(feature_names):
    col_idx = idx % 3
    with symptom_cols[col_idx]:
        # Clean symptom name for display
        display_name = symptom.replace('_', ' ').title()
        selected_symptoms[symptom] = st.checkbox(display_name, key=symptom)

# Prediction button
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    predict_button = st.button("🔮 Predict Disease", use_container_width=True)

# Make prediction
if predict_button:
    # Count selected symptoms
    num_selected = sum(selected_symptoms.values())
    
    if num_selected == 0:
        st.markdown("""
        <div class='error-box'>
        <strong>⚠️ Warning:</strong> Please select at least one symptom before prediction.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Prepare feature vector
        X = np.zeros((1, len(feature_names)))
        
        for i, feature in enumerate(feature_names):
            if selected_symptoms[feature]:
                X[0, i] = 1
        
        # Make prediction
        prediction = model.predict(X)[0]
        prediction_proba = model.predict_proba(X)[0]
        confidence = np.max(prediction_proba)
        
        # Display results
        st.markdown("---")
        st.markdown("### 📋 Prediction Results")
        
        # Main prediction box
        st.markdown(f"""
        <div class='prediction-box'>
        <h2 style='color: #2E7D32;'>Predicted Disease</h2>
        <h1 style='color: #1565C0; font-size: 40px;'>{prediction}</h1>
        <p style='font-size: 18px;'><strong>Confidence:</strong> {confidence*100:.2f}%</p>
        <p style='font-size: 16px; color: #555;'>
        <strong>Selected Symptoms:</strong> {num_selected} out of {len(feature_names)}
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Top 3 predictions
        st.markdown("### 🎯 Top Predictions")
        
        top_3_indices = np.argsort(prediction_proba)[::-1][:3]
        top_3_diseases = [model.classes_[i] for i in top_3_indices]
        top_3_probs = [prediction_proba[i] for i in top_3_indices]
        
        result_df = pd.DataFrame({
            'Rank': ['1st', '2nd', '3rd'],
            'Disease': top_3_diseases,
            'Confidence': [f"{prob*100:.2f}%" for prob in top_3_probs]
        })
        
        st.dataframe(result_df, use_container_width=True, hide_index=True)
        
        # Additional info
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Statistics")
            st.metric("Total Symptoms Selected", num_selected)
            st.metric("Total Symptoms Available", len(feature_names))
        
        with col2:
            st.markdown("#### ℹ️ Information")
            st.write(f"**Total Diseases in Model:** {len(model.classes_)}")
            st.write(f"**Prediction Confidence:** {confidence*100:.2f}%")
        
        # Disclaimer
        st.markdown("---")
        st.markdown("""
        ⚠️ **DISCLAIMER:** 
        This application is for educational and informational purposes only. 
        It should NOT be used as a substitute for professional medical advice, 
        diagnosis, or treatment. Always consult with a qualified healthcare provider 
        for any medical concerns.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px; padding: 20px;'>
<p>Disease Prediction System v1.0 | Powered by Machine Learning | 
<strong>Deployment Date:</strong> 2024</p>
</div>
""", unsafe_allow_html=True)
