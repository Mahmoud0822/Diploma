from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the model and column names
model = joblib.load('hotel_booking_model.pkl')
model_columns = joblib.load('model_columns.pkl')

def prepare_input(input_data):
    """
    Prepare input data for prediction by ensuring it has the correct format
    and all necessary columns.
    """
    # Convert date of reservation to timestamp if it's in string format
    if 'date of reservation' in input_data and isinstance(input_data['date of reservation'], str):
        input_data['date of reservation'] = pd.to_datetime(input_data['date of reservation'], errors='coerce')
        input_data['date of reservation'] = input_data['date of reservation'].astype('int64') // 10**9
    
    # Create DataFrame with the expected columns
    input_df = pd.DataFrame([input_data])
    
    # Ensure all model columns exist (for one-hot encoded features)
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    # Keep only the columns used by the model, in the correct order
    input_df = input_df[model_columns]
    
    return input_df

@app.route('/')
def home():
    """
    Home route to render the HTML form.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Route to handle prediction requests.
    """
    try:
        # Get the data from the form
        data = request.form.to_dict()

        # Prepare input data
        input_df = prepare_input(data)

        # Make prediction
        prediction = model.predict(input_df)[0]

        # Get probability
        proba = model.predict_proba(input_df)[0]
        probability = proba[0] if prediction == 'Canceled' else proba[1]

        # Return the prediction
        return render_template('index.html', prediction_text=f'Booking Status: {prediction}', probability=f'Probability: {probability:.2f}')
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)