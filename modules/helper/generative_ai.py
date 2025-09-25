import os
import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="gcds-oht33423u9-2023", location="us-central1")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"


def diet_plans(diet_parameters):
    model = TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }

    weight = str(diet_parameters["weight"])
    age = str(diet_parameters["age"])
    condition = diet_parameters["condition"]

    prompt_string = "Give me precise and concise health, diet, and exercise tips based on weight of " + weight + "kg, age " + age + " and having " + condition

    response = model.predict(
        prompt_string,
        **parameters
    )

    return response
