import os
import requests

from flask import Blueprint, jsonify, request
from flask_api import status

import APP_Constants as AC
from modules.helper.verification import verification_cache

network_blp = Blueprint(
    'network_blueprint', __name__, url_prefix=f"{AC.APP_ENDPOINT}network"
)


@network_blp.route('/verify', methods=['POST'])
def verify_number():
    """Verify a patient phone number using Open Gateway Number Verification API.

    Request JSON: { "phoneNumber": "+91xxxxxxxxxx" }
    """
    try:
        payload = request.get_json(cache=False) or {}
        phone_number = payload.get("phoneNumber")
        if not phone_number:
            return jsonify({"message": "phoneNumber is required"}), status.HTTP_400_BAD_REQUEST

        # Prefer environment variable for security; fallback to header value if provided
        rapidapi_key = os.getenv("RAPIDAPI_KEY") or request.headers.get("x-rapidapi-key")
        if not rapidapi_key:
            return jsonify({"message": "RAPIDAPI_KEY not configured"}), status.HTTP_400_BAD_REQUEST

        url = (
            "https://network-as-code.p-eu.rapidapi.com/passthrough/camara/"
            "v1/number-verification/number-verification/v0/verify"
        )
        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
            "x-rapidapi-key": rapidapi_key,
        }
        resp = requests.post(url, json={"phoneNumber": phone_number}, headers=headers, timeout=20)
        data = safe_json(resp)

        # Basic success heuristic: mark verified on HTTP 200-299
        if 200 <= resp.status_code < 300:
            verification_cache.mark_verified(phone_number)

        return jsonify({
            "status_code": resp.status_code,
            "data": data,
            "verified": verification_cache.is_verified(phone_number)
        }), status.HTTP_200_OK
    except requests.Timeout:
        return jsonify({"message": "Verification timed out"}), status.HTTP_504_GATEWAY_TIMEOUT
    except Exception as err:
        return jsonify({"message": f"Verification error - {err}"}), status.HTTP_400_BAD_REQUEST


def safe_json(resp: requests.Response):
    try:
        return resp.json()
    except Exception:
        return {"text": resp.text}


@network_blp.route('/device-status', methods=['GET'])
def device_status():
    # Placeholder for CAMARA Device Status API integration
    return jsonify({"message": "Device Status integration pending"}), status.HTTP_200_OK


@network_blp.route('/location', methods=['GET'])
def device_location():
    # Placeholder for CAMARA Location API integration
    return jsonify({"message": "Location integration pending"}), status.HTTP_200_OK


@network_blp.route('/qod', methods=['POST'])
def quality_on_demand():
    # Placeholder for CAMARA Quality on Demand API integration
    return jsonify({"message": "QoD integration pending"}), status.HTTP_200_OK


