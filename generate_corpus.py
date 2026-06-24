#!/usr/bin/env python3
"""
Ruff Lint Benchmark Lab - Corpus Generator
Generates reproducible Python project with various linting scenarios.
"""

import os
from pathlib import Path
import random
import string

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def generate_clean_file(path, lines=50):
    """Generate a clean Python file with no issues"""
    with open(path, 'w') as f:
        f.write('"""Clean module with proper style."""\n\n')
        f.write('import os\n')
        f.write('import sys\n\n')
        f.write('def hello_world(name: str) -> str:\n')
        f.write('    """Return a greeting."""\n')
        f.write('    return f"Hello, {name}!"\n\n')
        f.write('def main():\n')
        f.write('    """Main entry point."""\n')
        f.write('    print(hello_world("World"))\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    main()\n')

def generate_with_unused_imports(path):
    """Generate file with unused imports"""
    with open(path, 'w') as f:
        f.write('import os\n')
        f.write('import sys\n')
        f.write('import json\n')
        f.write('import random\n\n')
        f.write('def foo():\n')
        f.write('    return 42\n')

def generate_with_undefined_names(path):
    """Generate file with undefined names"""
    with open(path, 'w') as f:
        f.write('def bar():\n')
        f.write('    x = undefined_variable\n')
        f.write('    y = another_undefined\n')
        f.write('    return x + y\n')

def generate_with_long_lines(path):
    """Generate file with long lines"""
    with open(path, 'w') as f:
        f.write('def long_function():\n')
        f.write('    x = "This is a very long line that exceeds the typical 88 or 100 character limit that most Python style guides recommend for code formatting purposes"\n')
        f.write('    return x\n')

def generate_with_import_order_issues(path):
    """Generate file with import order problems"""
    with open(path, 'w') as f:
        f.write('import sys\n')
        f.write('import os\n')
        f.write('from pathlib import Path\n')
        f.write('import json\n\n')
        f.write('def test():\n')
        f.write('    pass\n')

def generate_with_type_annotations(path):
    """Generate file with type annotations"""
    with open(path, 'w') as f:
        f.write('from typing import List, Dict, Optional\n\n')
        f.write('def process_items(items: List[str]) -> Dict[str, int]:\n')
        f.write('    """Process a list of items."""\n')
        f.write('    result: Dict[str, int] = {}\n')
        f.write('    for item in items:\n')
        f.write('        result[item] = len(item)\n')
        f.write('    return result\n')

def generate_with_fstrings(path):
    """Generate file with f-strings"""
    with open(path, 'w') as f:
        f.write('def format_user(name, age, city):\n')
        f.write('    return f"User {name} is {age} years old and lives in {city}"\n\n')
        f.write('def debug_values(a, b, c):\n')
        f.write('    print(f"{a=}, {b=}, {c=}")\n')

def generate_with_match_case(path):
    """Generate file with match/case (Python 3.10+)"""
    with open(path, 'w') as f:
        f.write('def handle_status(status):\n')
        f.write('    match status:\n')
        f.write('        case 200:\n')
        f.write('            return "OK"\n')
        f.write('        case 404:\n')
        f.write('            return "Not Found"\n')
        f.write('        case _:\n')
        f.write('            return "Unknown"\n')

def generate_with_noqa(path):
    """Generate file with noqa comments"""
    with open(path, 'w') as f:
        f.write('import os  # noqa: F401\n')
        f.write('import sys  # noqa\n\n')
        f.write('def foo():\n')
        f.write('    x = 1  # noqa: F841\n')
        f.write('    return 42\n')

def generate_syntax_error(path):
    """Generate file with syntax error"""
    with open(path, 'w') as f:
        f.write('def broken(\n')
        f.write('    return "missing closing paren"\n')

def generate_unicode_file(path):
    """Generate file with unicode identifiers and comments"""
    with open(path, 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('"""Module with unicode: café, naïve, résumé"""\n\n')
        f.write('def héllo():\n')
        f.write('    """Function with unicode name."""\n')
        f.write('    café = "coffee"\n')
        f.write('    return café\n')

def generate_corpus(output_dir="corpus"):
    """Generate complete Python test corpus"""
    ensure_dir(output_dir)
    ensure_dir(f"{output_dir}/nested")
    ensure_dir(f"{output_dir}/nested/deep")
    
    print("Generating Python lint benchmark corpus...")
    
    # Clean files
    print("  - clean files")
    for i in range(10):
        generate_clean_file(f"{output_dir}/clean_{i:02d}.py")
    
    # Files with specific issues
    print("  - files with lint issues")
    generate_with_unused_imports(f"{output_dir}/unused_imports.py")
    generate_with_undefined_names(f"{output_dir}/undefined_names.py")
    generate_with_long_lines(f"{output_dir}/long_lines.py")
    generate_with_import_order_issues(f"{output_dir}/bad_imports.py")
    
    # Modern Python features
    print("  - modern Python features")
    generate_with_type_annotations(f"{output_dir}/type_annotations.py")
    generate_with_fstrings(f"{output_dir}/fstrings.py")
    generate_with_match_case(f"{output_dir}/match_case.py")
    
    # Special cases
    print("  - special cases")
    generate_with_noqa(f"{output_dir}/with_noqa.py")
    generate_syntax_error(f"{output_dir}/syntax_error.py")
    generate_unicode_file(f"{output_dir}/unicode_test.py")
    
    # Many tiny files
    print("  - many tiny files")
    ensure_dir(f"{output_dir}/many_small")
    for i in range(50):
        with open(f"{output_dir}/many_small/tiny_{i:03d}.py", 'w') as f:
            f.write(f'x = {i}\n')
    
    # Large module
    print("  - large module")
    with open(f"{output_dir}/large_module.py", 'w') as f:
        f.write('"""Large module with many functions."""\n\n')
        for i in range(100):
            f.write(f'def func_{i}():\n')
            f.write(f'    """Function {i}."""\n')
            f.write(f'    return {i} * 2\n\n')
    
    # Nested packages
    print("  - nested packages")
    for path in [f"{output_dir}/nested/__init__.py", 
                 f"{output_dir}/nested/deep/__init__.py"]:
        with open(path, 'w') as f:
            f.write('"""Package init."""\n')
    
    with open(f"{output_dir}/nested/module.py", 'w') as f:
        f.write('from .deep import helper\n\n')
        f.write('def main():\n')
        f.write('    helper()')
    
    with open(f"{output_dir}/nested/deep/helper.py", 'w') as f:
        f.write('def helper():\n')
        f.write('    pass\n')
    
    # pyproject.toml
    print("  - pyproject.toml")
    with open(f"{output_dir}/pyproject.toml", 'w') as f:
        f.write('[tool.ruff]\n')
        f.write('line-length = 88\n')
        f.write('target-version = "py38"\n\n')
        f.write('[tool.ruff.lint]\n')
        f.write('select = ["E", "F", "I"]\n')
        f.write('ignore = ["E501"]\n\n')
        f.write('[tool.black]\n')
        f.write('line-length = 88\n')
    
    # Files to be skipped
    print("  - files to skip")
    ensure_dir(f"{output_dir}/vendor")
    with open(f"{output_dir}/vendor/vendored.py", 'w') as f:
        f.write('# Vendored file - should be skipped\n')
        f.write('x=1+2+3+4+5\n')
    
    print(f"\nCorpus generated in '{output_dir}/'")
    total_files = sum(1 for _ in Path(output_dir).rglob('*.py'))
    total_files += sum(1 for _ in Path(output_dir).rglob('*.toml'))
    print(f"Total files: {total_files}")

if __name__ == "__main__":
    generate_corpus()
