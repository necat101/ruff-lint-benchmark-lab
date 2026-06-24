# Ruff Lint Benchmark Results

Generated: 2026-06-24T18:47:26.812354

## System Information

- **Python**: 3.12.3
- **Platform**: linux

## Tool Availability

- ✗ ruff
- ✗ flake8
- ✗ pylint
- ✗ pyflakes
- ✗ pycodestyle
- ✗ black
- ✗ isort
- ✓ compileall

## Benchmark Results

| Tool | Description | Mean (ms) | Min (ms) | Success |
|------|-------------|-----------|----------|---------|
| compileall | Python compile check | 197.0 | 171.0 | ✓ |

## Detailed Results

### compileall

```json
{
  "returncode": 1,
  "success": false
}
```

## Notes

- Results from test run on corpus with 77 Python files
- Tools not installed are skipped (marked ✗ in availability)
- Install tools with: pip install ruff black isort flake8 pylint
- Re-run benchmark to get comparative results
