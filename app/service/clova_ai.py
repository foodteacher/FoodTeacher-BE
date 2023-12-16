import json
import requests

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8'
        }

        # Initialize result variable
        result = None

        try:
            # Use requests.post for making an HTTP POST request

            # Tunning model
            response = requests.post(
                f"{self._host}/testapp/v1/chat-completions/HCX-002",
                headers=headers, json=completion_request, stream=False
            )

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                result = response.json()
            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.RequestException as e:
            # Handle exceptions, log, or raise accordingly
            print(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
        return result


    def execute(self, completion_request):
        res = self._send_request(completion_request)

        if res['status']['code'] == '40103':
            # Check whether the token has expired and reissue the token.
            self._access_token = None
            return self.execute(completion_request)
        elif res['status']['code'] == '20000':
            return res['result']['message']['content']
        else:
            return 'Error'

def get_executor():
    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="NTA0MjU2MWZlZTcxNDJiYzQNPMHi/Vt8f/jUw+uD7CxxbMRCZVRUTctyUOXF4j66TwYR+0rbAlCPe0Gidp9I8H5FHyh/CZdR2nR3P9YLzdyPcQWUoaoBJNdfVdlLRfbApqW6nidfOULcNq8DgkXCDt2ZM3vduRz5ANdNiQE6dExfAsazK9E+7N3ujKbXes6CjsU82BBl6Xgzi+p7xEfKmZauaTerL9hyD591yntGgCg=",
        api_key_primary_val="3NxiPMlcuPlUytdAbAeMLg10eZwrwgQ4FNxYRTeh",
        request_id="1ba64a1d5d5a410b902cf0af1e2a8684"
    )
    return completion_executor