from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained Logistic Regression model and scaler
try:
    model = joblib.load("models/logreg_best.pkl")
    scaler = joblib.load("models/scaled.pkl")
except FileNotFoundError:
    print("Error: 'logreg_best.pkl' or 'scaled.pkl' not found.")
    exit()

@app.route('/')
def home():
    return render_template('index.html')  # Optional UI

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        expected_features = [
            'gender', 'age', 'customer_type', 'type_of_travel', 'class',
            'flight_distance', 'departure_delay', 'arrival_delay',
            'ease_of_online_booking', 'check_in_service', 'online_boarding', 'gate_location',
            'on_board_service', 'seat_comfort', 'leg_room_service', 'cleanliness',
            'food_and_drink', 'in_flight_service', 'in_flight_wifi_service',
            'in_flight_entertainment', 'baggage_handling'
        ]

        if not all(feature in data for feature in expected_features):
            return jsonify({'error': 'Missing one or more required features'}), 400

        features = [data[feature] for feature in expected_features]
        input_features = np.array(features).reshape(1, -1)
        scaled_input = scaler.transform(input_features)

        prediction = model.predict(scaled_input)[0]
        output = {'satisfaction': 'Satisfied' if prediction == 1 else 'Neutral or Dissatisfied'}
        return jsonify(output)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
