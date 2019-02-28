import os
import json

json_file = "keys/keys.json"
# read the pipeline params
with open(json_file) as pipeline_file:
    pipeline_params = json.load(pipeline_file)

os.environ["INDICO_APP_KEY"] = None
os.environ["CLARIFAI_API_KEY"] = None
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/google.json"
