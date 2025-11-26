import pytest
import importlib.util
import time
from typing import List, Optional
import subprocess
import sys
import json
import random
from conftest import GLOBAL_TEST_RESULTS

NUM_KEYS_EFFICIENCY = 50_000
NUM_SEARCHES_EFFICIENCY = 1_000_000
MIN_KEY = 1

JAVA_BASELINE_MS = 10.0
PYTHON_BASELINE_MS = 105.0
EFFICIENCY_THRESHOLD_FACTOR = 1.2

_TEST_RESULTS = {"time_ms": 0.0, "passed": False}

SIMPLE_SEQUENCE = [10, 5, 15, 7, 3, 12]

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

def test_01_intermediate_complexity(run_python_tests):
    tree = run_python_tests
    
    assert tree.search(5) is False
    
    for key in SIMPLE_SEQUENCE:
        tree.insert(key)
    
    assert tree.search(3) is True
    assert tree.root.key == 3
    assert check_bst_property(tree.root)

    tree.delete(10)
    assert tree.search(10) is False
    assert check_bst_property(tree.root) 

    assert tree.search(12) is True
    assert tree.root.key == 12
    assert check_bst_property(tree.root)

    tree.delete(5); tree.delete(7); tree.delete(15); tree.delete(3); tree.delete(12)
    assert tree.root is None

def test_02_algorithmic_efficiency(module_path):
    global GLOBAL_TEST_RESULTS
    spec = importlib.util.spec_from_file_location("splay_module", module_path)
    splay_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(splay_module)
    Tree = splay_module.SplayTree
    
    tree = Tree()
    
    for i in range(MIN_KEY, NUM_KEYS_EFFICIENCY + MIN_KEY):
        tree.insert(i)

    start_time = time.perf_counter()
    for _ in range(NUM_SEARCHES_EFFICIENCY):
        tree.search(MIN_KEY)
    end_time = time.perf_counter()
    
    measured_time_ms = (end_time - start_time) * 1000
    
    GLOBAL_TEST_RESULTS["time_ms"] = measured_time_ms
    
    if measured_time_ms > EFFICIENCY_THRESHOLD_FACTOR * PYTHON_BASELINE_MS:
        raise AssertionError(f"Algorithmic Efficiency Failure: Time {measured_time_ms:.2f}ms exceeds baseline.")
        
    assert measured_time_ms <= 10 * PYTHON_BASELINE_MS
