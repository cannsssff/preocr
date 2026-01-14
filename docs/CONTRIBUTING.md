# Contributing to PreOCR

Thank you for your interest in contributing to PreOCR! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/preocr.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
5. Install in development mode: `pip install -e ".[dev]"`
6. Install pre-commit hooks: `pre-commit install`

## Development Workflow

1. Create a new branch for your changes: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Run linting: `ruff check preocr/`
5. Run type checking: `mypy preocr/`
6. Format code: `black preocr/`
7. Commit your changes (pre-commit hooks will run automatically)
8. Push to your fork: `git push origin feature/your-feature-name`
9. Create a Pull Request

## Code Style

- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 100)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and small

## Testing

- Write tests for all new features
- Ensure all existing tests pass
- Aim for high test coverage
- Place tests in the `tests/` directory
- Use descriptive test names: `test_<function_name>_<scenario>`

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in imperative mood (e.g., "Add", "Fix", "Update")
- Reference issue numbers if applicable: "Fix #123: ..."

## Pull Request Guidelines

- Keep PRs focused and small
- Provide a clear description of changes
- Reference related issues
- Ensure CI checks pass
- Request review from maintainers

## Reporting Issues

When reporting issues, please include:
- Python version
- PreOCR version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

## Questions?

Feel free to open an issue for questions or discussions about contributions.

Thank you for contributing to PreOCR!

