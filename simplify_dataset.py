"""
Feature Selection Script - Keep only top 20-30 symptoms
Reduces dataset complexity while maintaining model accuracy
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import os

# Load full datasets
print("Loading full datasets...")
train_data = pd.read_csv('data/Training.csv')
test_data = pd.read_csv('data/Testing.csv')

# Remove unnamed columns
train_data = train_data.loc[:, ~train_data.columns.str.contains('^Unnamed')]
test_data = test_data.loc[:, ~test_data.columns.str.contains('^Unnamed')]

print(f"Original features: {train_data.shape[1] - 1} (excluding target)")

# Separate features and target
X_train = train_data.drop('prognosis', axis=1)
y_train = train_data['prognosis']

X_test = test_data.drop('prognosis', axis=1)
y_test = test_data['prognosis']

# Train quick model to get feature importance
print("\nTraining model to compute feature importance...")
model = DecisionTreeClassifier(max_depth=25, min_samples_split=10, 
                                min_samples_leaf=5, random_state=42)
model.fit(X_train, y_train)

# Get feature importance
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 25 Most Important Features:")
print("="*60)
top_features = feature_importance.head(25)
for idx, row in top_features.iterrows():
    print(f"{row['feature']:40} | Importance: {row['importance']:.6f}")

# Select top 25 features
selected_features = feature_importance.head(25)['feature'].tolist()

# Create simplified datasets with only selected features + target
train_simplified = train_data[selected_features + ['prognosis']].copy()
test_simplified = test_data[selected_features + ['prognosis']].copy()

# Backup original files
print("\n" + "="*60)
print("Creating backups of original files...")
os.makedirs('data/backup', exist_ok=True)
train_data.to_csv('data/backup/Training_FULL.csv', index=False)
test_data.to_csv('data/backup/Testing_FULL.csv', index=False)
print("✓ Backup saved to data/backup/")

# Save simplified datasets
print("\n" + "="*60)
print("Saving simplified datasets...")
train_simplified.to_csv('data/Training.csv', index=False)
test_simplified.to_csv('data/Testing.csv', index=False)
print("✓ Simplified Training.csv saved")
print("✓ Simplified Testing.csv saved")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Original features: 132")
print(f"Reduced to: {len(selected_features)} features")
print(f"Reduction: {(1 - len(selected_features)/132)*100:.1f}%")
print(f"\nTraining samples: {train_simplified.shape[0]}")
print(f"Testing samples: {test_simplified.shape[0]}")
print(f"Diseases: {train_simplified['prognosis'].nunique()}")
print("\n✓ Dataset simplified successfully!")
print("✓ You can now run: python train.py")
print("\n" + "="*60)
