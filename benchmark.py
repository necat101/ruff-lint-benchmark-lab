#!/usr/bin/env python3
"""
Ruff Lint Benchmark Lab - Main Benchmark Runner
Compares ruff, flake8, pylint, pyflakes, pycodestyle, black, isort.
"""

import subprocess
import time
import os
import sys
import json
from pathlib import Path
from datetime import datetime
import statistics

class ToolAvailability:
    """Check which tools are available"""
    def __init__(self):
        self.tools = {}
        self.check_tools()
    
    def check_tools(self):
        tools_to_check = {
            'ruff': ['ruff', '--version'],
            'flake8': ['flake8', '--version'],
            'pylint': ['pylint', '--version'],
            'pyflakes': ['pyflakes', '--version'],
            'pycodestyle': ['pycodestyle', '--version'],
            'black': ['black', '--version'],
            'isort': ['isort', '--version'],
        }
        
        for tool, cmd in tools_to_check.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                self.tools[tool] = result.returncode == 0
                if self.tools[tool]:
                    output = result.stdout + result.stderr
                    self.tools[f'{tool}_version'] = output.split('\n')[0][:50]
                else:
                    self.tools[f'{tool}_version'] = None
            except:
                self.tools[tool] = False
                self.tools[f'{tool}_version'] = None
        
        self.tools['compileall'] = True
    
    def report(self):
        lines = ["## Tool Availability", ""]
        for tool in ['ruff', 'flake8', 'pylint', 'pyflakes', 'pycodestyle', 'black', 'isort', 'compileall']:
            available = self.tools.get(tool, False)
            status = "✓" if available else "✗"
            version = self.tools.get(f'{tool}_version', '')
            version_str = f" ({version})" if version else ""
            lines.append(f"- {status} {tool}{version_str}")
        return "\n".join(lines)

class BenchmarkRunner:
    def __init__(self, corpus_dir="corpus", results_file="RESULTS.md"):
        self.corpus_dir = Path(corpus_dir)
        self.results_file = results_file
        self.tools = ToolAvailability()
        self.trials = 3
    
    def time_operation(self, func, *args, **kwargs):
        """Time an operation with multiple trials"""
        times = []
        for _ in range(self.trials):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                result = None
                success = False
            end = time.perf_counter()
            times.append(end - start)
        
        return {
            'times': times,
            'mean': statistics.mean(times),
            'min': min(times),
            'max': max(times),
            'result': result,
            'success': success
        }
    
    def run_ruff_check(self, path):
        """Run ruff check"""
        result = subprocess.run(
            ['ruff', 'check', str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'issues': len([l for l in result.stdout.split('\n') if l.strip()])
        }
    
    def run_ruff_format_check(self, path):
        """Run ruff format --check"""
        result = subprocess.run(
            ['ruff', 'format', '--check', str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'returncode': result.returncode,
            'needs_formatting': result.returncode != 0
        }
    
    def run_flake8(self, path):
        """Run flake8"""
        result = subprocess.run(
            ['flake8', str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'issues': len([l for l in result.stdout.split('\n') if l.strip()])
        }
    
    def run_black_check(self, path):
        """Run black --check"""
        result = subprocess.run(
            ['black', '--check', '--diff', str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'returncode': result.returncode,
            'needs_formatting': result.returncode != 0
        }
    
    def run_isort_check(self, path):
        """Run isort --check"""
        result = subprocess.run(
            ['isort', '--check', '--diff', str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'returncode': result.returncode,
            'needs_sorting': result.returncode != 0
        }
    
    def run_compileall(self, path):
        """Run python -m compileall"""
        result = subprocess.run(
            [sys.executable, '-m', 'compileall', '-q', str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'returncode': result.returncode,
            'success': result.returncode == 0
        }
    
    def benchmark_tool(self, tool_name, func, path, description):
        """Benchmark a single tool"""
        print(f"    - {tool_name}...", end=" ", flush=True)
        result = self.time_operation(func, path)
        status = "✓" if result['success'] else "✗"
        print(f"{status} {result['mean']*1000:.1f}ms")
        return {
            'tool': tool_name,
            'description': description,
            'mean_ms': result['mean'] * 1000,
            'min_ms': result['min'] * 1000,
            'success': result['success'],
            'result': result['result']
        }
    
    def run_benchmarks(self):
        """Run all benchmarks"""
        print("=" * 70)
        print("Ruff Lint Benchmark Lab")
        print("=" * 70)
        print(self.tools.report())
        print()
        
        results = []
        
        print(f"\nBenchmarking on corpus: {self.corpus_dir}")
        print("-" * 70)
        
        if self.tools.tools['ruff']:
            results.append(self.benchmark_tool(
                'ruff check',
                self.run_ruff_check,
                self.corpus_dir,
                'Lint check with ruff'
            ))
            
            results.append(self.benchmark_tool(
                'ruff format --check',
                self.run_ruff_format_check,
                self.corpus_dir,
                'Format check with ruff'
            ))
        
        if self.tools.tools['flake8']:
            results.append(self.benchmark_tool(
                'flake8',
                self.run_flake8,
                self.corpus_dir,
                'Lint check with flake8'
            ))
        
        if self.tools.tools['black']:
            results.append(self.benchmark_tool(
                'black --check',
                self.run_black_check,
                self.corpus_dir,
                'Format check with black'
            ))
        
        if self.tools.tools['isort']:
            results.append(self.benchmark_tool(
                'isort --check',
                self.run_isort_check,
                self.corpus_dir,
                'Import sort check with isort'
            ))
        
        if self.tools.tools['compileall']:
            results.append(self.benchmark_tool(
                'compileall',
                self.run_compileall,
                self.corpus_dir,
                'Python compile check'
            ))
        
        self.save_results(results)
        return results
    
    def save_results(self, results):
        """Save results to markdown file"""
        print(f"\n\nSaving results to {self.results_file}...")
        
        with open(self.results_file, 'w') as f:
            f.write("# Ruff Lint Benchmark Results\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            f.write("## System Information\n\n")
            f.write(f"- **Python**: {sys.version.split()[0]}\n")
            f.write(f"- **Platform**: {sys.platform}\n\n")
            
            f.write(self.tools.report())
            f.write("\n\n")
            
            f.write("## Benchmark Results\n\n")
            f.write("| Tool | Description | Mean (ms) | Min (ms) | Success |\n")
            f.write("|------|-------------|-----------|----------|---------|\n")
            
            for r in results:
                f.write(f"| {r['tool']} | {r['description']} | "
                       f"{r['mean_ms']:.1f} | {r['min_ms']:.1f} | "
                       f"{'✓' if r['success'] else '✗'} |\n")
            
            f.write("\n")
        
        print(f"Results saved to {self.results_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Ruff Lint Benchmark Lab')
    parser.add_argument('--corpus', default='corpus', help='Corpus directory')
    parser.add_argument('--trials', type=int, default=3, help='Number of trials')
    
    args = parser.parse_args()
    
    corpus_path = Path(args.corpus)
    if not corpus_path.exists():
        print("Corpus not found, generating...")
        import generate_corpus
        generate_corpus.generate_corpus(args.corpus)
    
    runner = BenchmarkRunner(args.corpus)
    runner.trials = args.trials
    runner.run_benchmarks()
    
    print("\n" + "=" * 70)
    print("Benchmark complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
