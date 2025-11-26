# import os
# from openai import OpenAI
# from google import genai

# try:
#     openai_key = os.environ['OPENAI_API_KEY']
#     gemini_key = os.environ['GEMINI_API_KEY']
#     print("API Keys successfully loaded from environment variables.")
# except KeyError as e:
#     print(f"ERROR: Environment variable {e} not set. Please set it using 'export' or 'setx'.")
#     exit()

# try:
#     openai_client = OpenAI()
#     response = openai_client.chat.completions.create(
#         model="gpt-4.1",
#         messages=[{"role": "user", "content": "Say 'ready'"}],
#         max_tokens=5
#     )
#     print(f"GPT-4 Test Success! Model responded: {response.choices[0].message.content.strip()[:50]}...")
# except Exception as e:
#     print(f"GPT-4 Test FAILED: {e}")

# try:
#     gemini_client = genai.Client()
#     response = gemini_client.models.generate_content(
#         model="gemini-2.5-pro",
#         contents="Say 'ready'"
#     )
#     print(f"Gemini Pro Test Success! Model responded: {response.text.strip()[:50]}...")
# except Exception as e:
#     print(f"Gemini Pro Test FAILED: {e}")