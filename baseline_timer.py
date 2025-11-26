import time
import subprocess
import os
from datetime import datetime

NUM_KEYS = 10_000
NUM_SEARCHES = 500_000
MIN_KEY = 1

JAVA_REF_FILE = 'reference_SplayTree.java'
PYTHON_REF_FILE = 'reference_splay_tree.py'

def run_java_baseline():
    print("Compiling Java reference code...")
    
    compile_process = subprocess.run(['javac', JAVA_REF_FILE], capture_output=True, text=True)
    if compile_process.returncode != 0:
        print(f"Java Compilation Error:\n{compile_process.stderr}")
        return None

    total_time = 0
    NUM_RUNS = 500 

    print(f"Running Java baseline ({NUM_SEARCHES} searches)...")

    for i in range(NUM_RUNS):
        run_process = subprocess.run(
            ['java', 'reference_SplayTree', str(NUM_KEYS), str(NUM_SEARCHES), str(MIN_KEY)],
            capture_output=True, text=True, timeout=180
        )

        if run_process.returncode != 0:
            print(f"Java Runtime Error (Run {i}):\n{run_process.stderr}")
            return None

        try:
            time_ms = float(run_process.stdout.strip().split()[-1])
            if i > 0:
                total_time += time_ms
            
        except (ValueError, IndexError):
            print(f"Java Output Error: Could not parse time from output:\n{run_process.stdout}")
            return None
    
    return total_time / (NUM_RUNS - 1)

def run_python_baseline():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ref_st", PYTHON_REF_FILE)
    ref_st = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref_st)
    
    if not hasattr(ref_st, 'SplayTree'):
        print(f"Python Error: Cannot find SplayTree class in {PYTHON_REF_FILE}")
        return None

    SplayTree = ref_st.SplayTree
    
    print(f"Running Python baseline ({NUM_SEARCHES} searches)...")
    
    start_time = time.perf_counter()
    
    tree = SplayTree()
    for i in range(MIN_KEY, NUM_KEYS + MIN_KEY):
        tree.insert(i)
        
    for _ in range(NUM_SEARCHES):
        tree.search(MIN_KEY)
        
    end_time = time.perf_counter()
    
    return (end_time - start_time) * 1000

def run_baseline_timer():
    print("--- Splay Tree Amortized Time Baseline Test ---")
    print(f"Test Configuration: N={NUM_KEYS} Inserts, M={NUM_SEARCHES} Searches")
    print("-" * 45)
    
    python_time = run_python_baseline()
    if python_time is not None:
        print(f"\n[Python Baseline]: {python_time:.3f} ms")
        
    java_time = run_java_baseline()
    if java_time is not None:
        print(f"\n[Java Baseline (Avg 3 runs)]: {java_time:.3f} ms")
        
    print("\nBaseline test complete. Record these times as your O(log n) expected performance.")


if __name__ == '__main__':
    run_baseline_timer()