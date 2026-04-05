"""
Disease Prediction Model Training Script
Trains a Decision Tree classifier on medical symptoms dataset
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings

warnings.filterwarnings('ignore')

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.classes = None
        
    def load_data(self, train_path, test_path=None):
        """Load training and testing data"""
        print(f"Loading training data from {train_path}...")
        self.train_data = pd.read_csv(train_path)
        
        # Remove unnamed columns (caused by trailing commas in CSV)
        self.train_data = self.train_data.loc[:, ~self.train_data.columns.str.contains('^Unnamed')]
        
        if test_path:
            print(f"Loading test data from {test_path}...")
            self.test_data = pd.read_csv(test_path)
            # Remove unnamed columns
            self.test_data = self.test_data.loc[:, ~self.test_data.columns.str.contains('^Unnamed')]
        else:
            self.test_data = None
            
        print(f"Training data shape: {self.train_data.shape}")
        if self.test_data is not None:
            print(f"Test data shape: {self.test_data.shape}")
        
        return self.train_data, self.test_data
    
    def prepare_data(self, data):
        """Separate features and target"""
        X = data.drop('prognosis', axis=1)
        y = data['prognosis']
        
        self.feature_names = X.columns.tolist()
        self.classes = y.unique().tolist()
        
        return X, y
    
    def train_model(self):
        """Train Decision Tree model"""
        print("\n" + "="*50)
        print("TRAINING MODEL")
        print("="*50)
        
        # Prepare data
        X_train, y_train = self.prepare_data(self.train_data)
        
        # Create and train Decision Tree
        self.model = DecisionTreeClassifier(
            max_depth=25,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            criterion='gini'
        )
        
        self.model.fit(X_train, y_train)
        
        # Training accuracy
        y_pred_train = self.model.predict(X_train)
        train_accuracy = accuracy_score(y_train, y_pred_train)
        print(f"\n✓ Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
        
        return train_accuracy
    
    def evaluate_model(self):
        """Evaluate model on test data"""
        if self.test_data is None:
            print("No test data available for evaluation")
            return None
            
        print("\n" + "="*50)
        print("EVALUATING MODEL")
        print("="*50)
        
        X_test, y_test = self.prepare_data(self.test_data)
        
        y_pred = self.model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✓ Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        print(f"\nNumber of diseases: {len(self.classes)}")
        print(f"Diseases: {', '.join(sorted(self.classes))}")
        
        print("\n" + "-"*50)
        print("CLASSIFICATION REPORT")
        print("-"*50)
        print(classification_report(y_test, y_pred))
        
        return test_accuracy
    
    def save_model(self, model_path='model.pkl'):
        """Save trained model """
        if self.model is None:
            raise ValueError("Model has not been trained yet!")
        
        print(f"\n✓ Saving model to {model_path}...")
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"✓ Model saved successfully!")
        
    def predict(self, symptoms_dict):
        """Make prediction for given symptoms"""
        if self.model is None:
            raise ValueError("Model has not been trained yet!")
        
        # Create feature vector
        X = np.zeros((1, len(self.feature_names)))
        
        for i, feature in enumerate(self.feature_names):
            if feature in symptoms_dict:
                X[0, i] = symptoms_dict[feature]
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        
        return prediction

def main():
    """Main training pipeline"""
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + " "*10 + "DISEASE PREDICTION SYSTEM" + " "*13 + "║")
    print("║" + " "*15 + "Training Pipeline" + " "*17 + "║")
    print("╚" + "="*48 + "╝")
    
    # Initialize predictor
    predictor = DiseasePredictor()
    
    # Define paths
    train_path = 'data/Training.csv'
    test_path = 'data/Testing.csv'
    model_path = 'model.pkl'
    
    # Check if data exists
    if not os.path.exists(train_path):
        print(f"\n✗ Error: Training data not found at {train_path}")
        print("Please ensure Training.csv is in the 'data' directory")
        return
    
    # Load data
    predictor.load_data(train_path, test_path)
    
    # Train model
    train_acc = predictor.train_model()
    
    # Evaluate model
    test_acc = predictor.evaluate_model()
    
    # Save model
    predictor.save_model(model_path)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print(f"Model saved as: {model_path}")
    print(f"Number of features: {len(predictor.feature_names)}")
    print(f"Number of diseases: {len(predictor.classes)}")
    
    if test_acc:
        print(f"\nFinal Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")

if __name__ == "__main__":
    main()
