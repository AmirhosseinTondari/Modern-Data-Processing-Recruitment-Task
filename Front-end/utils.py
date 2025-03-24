import requests
import json

def stream_cot(url):
    with requests.get(url, stream=True) as response:
        for chunk in response.iter_content(decode_unicode=True):
            if chunk:
                try:
                    yield chunk
                except:
                    print(chunk)

def stream_cotsc(url):
    with requests.get(url, stream=True) as response:
        buffer = ""
        for chunk in response.iter_content(decode_unicode=True):
            if chunk:
                buffer += chunk
                if buffer[-1] == "\n":
                    data, buffer = buffer.split('\n', 1)
                    yield json.loads(data)
