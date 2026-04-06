"""
Disease Prediction Model Training Script
Trains a Decision Tree classifier on medical symptoms dataset
"""

import os
import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")


class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.classes = None
        self.train_data = None
        self.test_data = None

    def load_data(self, train_path, test_path=None):
        """Load training and testing data."""
        print(f"Loading training data from {train_path}...")
        self.train_data = pd.read_csv(train_path)

        # Remove unnamed columns caused by trailing commas in CSV files.
        self.train_data = self.train_data.loc[
            :, ~self.train_data.columns.str.contains("^Unnamed")
        ]

        if test_path:
            print(f"Loading test data from {test_path}...")
            self.test_data = pd.read_csv(test_path)
            self.test_data = self.test_data.loc[
                :, ~self.test_data.columns.str.contains("^Unnamed")
            ]
        else:
            self.test_data = None

        print(f"Training data shape: {self.train_data.shape}")
        if self.test_data is not None:
            print(f"Test data shape: {self.test_data.shape}")

        return self.train_data, self.test_data

    def prepare_data(self, data):
        """Separate features and target."""
        x_data = data.drop("prognosis", axis=1)
        y_data = data["prognosis"]

        self.feature_names = x_data.columns.tolist()
        self.classes = y_data.unique().tolist()

        return x_data, y_data

    def train_model(self):
        """Train the decision tree model."""
        print("\n" + "=" * 50)
        print("TRAINING MODEL")
        print("=" * 50)

        x_train, y_train = self.prepare_data(self.train_data)

        self.model = DecisionTreeClassifier(
            max_depth=25,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            criterion="gini",
        )

        self.model.fit(x_train, y_train)

        y_pred_train = self.model.predict(x_train)
        train_accuracy = accuracy_score(y_train, y_pred_train)
        print(
            f"\n[OK] Training Accuracy: {train_accuracy:.4f} "
            f"({train_accuracy * 100:.2f}%)"
        )

        return train_accuracy

    def evaluate_model(self):
        """Evaluate model on test data."""
        if self.test_data is None:
            print("No test data available for evaluation")
            return None

        print("\n" + "=" * 50)
        print("EVALUATING MODEL")
        print("=" * 50)

        x_test, y_test = self.prepare_data(self.test_data)

        y_pred = self.model.predict(x_test)
        test_accuracy = accuracy_score(y_test, y_pred)

        print(
            f"\n[OK] Test Accuracy: {test_accuracy:.4f} "
            f"({test_accuracy * 100:.2f}%)"
        )
        print(f"\nNumber of diseases: {len(self.classes)}")
        print(f"Diseases: {', '.join(sorted(self.classes))}")

        print("\n" + "-" * 50)
        print("CLASSIFICATION REPORT")
        print("-" * 50)
        print(classification_report(y_test, y_pred))

        return test_accuracy

    def save_model(self, model_path="model.pkl"):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("Model has not been trained yet!")

        print(f"\n[OK] Saving model to {model_path}...")
        with open(model_path, "wb") as model_file:
            pickle.dump(self.model, model_file)

        print("[OK] Model saved successfully!")

    def predict(self, symptoms_dict):
        """Make a prediction for a given symptom set."""
        if self.model is None:
            raise ValueError("Model has not been trained yet!")

        feature_vector = np.zeros((1, len(self.feature_names)))

        for index, feature in enumerate(self.feature_names):
            if feature in symptoms_dict:
                feature_vector[0, index] = symptoms_dict[feature]

        return self.model.predict(feature_vector)[0]


def main():
    """Run the training pipeline."""
    print("\n")
    print("=" * 50)
    print("DISEASE PREDICTION SYSTEM")
    print("Training Pipeline")
    print("=" * 50)

    predictor = DiseasePredictor()

    train_path = "data/Training.csv"
    test_path = "data/Testing.csv"
    model_path = "model.pkl"

    if not os.path.exists(train_path):
        print(f"\n[ERROR] Training data not found at {train_path}")
        print("Please ensure Training.csv is in the 'data' directory")
        return

    predictor.load_data(train_path, test_path)
    predictor.train_model()
    test_accuracy = predictor.evaluate_model()
    predictor.save_model(model_path)

    print("\n" + "=" * 50)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print(f"Model saved as: {model_path}")
    print(f"Number of features: {len(predictor.feature_names)}")
    print(f"Number of diseases: {len(predictor.classes)}")

    if test_accuracy is not None:
        print(f"\nFinal Test Accuracy: {test_accuracy:.4f} ({test_accuracy * 100:.2f}%)")


if __name__ == "__main__":
    main()
