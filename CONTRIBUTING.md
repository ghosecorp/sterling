# Contributing to Sterling Python Client

Thank you for your interest in contributing to the Sterling Python Client! This document provides guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Multi-Language Clients](#multi-language-clients)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@sterling-cache.dev.

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
- Check the issue tracker to avoid duplicates
- Collect relevant information (Python version, OS, error messages)

When submitting a bug report, include:
- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Code samples** (if applicable)
- **Environment details**

### Suggesting Features

We welcome feature suggestions! When suggesting a feature:
- **Check existing issues** to avoid duplicates
- **Describe the use case** clearly
- **Explain why** this feature would be useful
- **Consider backwards compatibility**

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes
7. Push to your fork
8. Open a Pull Request

## Development Setup

```
# Clone your fork
git clone https://github.com/ghosecorp/sterling-python-client.git
cd sterling-python-client

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=sterling --cov-report=html
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all public methods
- Write clear docstrings for all public APIs
- Keep functions focused and testable
- Maximum line length: 100 characters

### Example

```
def get(self, key: str) -> Optional[str]:
    """
    Retrieve value for the given key.
    
    Args:
        key: The key to retrieve
        
    Returns:
        The value associated with the key, or None if key doesn't exist
        
    Raises:
        ConnectionError: If connection to server is lost
    """
    response = self._send_command(f"GET {key}")
    return None if response == "(nil)" else response
```

### Type Hints

Always use type hints:

```
from typing import Optional, List, Union

def set(self, key: str, value: Union[str, int, float]) -> bool:
    """Set key-value pair."""
    response = self._send_command(f"SET {key} {value}")
    return response == "OK"

def keys(self) -> List[str]:
    """Get all keys."""
    response = self._send_command("KEYS")
    return response.split() if response != "(empty)" else []
```

## Testing

### Running Tests

```
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_client.py

# Run with coverage
pytest --cov=sterling
```

### Writing Tests

Place tests in the `tests/` directory:

```
# tests/test_client.py
import pytest
from sterling import Sterling

def test_set_get():
    """Test basic set and get operations."""
    client = Sterling()
    assert client.set('test_key', 'test_value') is True
    assert client.get('test_key') == 'test_value'
    client.close()

def test_context_manager():
    """Test context manager usage."""
    with Sterling() as client:
        client.set('foo', 'bar')
        assert client.get('foo') == 'bar'
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] CHANGELOG.md updated under `[Unreleased]`
- [ ] Type hints added
- [ ] Docstrings added/updated

### PR Template

When opening a PR, include:

```
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code follows style guide
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, a maintainer will merge
4. Your contribution will be credited in the changelog

## Multi-Language Clients

🌐 **Expanding Beyond Python**: We're building Sterling clients for multiple programming languages!

### Current Status
- ✅ Python (this repository)
- 🚧 JavaScript/Node.js (planned)
- 🚧 Go (planned)
- 🚧 Java (planned)
- 🚧 Rust (planned)

### Want to Build a Client for Another Language?

We'd love your help! Here's how:

1. **Open an issue** describing which language you want to support
2. **Review the Python client** to understand the API
3. **Follow the protocol** documented in the Sterling Server repository
4. **Maintain API consistency** across language clients
5. **Write comprehensive tests**
6. **Document usage** with examples

### Client Guidelines

All Sterling clients should:
- Implement the same core API (set, get, delete, exists, expire, ttl, keys)
- Use idiomatic patterns for the target language
- Include comprehensive tests
- Provide clear documentation with examples
- Support connection configuration (host, port)
- Handle errors gracefully
- Be published to the language's package registry

## Questions?

- **Email**: ghosecorp@gmail.com
- **Discussions**: [GitHub Discussions](https://github.com/ghosecorp/sterling-python-client/discussions)
- **Issues**: [GitHub Issues](https://github.com/ghosecorp/sterling-python-client/issues)

---

Thank you for contributing!

***

These documentation files follow best practices from the open-source community and provide comprehensive guidance for users and contributors to both the server and client libraries.[1][2][3][4][5][6]

[1](https://realpython.com/readme-python-project/)
[2](https://packaging.python.org/guides/making-a-pypi-friendly-readme/)
[3](https://www.pyopensci.org/python-package-guide/documentation/repository-files/readme-file-best-practices.html)
[4](https://contribute.cncf.io/resources/templates/contributing/)
[5](https://openchangelog.com/docs/getting-started/keep-a-changelog/)
[6](https://mozillascience.github.io/working-open-workshop/contributing/)
[7](https://packaging.python.org/tutorials/packaging-projects/)
[8](https://github.com/matiassingers/awesome-readme)
[9](https://www.reddit.com/r/Python/comments/y3inzj/best_practices_for_providing_examples_for_python/)
[10](https://towncrier.readthedocs.io/en/stable/markdown.html)