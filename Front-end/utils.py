import requests

def stream_response(url):
    with requests.get(url, stream=True) as response:
        for chunk in response.iter_content():
            if chunk:
                try:
                    yield chunk.decode("utf-8")
                except:
                    print(chunk)

def styling_wrapper(response_generator):
    response = ""
    for token in response_generator:
        response += token
        if response[-16:] == "Final Response: ":
            break
        yield f'<p class="thoughts">{token}</p>'
    
    for token in response_generator:
        yield token