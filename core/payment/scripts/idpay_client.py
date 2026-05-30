import requests
import json


class ZibalSandbox:
    _payment_request_url = "https://gateway.zibal.ir/v1/request"
    _payment_verify_url = "https://gateway.zibal.ir/v1/inquiry"
    _payment_page_url = "https://gateway.zibal.ir/start/"
    _callback_url = "http://redreseller.com/verify"

    def payment_request(self, amount=66666, description="پرداختی کاربر"):
        payload = {
            "merchant": "zibal",
            "amount": 16000,
            "callbackUrl": "http://yourapiurl.com/callback.php",
            "description": "Hello World!",
            "orderId": "ZBL-8000",
            "mobile": "09123456789",
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self._payment_request_url,
            headers=headers,
            data=json.dumps(payload),
        )

        return response.json()

    def payment_verify(self, trackId):
        payload = {
            "merchant": "zibal",
            "trackId": trackId,
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self._payment_verify_url, headers=headers, data=json.dumps(payload)
        )
        return response.json()

    def generate_payment_url(self, trackId):
        return self._payment_page_url + str(trackId)


if __name__ == "__main__":
    zarinpal = ZibalSandbox()
    response = zarinpal.payment_request()

    print(response)
    input("proceed to generating payment url?")
    print(zarinpal.generate_payment_url(response["trackId"]))

    input("check the payment?")

    response = zarinpal.payment_verify(response["trackId"])
    print(response)
