import pytest
import importlib.util
import time
import subprocess
import sys
import json
import random
from conftest import GLOBAL_TEST_RESULTS

NUM_KEYS_HARD = 200000
NUM_SEARCHES_HARD = 4000000
MIN_KEY = 1

JAVA_BASELINE_MS = 33.0
PYTHON_BASELINE_MS = 430.0
EFFICIENCY_THRESHOLD_FACTOR = 1.2

_TEST_RESULTS = {"time_ms": 0.0, "passed": False}

def check_bst_property(node):
    if node is None:
        return True
    if node.left and node.left.key > node.key:
        return False
    if node.right and node.right.key < node.key:
        return False
    return check_bst_property(node.left) and check_bst_property(node.right)

@pytest.fixture
def run_python_tests(module_path):
    spec = importlib.util.spec_from_file_location("splay_module", module_path)
    splay_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(splay_module)
    
    if not hasattr(splay_module, 'SplayTree'):
        raise AttributeError("SplayTree class not found.")
        
    Tree = splay_module.SplayTree
    tree = Tree()
    return tree

def test_01_hard_functional_check(run_python_tests):
    tree = run_python_tests
    tree.insert(10);
    tree.insert(20);
    assert tree.search(10) is True
    tree.delete(10)
    assert tree.search(10) is False

def test_02_algorithmic_efficiency_hard(module_path):
    global GLOBAL_TEST_RESULTS
    spec = importlib.util.spec_from_file_location("splay_module", module_path)
    splay_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(splay_module)
    Tree = splay_module.SplayTree
    
    tree = Tree()
    
    for i in range(MIN_KEY, NUM_KEYS_HARD + MIN_KEY):
        tree.insert(i)

    start_time = time.perf_counter()
    for _ in range(NUM_SEARCHES_HARD):
        tree.search(MIN_KEY)
    end_time = time.perf_counter()
    
    measured_time_ms = (end_time - start_time) * 1000
    
    GLOBAL_TEST_RESULTS["time_ms"] = measured_time_ms
    
    if measured_time_ms > EFFICIENCY_THRESHOLD_FACTOR * PYTHON_BASELINE_MS:
        raise AssertionError(f"Algorithmic Efficiency Failure: Time {measured_time_ms:.2f}ms exceeds baseline.")
        
    assert measured_time_ms <= 10 * PYTHON_BASELINE_MS