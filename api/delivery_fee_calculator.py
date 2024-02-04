from flask import Flask, request, jsonify
from models.request.DeliveryRequest import DeliveryRequest
from models.response.DeliveryResponse import DeliveryResponse
from calculations.fee_calculator import calculate_delivery_fee

app = Flask(__name__)


# Define the API endpoint
@app.route('/calculate_delivery_fee', methods=['POST'])
def calculate_delivery_fee_api():
    try:
        # Get the input data from the request
        data = request.json
        # Check if the input data is missing
        if not data:
            raise ValueError('Input data is missing')
        # Validate the input data
        is_input_data_valid, error_message = DeliveryRequest.validate_input_data(data)
        # Return an error response if the input data is invalid
        if not is_input_data_valid:
            error_response = {
                'status': 'error',
                'message': error_message
            }
            return jsonify(error_response), 400
        else:
            # Calculate the delivery fee
            delivery_request = DeliveryRequest.from_dict(data)
            delivery_fee = calculate_delivery_fee(delivery_request)
            response = DeliveryResponse(delivery_fee)
            return jsonify(response.to_dict())
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(error_response), 400
