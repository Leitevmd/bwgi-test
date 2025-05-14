# Code Test: Utilities for Property Caching, Reverse File Reading, and Transaction Reconciliation

This repository was created as a response to a coding test. It contains three self-contained Python modules, each with its own functionality, tests, and benchmarks.

## 🧩 Modules

### 1. `reconcile_accounts`

Efficiently compares two lists of financial transactions and reconciles each row by matching on department, amount, payee, and date (with ±1 day tolerance).

### 2. `last_lines`

A UTF-8-safe file reader that retrieves the last lines of a large text file without loading the entire content into memory. 

### 3. `computed_property`

A decorator for defining computed, cached properties in Python classes. 

---

## ✅ Running Tests

To execute all unit tests:

```bash
python -m unittest discover -s tests
```

---

## 🚀 Running Benchmarks

Benchmarks are located in the `benchmarks/` folder.

Run them individually:

```bash
python benchmarks/benchmark_computed_property.py
python benchmarks/benchmark_last_lines.py
python benchmarks/benchmark_reconcile.py
```

---

## 💡 Usage Examples

You can explore example usage for each module:

- `use_computed_property.py`
- `use_last_lines.py`
- `use_reconcile_accounts.py`

---

## 🔧 Requirements

- Python 3.9
- No external dependencies required