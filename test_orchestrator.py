import os
import subprocess
import shutil
import time
import pandas as pd
import re
import sys
import pytest

MODELS = ['GPT4', 'GeminiPro']
LANGUAGES = ['Java', 'Python']
# LANGUAGES = ['Python']
OUTPUT_DIR = 'generated_code'
RESULT_CSV = 'splay_tree_benchmarking_results.csv'
NUM_SAMPLES = 100

EASY_JAVA_BASELINE_MS = 4.5
EASY_PYTHON_BASELINE_MS = 43.0
MEDIUM_JAVA_BASELINE_MS = 10.0
MEDIUM_PYTHON_BASELINE_MS = 105.0
HARD_JAVA_BASELINE_MS = 33.0
HARD_PYTHON_BASELINE_MS = 430.0
EFFICIENCY_THRESHOLD_FACTOR = 2

JAVAC_PATH = r"C:\Program Files\Java\jdk-21\bin\javac"
JAVA_PATH = r"C:\Program Files\Java\jdk-21\bin\java" 

TEST_SUITE_MAP = {
    'easy': {
        'java_driver': 'easy_TestDriver.java',
        'python_harness': 'easy_test_harness.py',
    },
    'medium': {
        'java_driver': 'medium_TestDriver.java',
        'python_harness': 'medium_test_harness.py',
    },
    'hard': {
        'java_driver': 'hard_TestDriver.java',
        'python_harness': 'hard_test_harness.py',
    },
}


# TEST_SUITES_TO_RUN = ['easy', 'medium', 'hard']
# TEST_SUITES_TO_RUN = ['easy']
# TEST_SUITES_TO_RUN = ['medium']
TEST_SUITES_TO_RUN = ['hard']

# JAVA SETUP
JAVA_HELPER_FILES = ['SplayNode.java', 'reference_SplayTree.java']
JAVA_REFERENCE_CLASS = 'reference_SplayTree'

N_KEYS = 20000
M_SEARCHES = 200000
MIN_KEY = 1


def run_java_tests(filepath, model_name, sample_id, suite_config):
    current_dir = os.path.dirname(filepath)
    original_filename = os.path.basename(filepath)
    
    COMPILATION_FILENAME = 'SplayTree.java' 
    temp_filepath = os.path.join(current_dir, COMPILATION_FILENAME)
    
    java_driver_file = suite_config['java_driver']

    shutil.copy(filepath, temp_filepath) 
    
    try:
        files_to_copy = ['SplayNode.java', java_driver_file, 'reference_SplayTree.java']
        for f in files_to_copy:
            shutil.copy(os.path.join(os.getcwd(), f), current_dir)
        
        compile_command = [
            JAVAC_PATH,
            '-source', '21', '-target', '21',
            os.path.join(current_dir, COMPILATION_FILENAME), 
            os.path.join(current_dir, 'SplayNode.java'), 
            os.path.join(current_dir, java_driver_file),
            os.path.join(current_dir, 'reference_SplayTree.java')
        ]
        
        compilation = subprocess.run(compile_command, capture_output=True, text=True, timeout=15)
        
        if compilation.returncode != 0:
            return 'N_Syntax', 0.0
        
    except subprocess.TimeoutExpired:
        return 'N_Syntax', 0.0
    except FileNotFoundError:
        return 'N_Syntax', 0.0

    try:
        runtime_command = [JAVA_PATH, java_driver_file.replace('.java', '')] 
        
        execution = subprocess.run(runtime_command, cwd=current_dir, capture_output=True, text=True, timeout=30) 
        
        output = execution.stdout.strip()
        
        time_ms = 0.0
        time_match = re.search(r"Execution time in ms: ([\d\.]+)", output)
        if time_match:
            time_ms = float(time_match.group(1))

        if execution.returncode != 0:
            return 'N_Safety', 0.0 

        if "TEST_PASSED" in output:
            if time_ms == 0.0:
                return 'N_Syntax', 0.0
                
            if time_ms > EFFICIENCY_THRESHOLD_FACTOR * HARD_JAVA_BASELINE_MS:
                return 'N_Efficiency', time_ms
            return 'N_Correct', time_ms
        
        if "TEST_FAILED" in output:
            if "Safety Error" in output or "Null Pointer" in output:
                return 'N_Safety', 0.0
            return 'N_Logical', 0.0
            
    except subprocess.TimeoutExpired:
        return 'N_Efficiency', 0.0
    except Exception:
        return 'N_Syntax', 0.0
    finally:
        if os.path.exists(temp_filepath):
             os.remove(temp_filepath) 

        files_to_clean = JAVA_HELPER_FILES + [java_driver_file]
        for item in os.listdir(current_dir):
            if item.endswith('.class'):
                os.remove(os.path.join(current_dir, item))
            
        for f in files_to_clean:
            copied_file_path = os.path.join(current_dir, f)
            if os.path.exists(copied_file_path):
                os.remove(copied_file_path)


def run_python_tests(filepath, model_name, sample_id, suite_config):
    current_dir = os.path.dirname(filepath)
    python_harness_file = suite_config['python_harness']
    
    pytest_command = ['pytest', '-vv', '--tb=no', 
                      f'--model-path={filepath}', 
                      os.path.join(os.getcwd(), python_harness_file)]
    
    try:
        test_result = subprocess.run(pytest_command, capture_output=True, text=True, timeout=10)
        
        output_stderr = test_result.stderr
        full_output = test_result.stdout + output_stderr
        
        time_ms = 0.0
        time_match = re.search(r'\{"time_ms":\s*([\d\.]+)', full_output)
        
        if time_match:
            try:
                time_ms = float(time_match.group(1))
            except ValueError:
                time_ms = 0.0
        if test_result.returncode != 0:
            
            if "Algorithmic Efficiency Failure" in full_output:
                return 'N_Efficiency', time_ms
            if "AssertionError" in full_output:
                return 'N_Logical', 0.0
            if "AttributeError" in full_output or "TypeError" in full_output:
                return 'N_Safety', 0.0
            
            return 'N_Syntax', 0.0
            
        if time_ms > 0.0:
            return 'N_Correct', time_ms
        else:
            return 'N_Syntax', 0.0
        
    except subprocess.TimeoutExpired:
        return 'N_Safety', 0.0
    except Exception:
        return 'N_Syntax', 0.0

def orchestrate_testing():
    all_results = []
    
    for suite_name in TEST_SUITES_TO_RUN:
        suite_config = TEST_SUITE_MAP[suite_name]
        
        for model in MODELS:
            for lang in LANGUAGES:
                base_path = os.path.join(OUTPUT_DIR, model, lang)
                if not os.path.exists(base_path):
                    print(f"Directory not found: {base_path}. Skipping.")
                    continue

                for i in range(1, NUM_SAMPLES + 1):
                    file_ext = 'py' if lang == 'Python' else 'java'
                    filename = f'{i:03d}_SplayTree.{file_ext}'
                    filepath = os.path.join(base_path, filename)
                    
                    if not os.path.exists(filepath):
                        continue

                    if lang == 'Java':
                        category, time_ms = run_java_tests(filepath, model, i, suite_config)
                    else:
                        category, time_ms = run_python_tests(filepath, model, i, suite_config)
                    
                    all_results.append({
                        'Model': model,
                        'Language': lang,
                        'SampleID': i,
                        'Test_Suite': suite_name.capitalize(),
                        'Result': category,
                        'ExecutionTime_ms': time_ms
                    })
                    print(f"Tested {model} ({lang} {i:03d}) [{suite_name.upper()}]: {category} (Time: {time_ms:.3f} ms)")
    
    df = pd.DataFrame(all_results)
    df.to_csv(RESULT_CSV, index=False)
    print(f"\n--- Testing Complete ---")
    print(f"Results saved to {RESULT_CSV}")
    
    comparison = df.groupby(['Model', 'Language', 'Test_Suite', 'Result']).size().reset_index(name='Count')
    print("\n--- Summary Comparison (By Test Suite) ---")
    print(comparison)


if __name__ == '__main__':
    orchestrate_testing()