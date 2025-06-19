import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print('GEMINI_API_KEY not set in environment!')
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

try:
    models = genai.list_models()
    print('Available Gemini models:')
    for model in models:
        print(model)
except Exception as e:
    print(f'Error listing models: {e}') 