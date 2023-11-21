import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Create models directory if it doesn't exist
models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)

def train_model(data, target_column, model_name, features, model_params):
    print(f"Training {model_name} model...")

    # Remove non-numeric columns
    data = data.drop('Name', axis=1)

    # Label encode the 'Gender' column
    le = LabelEncoder()
    data['Gender'] = le.fit_transform(data['Gender'])

    # Define features (X) and target variable (y)
    X = data[features]
    y = data[target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the classifier
    clf = RandomForestClassifier(**model_params)

    # Train the model
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f'{model_name} Model Accuracy: {accuracy:.2f}')

    # Save the trained model to a file in the models directory
    model_filename = os.path.join(models_dir, f'{model_name.lower()}_model.joblib')
    joblib.dump(clf, model_filename)
    print(f'{model_name} Model Saved: {model_filename}\n')

def train_diabetes_model():
    diabetes_data = pd.read_csv('datasets/diabetes_dataset.csv')
    features = ['Age', 'Gender', 'Height', 'Weight', 'BMI', 'BloodSugarLevel', 'InsulinLevel']
    model_params = {'n_estimators': 100, 'random_state': 42}
    train_model(diabetes_data, 'DiabetesType', 'Diabetes', features, model_params)

def train_cardiovascular_model():
    cardiovascular_data = pd.read_csv('datasets/cardiovascular_dataset.csv')
    cardiovascular_data = cardiovascular_data.drop('Name', axis=1)
    le = LabelEncoder()
    cardiovascular_data['Gender'] = le.fit_transform(cardiovascular_data['Gender'])
    if 'BloodPressure' in cardiovascular_data.columns:
        cardiovascular_data[['SystolicPressure', 'DiastolicPressure']] = cardiovascular_data['BloodPressure'].str.split('/', expand=True)
        cardiovascular_data['SystolicPressure'] = pd.to_numeric(cardiovascular_data['SystolicPressure'])
        cardiovascular_data['DiastolicPressure'] = pd.to_numeric(cardiovascular_data['DiastolicPressure'])
        cardiovascular_data = cardiovascular_data.drop('BloodPressure', axis=1)
        features = ['Age', 'Gender', 'Height', 'Weight', 'SystolicPressure', 'DiastolicPressure', 'CholesterolLevel', 'HeartRate']
        y = cardiovascular_data['CardiovascularType']
        X_train, X_test, y_train, y_test = train_test_split(cardiovascular_data[features], y, test_size=0.2, random_state=42)
        clf = RandomForestClassifier(n_estimators=100, random_state=42)

        # Train the model
        clf.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = clf.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Cardiovascular Model Accuracy: {accuracy:.2f}')

        # Save the trained model to a file in the models directory
        model_filename = os.path.join(models_dir, 'cardiovascular_model.joblib')
        joblib.dump(clf, model_filename)
        print(f'Cardiovascular Model Saved: {model_filename}/n')
    else:
        print("Error: 'BloodPressure' column not found in the dataset.")

def train_pulmonary_model():
    pulmonary_data = pd.read_csv('datasets/pulmonary_dataset.csv')
    features = ['Age', 'Gender', 'Height', 'Weight', 'LungCapacity', 'BreathingRate']
    model_params = {'n_estimators': 100, 'random_state': 42}
    train_model(pulmonary_data, 'PulmonaryType', 'Pulmonary', features, model_params)

def train_kidney_model():
    kidney_data = pd.read_csv('datasets/kidney_dataset.csv')
    features = ['Age', 'Gender', 'Height', 'Weight', 'CreatinineLevel', 'UrineProtein']
    model_params = {'n_estimators': 100, 'random_state': 42}
    train_model(kidney_data, 'KidneyType', 'Kidney', features, model_params)

if __name__ == "__main__":
    train_diabetes_model()
    train_cardiovascular_model()
    train_pulmonary_model()
    train_kidney_model()
