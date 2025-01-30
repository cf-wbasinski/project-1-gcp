from flask import Flask, request, jsonify
from typing import Dict
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv(override=True)

print("PROJECT_ID: ", os.getenv('PROJECT_ID'))
print("ENDPOINT_ID: ", os.getenv('ENDPOINT_ID'))

app = Flask(__name__)

def predict_tabular_classification(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "europe-west4",
    api_endpoint: str = "europe-west4-aiplatform.googleapis.com",
):
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )

    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    # Extract predictions
    predictions = response.predictions
    prediction_dict = dict(predictions[0])

    # Print the prediction_dict to see its structure
    print("Prediction dict:", prediction_dict)

    return prediction_dict

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the request data
        data = request.get_json()

        # Extract the features
        instance_dict = {
            'culmen_length_mm': data.get('culmen_length_mm'),
            'culmen_depth_mm': data.get('culmen_depth_mm'),
            'flipper_length_mm': data.get('flipper_length_mm'),
            'body_mass_g': data.get('body_mass_g')
        }
        # Get project details from environment variables
        PROJECT_ID = os.getenv('PROJECT_ID')
        ENDPOINT_ID = os.getenv('ENDPOINT_ID')

        if not PROJECT_ID or not ENDPOINT_ID:
            raise ValueError("PROJECT_ID and ENDPOINT_ID must be set in environment variables")

        # Get prediction
        prediction_dict = predict_tabular_classification(
            project=PROJECT_ID,
            endpoint_id=ENDPOINT_ID,
            instance_dict=instance_dict
        )

        # Format the prediction response
        formatted_prediction = {
            'classes': list(prediction_dict['classes']),
            'scores': list(prediction_dict['scores'])
        }

        return jsonify({
            'status': 'success',
            'prediction': formatted_prediction
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
