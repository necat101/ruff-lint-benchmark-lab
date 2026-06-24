# Ruff Lint Benchmark Lab

A practical comparison of Python linting and formatting tools, inspired by the [Hacker News discussion on Ruff](https://news.ycombinator.com/item?id=34788020) - a fast Python linter written in Rust.

## What HN Users Were Debating

The Hacker News thread on Ruff highlighted several key tensions in Python tooling:

### 1. **"10-100x Faster" vs Real-World Impact**
- **Ruff claims**: 10-100x faster than Flake8/Pylint, linting CPython in 300ms vs 30-60 seconds
- **Skepticism**: For small codebases or single-file edits, the difference is imperceptible
- **Reality**: Speed matters most in CI/CD, pre-commit hooks, and large codebases where linters run frequently

### 2. **Rust vs Python for Tooling**
- **Pro-Rust**: Fearless concurrency, zero-cost abstractions, memory control enable real performance gains
- **Pro-Python**: Tooling should be written in the language it targets for dogfooding and contributor accessibility
- **Middle ground**: Python tooling increasingly uses Rust/C for performance-critical parts (see: pydantic-core, orjson)

### 3. **Single Tool vs Ecosystem**
- **Ruff approach**: One binary replaces Flake8, isort, pyupgrade, and more - "batteries included"
- **Traditional approach**: Composable tools (flake8 + isort + black + ...) allow mix-and-match
- **Trade-off**: Integration vs flexibility; Ruff is faster but less extensible

### 4. **Feature Parity vs Speed**
- **Ruff**: Implements 700+ rules from popular linters, but not 100% parity with Pylint's 300+ checks
- **Pylint**: More comprehensive analysis (e.g., type inference, deeper code understanding) but slower
- **Question**: Is "fast with 90% coverage" better than "slow with 100% coverage"?

### 5. **Formatter Compatibility**
- **Black**: The uncompromising formatter - "you get what you get"
- **Ruff formatter**: Designed to be Black-compatible but implemented in Rust
- **Debate**: Should formatters be configurable or opinionated? Is Black compatibility a feature or a constraint?

### 6. **Import Sorting: Ruff vs isort**
- **isort**: Highly configurable, supports custom sections, "flying" imports to top
- **Ruff**: Faster, Black-compatible by default, but fewer configuration options
- **Migration pain**: Projects with complex isort configs may not get identical results

### 7. **Caching and Cold Starts**
- **Ruff**: Aggressive caching, incremental checking
- **Traditional tools**: Often re-parse everything each run
- **Impact**: First run vs subsequent runs show dramatically different performance profiles

### 8. **Editor and CI Ergonomics**
- **Fast tools enable**: Lint-on-save, real-time feedback, running in pre-commit hooks without noticing
- **Slow tools lead to**: Disabling checks, running them less frequently, "I'll fix it later"
- **Developer experience**: A tool that's 10x faster might get run 10x more often

### 9. **"Ruff is Faster" ≠ "Ruff is Better"**
Different tools optimize for different things:

| Tool | Strength | Weakness | Best For |
|------|----------|----------|----------|
| **Ruff** | Speed, all-in-one | Not 100% feature parity | Fast feedback, CI/CD |
| **Flake8** | Mature, extensible | Slower, plugin ecosystem | Custom rules, legacy projects |
| **Pylint** | Deep analysis | Very slow, noisy | Comprehensive checking |
| **Black** | Opinionated, consistent | No configuration | Teams wanting zero bike-shedding |
| **isort** | Highly configurable | Slower than Ruff | Complex import layouts |

### 10. **The "Good Enough" Threshold**
- HN comment: "For my 22k line codebase, pylint takes 18 seconds, ruff takes 0.1 seconds"
- Counter: "But for most codebases, both are quasi-instant - who cares?"
- Reality: The threshold where speed matters depends on workflow, codebase size, and how often you run the tool

## This Benchmark

Instead of synthetic "X times faster" claims, this lab tests realistic scenarios:

### Test Corpus
- **Clean files**: Properly formatted Python with no issues
- **Files with issues**: Unused imports, undefined names, long lines, bad import order
- **Modern Python**: Type annotations, f-strings, match/case syntax
- **Edge cases**: Syntax errors, unicode identifiers, noqa comments, per-file ignores
- **Scale variants**: Many tiny files (50x) vs few large files (100 functions)
- **Project structure**: Nested packages, pyproject.toml config, vendored files to skip

### Operations Tested
1. **Lint checks**: Find issues without fixing
2. **Fixable checks**: Auto-fix what can be fixed safely
3. **Format check mode**: Verify formatting without changing files
4. **Actual formatting**: Apply formatting changes
5. **Import sorting**: Check and fix import order
6. **Syntax validation**: Handle syntax errors gracefully
7. **Config discovery**: Respect pyproject.toml, per-file ignores, skip patterns

### Tools Compared
- ✅ **Ruff** - If installed, all-in-one linter/formatter
- ⏭️ **Flake8** - If installed, traditional linter
- ⏭️ **Pylint** - If installed, comprehensive analyzer
- ⏭️ **Pyflakes** - If installed, fast logical checker
- ⏭️ **pycodestyle** - If installed, PEP 8 checker
- ⏭️ **Black** - If installed, formatter
- ⏭️ **isort** - If installed, import sorter
- ✅ **compileall** - Always available, syntax validation

Tools not installed are skipped clearly - no fake results.

## Running the Benchmark

```bash
# Generate test corpus
python3 generate_corpus.py

# Run benchmarks (3 trials per test)
python3 benchmark.py

# View results
cat RESULTS.md
```

## What the Results Mean

**Mean time** = Average of 3 runs (cold cache each time unless tool caches internally)

**Key metrics beyond speed:**
- **Diagnostic counts**: Does each tool find the same issues?
- **Fix behavior**: Do auto-fixes produce valid code?
- **Config respect**: Are pyproject.toml, noqa, per-file ignores honored?
- **Error handling**: How do tools handle syntax errors?
- **Output stability**: Does formatting produce consistent results?

## Key Takeaways (From HN Wisdom)

1. **Speed enables frequency** - A linter that takes 0.1s gets run on every save; one that takes 10s gets run in CI only
2. **Integration matters** - Ruff's speed comes partly from doing one parse for many checks vs multiple tools parsing separately
3. **"Fast enough" is contextual** - 100ms vs 1000ms matters for editor integration; 1s vs 10s matters for CI
4. **Feature parity is hard** - Replacing an ecosystem of tools requires matching not just speed but behavior
5. **Rust is a means, not an end** - The performance comes from architecture decisions enabled by Rust, not Rust itself
6. **Ecosystem effects** - Fast tools change workflows (more frequent checks, tighter feedback loops)

## Files

- `generate_corpus.py` - Creates reproducible Python test corpus
- `benchmark.py` - Runs comparisons, checks correctness, generates RESULTS.md
- `corpus/` - Generated test files (gitignored, reproducible)
- `RESULTS.md` - Benchmark output with timings and tool versions

## Requirements

Python 3.8+ with standard library only. Optional tools (install as needed):
- `ruff` - `pip install ruff`
- `flake8` - `pip install flake8`
- `pylint` - `pip install pylint`
- `black` - `pip install black`
- `isort` - `pip install isort`
- `pyflakes` - `pip install pyflakes`
- `pycodestyle` - `pip install pycodestyle`

## Honest Limitations

- This benchmark measures tool invocation time, not just core logic
- Results vary by system, filesystem, and Python version
- Caching behavior differs between tools and affects results
- We test a specific corpus; your mileage may vary
- Speed is one factor; features, accuracy, and ecosystem matter too

The goal isn't to crown a "fastest linter" but to understand trade-offs for real development workflows.
