import base64
import jsons
from text_to_speech.constants import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def calculate_sha256_string(input_string):
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_string.encode('utf-8'))
    return sha256.finalize().hex()


def base64_encode(input_dict):
    json_data = jsons.dumps(input_dict)
    data_bytes = json_data.encode('utf-8')
    return base64.b64encode(data_bytes).decode('utf-8')


def get_payload(request,MERCHANT_ID,MERCHANT_TRANSACTION_ID,credits_to_purchase):
    payload = {
                "merchantId": MERCHANT_ID,
                "merchantTransactionId": MERCHANT_TRANSACTION_ID,  # Replace with your unique ID
                "merchantUserId": request.user.id,  # Assuming you have a User model
                "amount": credits_to_purchase,
                "redirectUrl": "http://127.0.0.1:8000/purchase/callback/",  # Replace with your actual redirect URL
                "redirectMode": "POST",
                "callbackUrl": "http://127.0.0.1:8000/purchase/callback/",  # Replace with your actual callback URL
                "paymentInstrument": {
                    "type": "PAY_PAGE"
                },
                "mobileNumber": "9999999999",  # Replace with user's mobile number or make it dynamic
            }
    return payload
