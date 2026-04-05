#!/usr/bin/env python
"""Run Streamlit app with streamlit command"""
import subprocess
import sys
import os

os.chdir(r'c:\Users\chand\OneDrive\Desktop\DEVOPS\disease-predictor')
subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
