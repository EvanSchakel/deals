# Contributing to Deal Analyzer

First off, thank you for considering contributing to Deal Analyzer!

## How to Contribute

### 1. Adding a New Product

The core of Deal Analyzer is its product database (`products.py`). If you want to add a new product:

1. Open `products.py`.
2. Add a new entry to the `PRODUCTS` dictionary.
3. Make sure to define `retail`, `good`, `great`, `ram_gate` (if applicable), `tags`, and `upgrades`.
4. Ensure your product works correctly when running `python deal_analyzer.py --list-products`.
5. Run tests using `python -m unittest discover` before submitting a Pull Request.

### 2. Reporting Issues

If you find a bug or have a feature request, please open an issue in the GitHub repository. Provide as much detail as possible, including:
- Steps to reproduce the issue.
- The expected behavior.
- The actual behavior (including screenshots or command outputs if applicable).

### 3. Submitting a Pull Request

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Make your changes.
4. Ensure the codebase remains pure-stdlib and has no external dependencies.
5. Run the tests: `python -m unittest discover`.
6. Commit your changes with a descriptive message.
7. Push your branch to your fork.
8. Open a Pull Request against the `main` branch.

### Testing Guidelines

We have a suite of tests in the `test_*.py` files. Always make sure to write tests for your changes or ensure your changes pass existing tests before opening a pull request.
