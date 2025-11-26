import os
import time
import re
from openai import OpenAI
from google import genai

NUM_SAMPLES = 100
MODELS = {
    'GPT4': 'gpt-4.1',
    'GeminiPro': 'gemini-2.5-pro'
}
LANGUAGES = ['Java', 'Python']
# LANGUAGES = ['Java']
OUTPUT_DIR = 'generated_code'

PROMPTS = {
    'Python': (
        "Generate a complete, self-contained Python class named SplayTree that implements a dictionary-like set for integers. "
        "It must include the methods insert(key), delete(key), and search(key). The search method must perform the splaying operation "
        "on the accessed node (or its parent if the node is not found) to move it to the root. "
        "Only output the final, complete Python code within a single markdown code block."
    ),
    'Java': (
        "Generate a complete, self-contained Java class named SplayTree that implements an integer set. "
        "It must include the public methods insert(int key), delete(int key), and search(int key) which returns the key or null if not found. "
        "The search method must perform the splaying operation on the accessed node to move it to the root. "
        "Only output the final, complete Java code within a single markdown code block."
    )
}

def ensure_output_directory(model_name, lang):
    path = os.path.join(OUTPUT_DIR, model_name, lang)
    os.makedirs(path, exist_ok=True)
    return path

def extract_code_block(response_text, lang):
    pattern = re.compile(rf"```{lang.lower()}.*?\n(.*?)\n```", re.DOTALL)
    match = pattern.search(response_text)
    
    if match:
        return match.group(1).strip()
    else:
        pattern_generic = re.compile(r"```.*?\n(.*?)\n```", re.DOTALL)
        match_generic = pattern_generic.search(response_text)
        if match_generic:
            return match_generic.group(1).strip()
        
        return response_text.strip()


def generate_code(model_api_name, lang, prompt):
    MAX_RETRIES = 3
    INITIAL_DELAY = 5
    
    for attempt in range(MAX_RETRIES):
        try:
            if 'gpt' in model_api_name:
                client = OpenAI()
                response = client.chat.completions.create(
                    model=model_api_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    timeout=60
                )
                return response.choices[0].message.content
            
            elif 'gemini' in model_api_name:
                client = genai.Client()
                response = client.models.generate_content(
                    model=model_api_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.7,
                    ),
                )
                return response.text
                
        except Exception as e:
            error_message = str(e)
            
            if "503 UNAVAILABLE" in error_message or "overloaded" in error_message:
                if attempt < MAX_RETRIES - 1:
                    wait_time = INITIAL_DELAY * (2 ** attempt)
                    print(f"  [Retry {attempt + 1}/{MAX_RETRIES}]: Model overloaded (503). Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return f"API_ERROR: {error_message}"
            else:
                return f"API_ERROR: {error_message}"
    
    return f"API_ERROR: Failed after {MAX_RETRIES} attempts."

def run_generation_pipeline():
    print("Starting LLM Code Generation Pipeline...")
    
    for model_name, model_api_name in MODELS.items():
        for lang in LANGUAGES:
            
            output_path = ensure_output_directory(model_name, lang)
            prompt = PROMPTS[lang]
            
            print(f"\n--- Generating {NUM_SAMPLES} samples for {model_name} ({lang}) ---")

            for i in range(1, NUM_SAMPLES + 1):
                file_ext = 'py' if lang == 'Python' else 'java'
                filename = os.path.join(output_path, f'{i:03d}_SplayTree.{file_ext}')

                if os.path.exists(filename):
                    print(f"  Skipping {i:03d} (Exists)")
                    continue

                response_text = generate_code(model_api_name, lang, prompt)

                if response_text.startswith("API_ERROR"):
                    code_content = response_text
                    print(f"  Sample {i:03d}: API Error. Saving error message.")
                else:
                    code_content = extract_code_block(response_text, lang)
                    print(f"  Sample {i:03d}: Generated ({len(code_content)} chars)")

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code_content)
                
                time.sleep(2) 

    print("\nGeneration pipeline complete. Total 400 files attempted.")


if __name__ == '__main__':
    run_generation_pipeline()

