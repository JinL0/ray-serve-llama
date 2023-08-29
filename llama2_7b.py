# from transformers import AutoTokenizer
model_name = "michaelfeil/ct2fast-Llama-2-7b-hf"

from hf_hub_ctranslate2 import GeneratorCT2fromHfHub
import requests
from starlette.requests import Request
from typing import Dict

from ray import serve

@serve.deployment(route_prefix="/serve/llama7b")
class Llama7BDeployment:
    def __init__(self):
        self.model = GeneratorCT2fromHfHub(
                        model_name_or_path=model_name,
                        device="cpu",
                        compute_type="int8",
                        )

    async def __call__(self, request: Request) -> Dict:
        # Extracting the message from the request's JSON body
        json_data = await request.json()
        message = json_data.get("message", "")

        outputs = self.model.generate(
                text=[message],
                max_length=128,
                include_prompt_in_result=False
            )
        
        # I noticed you returned {"result": self._msg} which would cause an error since self._msg is not defined.
        # Assuming you want to return the generated outputs:
        return {"result": outputs}

app = Llama7BDeployment.bind()

# 2: Deploy the application locally.
serve.run(app)

import requests

# Define the URL for the endpoint
url = "http://localhost:8000/serve/llama7b"

# Define the payload
data = {
    "message": "Your input text here"
}

# Send a POST request
response = requests.post(url, json=data)

# Print the response
print(response.json())

