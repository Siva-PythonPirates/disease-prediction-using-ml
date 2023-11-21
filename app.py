from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained models
models_dir = 'models'

# Load the trained diabetes model
diabetes_model = joblib.load(f'{models_dir}/diabetes_model.joblib')

# Load the trained cardiovascular model
cardiovascular_model = joblib.load(f'{models_dir}/cardiovascular_model.joblib')

# Load the trained pulmonary model
pulmonary_model = joblib.load(f'{models_dir}/pulmonary_model.joblib')

# Load the trained kidney model
kidney_model = joblib.load(f'{models_dir}/kidney_model.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    form_data = request.form.to_dict()

    # Example: Extracting relevant features from the form data (modify according to your form structure)
    name = form_data['name']
    age = int(form_data['age'])
    gender = form_data['gender']
    height = float(form_data['height'])
    weight = float(form_data['weight'])
    disease_type = form_data['diseaseType']

    # Preprocess form data as needed for prediction
    # Example: Convert 'Gender' to numeric using label encoding
    gender_mapping = {'male': 1, 'female': 0}
    gender_numeric = gender_mapping.get(gender.lower(), 0)

    # Create a DataFrame for prediction
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender_numeric],
        'Height': [height],
        'Weight': [weight]
    })

    # Add disease-specific features based on the selected disease type
    if disease_type == 'diabetes':
        input_data['BMI'] = float(form_data.get('BMI', 0))
        input_data['BloodSugarLevel'] = float(form_data.get('bloodSugarLevel', 0))
        input_data['InsulinLevel'] = float(form_data.get('insulinLevel', 0))
    elif disease_type == 'cardiovascular':
        input_data['SystolicPressure'] = float(form_data.get('systolicPressure', 0))
        input_data['DiastolicPressure'] = float(form_data.get('diastolicPressure', 0))
        
        input_data['CholesterolLevel'] = float(form_data.get('cholesterolLevel', 0))
        input_data['HeartRate'] = float(form_data.get('heartRate', 0))
    elif disease_type == 'pulmonary':
        input_data['LungCapacity'] = float(form_data.get('lungCapacity', 0))
        input_data['BreathingRate'] = float(form_data.get('breathingRate', 0))
    elif disease_type == 'kidney':
        input_data['CreatinineLevel'] = float(form_data.get('creatinineLevel', 0))
        input_data['UrineProtein'] = float(form_data.get('urineProtein', 0))
    else:
        return jsonify({"error": "Invalid disease type"})

    # Make predictions based on the selected disease type
    if disease_type == 'diabetes':
        prediction = diabetes_model.predict(input_data)[0]
    elif disease_type == 'cardiovascular':
        prediction = cardiovascular_model.predict(input_data)[0]
    elif disease_type == 'pulmonary':
        prediction = pulmonary_model.predict(input_data)[0]
    elif disease_type == 'kidney':
        prediction = kidney_model.predict(input_data)[0]
    else:
        return jsonify({"error": "Invalid disease type"})

    # Example: Return the predicted type of disease
    prediction_result = {
        'Name': name,
        'Age': age,
        'Gender': gender,
        'Height': height,
        'Weight': weight,
        'DiseaseType': disease_type,
        'Prediction': prediction
    }

    print(prediction_result)

    return jsonify(prediction_result)

if __name__ == '__main__':
    app.run(debug=True)
