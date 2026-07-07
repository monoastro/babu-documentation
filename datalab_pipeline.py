# # I have datalab api, i want to build a pipeline wrapper around it
# #i need to input image, pass it to api, get it json and print it 

api_key="zOs3hB4K3qAijnqgZXy18F5EaRAXq7HfYyKXfXGbpdw"
image_path="test_tesse.png"

import requests

# def datalab_pipeline(api_key,input_data):
#     url = "https://api.datalab.com/v1/analyze"
#     headers={
#         "Authorization": f"Bearer {api_key}"

#     }

#     files = {"file": open(input_data, "rb")}
#     response = requests.post(url, headers=headers, files=files)
#     return response.json()

# print(datalab_pipeline(api_key,image_path))


url = "https://www.datalab.to/api/v1/convert"
headers = {"X-API-Key":api_key}

with open("document.pdf", "rb") as f:
    response = requests.post(
        url,
        files={"file": ("document.pdf", f, "application/pdf")},
        data={
            "output_format": "markdown",
            "mode": "balanced",
        },
        headers=headers
    )

data = response.json()
check_url = data["request_check_url"]