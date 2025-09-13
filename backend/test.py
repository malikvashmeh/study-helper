import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
print([m.name for m in genai.list_models()])
