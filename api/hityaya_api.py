######### Import Path into System Path ###########
import os
import os.path
import sys
from keras.models import load_model
import numpy as np
from openai import OpenAI
import cv2

path = os.path.abspath(os.path.join(os.getcwd(), "./."))
sys.path.append(path)

####### Importing  Flask Component and required python lib ##################

from flask import request, jsonify, Blueprint, Response
from flask_api import status
import logging
from modules.diseases import chest_xray
import cv2
import json

######## Importing Supporting Lib #################

import APP_Constants as AC

####### Importing responses from Disease Modules #########
from modules.helper.support import get_disease_response

from dotenv import load_dotenv
from modules.helper.verification import require_verified_number

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

######## Creating Blueprint for all APIs #########

disease_Blueprint = Blueprint('disease_Blueprint', __name__)

######### Function for return disease assesment #######

UPLOAD_FOLDER = 'static/upload'
model_file = 'resources/models/skin_cancer.h5'


@disease_Blueprint.route('/disease/chest_xray', methods=['GET', 'POST'])
@require_verified_number
def chest_xrays():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        filename = f.filename

        # save our image in upload folder
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(file_path)  # save image into upload folder
        # get predictions

        # import pdb
        # pdb.set_trace()
        host = request.headers.get('HOST')

        # Make prediction
        pred_image, predictions = chest_xray.chest_xray(source=file_path)
        pred_filename = 'prediction_image.jpg'
        cv2.imwrite(f'./static/predict/{pred_filename}', pred_image)

        print(predictions)

        report = []
        for i, obj in enumerate(predictions):
            imagex = obj['roi']  # grayscale image (array)
            x = obj['x']  # name
            y = obj['y']  # name
            w = obj['w']  # name
            h = obj['h']  # name
            class_name = obj['prediction_class']  # name
            prediction_score = obj['prediction_score']  # probability score

            # save grayscale and eigne in predict folder
            image = f'roi_{i}.jpg'
            cv2.imwrite(f'./static/predict/{image}', imagex)

            # save report
            report.append(["http://" + host + "/static/predict/" + image,
                           x,
                           y,
                           w,
                           h,
                           class_name,
                           prediction_score,
                           "http://" + host + "/static/predict/" + pred_filename])

        # Do some processing, get output_imgs
        return Response(json.dumps(report), mimetype='application/json')

    return None


@disease_Blueprint.route('/disease/skin_cancer', methods=['GET', 'POST'])
@require_verified_number
def skin_cancer():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        filename = f.filename

        # save our image in upload folder
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(file_path)  # save image into upload folder

        def load_image(img_path):
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            img_resize = cv2.resize(img, (64, 64))
            img_tensor = np.array(img_resize)
            image = np.expand_dims(img_tensor, axis=0)

            return image

        # load a single image
        new_image = load_image(file_path)
        # load model
        model = load_model(model_file)

        # check prediction
        pred = model.predict(new_image)

        skin_cancer_types = ['Melanoma', 'Vascular lesion', 'Melanocytic nevus', 'Actinic keratosis',
                             'Squamous cell carcinoma', 'Benign keratosis', 'Basal cell carcinoma', 'Dermatofibroma']

        pred = list(pred)

        pred_index = pred.index(max(pred))

        return Response(json.dumps(skin_cancer_types[pred_index]), mimetype='application/json')

    return None


@disease_Blueprint.route('/disease/diet_plans', methods=['POST'])
@require_verified_number
def diet_plans():
    input_payload = request.get_json(cache=False)
    logging.info("Request for diet_plan - %s", input_payload['parameters'])

    weight = str(input_payload['parameters']['weight'])
    age = str(input_payload['parameters']['age'])
    condition = str(input_payload['parameters']['condition'])

    try:
        prompt = """Consider yourself a diet planner. Create a complete day wise 7 days diet plan for a week of a person who is """ + str(
            age) + """ years of age and weight is """ + str(weight) + """ Kg having a medical condition of """ + str(
            condition) + """ Include the weekday number with the weekday name as 1 Sunday Use bootstrap frontend 
            framework classes for the table Do not write the total HTML document but create only the HTML table as a 
            chart and the HTML code should be in a minimized manner Do not include any new line  The table must contain 
            the columns Day Breakfast Snack Lunch Evening Snack and Dinner It must have Sunday Monday Tuesday Wednesday 
            Thursday Friday and Saturday Do not ignore any of the days List multiple food recommendation in using ul li 
            tags in HTML Add className=table Use single quotes  Do not explain what you are doing or inference Only give 
            the response Write it in a short so that it does not exceeds the text limit"""

        client = OpenAI(
            # This is the default and can be omitted
            api_key=OPENAI_API_KEY,
        )

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=OPENAI_MODEL,
        )

        formatted_text = response.choices[0].message.content

        return jsonify(formatted_text), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@disease_Blueprint.route('/disease', methods=['POST'])
@require_verified_number
def disease():
    """disease API 

    Returns:
        [JSON]: [disease Model result JSON]
    """
    try:
        inputpayload = request.get_json(cache=False)
        logging.info("Request came for Disease - %s", inputpayload['disease'])
        result = get_disease_response(disease=inputpayload['disease'], diseaseparameter=inputpayload['parameters'])
        logging.info("Prediction for Disease - %s", result)
        return jsonify(result), status.HTTP_200_OK
    except Exception as err:
        return jsonify(f"Module - Error - {err}"), status.HTTP_400_BAD_REQUEST
