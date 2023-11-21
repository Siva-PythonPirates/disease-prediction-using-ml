// Function to load additional form fields based on the selected disease type
function loadFormFields() {
    const diseaseType = document.getElementById('diseaseType').value;
    const additionalFieldsContainer = document.getElementById('additionalFields');

    // Clear previous fields
    additionalFieldsContainer.innerHTML = '';

    // Load fields dynamically based on disease type
    if (diseaseType === 'diabetes') {
        // Add fields specific to diabetes
        additionalFieldsContainer.innerHTML = `
        <label for="BloodSugarLevel">Fasting Blood Sugar Level (mg/dL):</label>
        <input type="number" id="BloodSugarLevel" name="bloodSugarLevel" required><br>

        <label for="InsulinLevel">Insulin Level (μU/mL):</label>
        <input type="number" id="InsulinLevel" name="insulinLevel" required><br>

        <label for="BMI">Body Mass Index (BMI):</label>
        <input type="number" id="BMI" name="BMI" required>

        `;
    } else if (diseaseType === 'cardiovascular') {
        // Add fields specific to cardiovascular
        additionalFieldsContainer.innerHTML = `
        <label for="bloodPressure">Blood Pressure (mmHg):</label>
        <input type="text" id="bloodPressure" name="bloodPressure" required><br>

        <label for="cholesterolLevel">Cholesterol Level (mg/dL):</label>
        <input type="number" id="cholesterolLevel" name="cholesterolLevel" required><br>

        <label for="heartRate">Resting Heart Rate (bpm):</label>
        <input type="number" id="heartRate" name="heartRate" required><br>
        `;
    }else if (diseaseType === 'pulmonary') {
        // Add fields specific to cardiovascular
        additionalFieldsContainer.innerHTML = `
        <label for="lungCapacity">Lung Capacity (L):</label>
        <input type="number" id="lungCapacity" name="lungCapacity" required><br>

        <label for="breathingRate">Breathing Rate (breaths per minute):</label>
        <input type="number" id="breathingRate" name="breathingRate" required>

        `;
    }else if (diseaseType === 'kidney') {
        // Add fields specific to cardiovascular
        additionalFieldsContainer.innerHTML = `
        <label for="creatinineLevel">Creatinine Level (mg/dL):</label>
        <input type="number" id="creatinineLevel" name="creatinineLevel" required><br>

        <label for="urineProtein">Urine Protein (g/day):</label>
        <input type="number" id="urineProtein" name="urineProtein" required>

        `;
    }
}

// Function to submit the form (you can adapt this function to send data to your backend)
// Function to submit the form (you can adapt this function to send data to your backend)
function submitForm() {
    const formData = new FormData(document.getElementById('diseaseForm'));

    // Add AJAX call to send data to the backend and get predictions
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data (update the DOM, show alerts, etc.)
        console.log('Prediction Result:', data);
        // Example: Update a result div with the prediction information
        document.getElementById('result').innerText = `Prediction Result: ${data.Prediction}`;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors (e.g., show an error message to the user)
        document.getElementById('result').innerText = 'Error occurred during prediction.';
    });
}
