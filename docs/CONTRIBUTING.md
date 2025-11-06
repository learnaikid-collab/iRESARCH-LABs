# Contributing Guidelines

Thank you for your interest in contributing to iRESARCH-LABs! This document provides guidelines for contributing to our AI Research & Engineering Lab.

## How to Contribute

### Research Contributions

1. **Propose Research Ideas**
   - Open an issue with the `research-proposal` label
   - Describe your research question and approach
   - Wait for feedback from maintainers

2. **Submit Research**
   - Fork the repository
   - Create your research in the `research/` directory
   - Include clear documentation and reproducible code
   - Submit a pull request

3. **Research Standards**
   - Document your methodology clearly
   - Provide reproducible experiments
   - Include references to related work
   - Share datasets or provide access instructions

### Engineering Contributions

1. **Feature Development**
   - Check existing issues or create a new one
   - Discuss your approach before major changes
   - Follow our coding standards
   - Write tests for your code

2. **Bug Fixes**
   - Open an issue describing the bug
   - Submit a PR with the fix
   - Include tests that verify the fix

3. **Engineering Standards**
   - Write clean, documented code
   - Follow PEP 8 for Python code
   - Add appropriate tests
   - Update documentation

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

### Documentation
- Write clear, concise documentation
- Include examples where helpful
- Keep README files up to date
- Document all public APIs

## Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass
   - Update documentation
   - Add yourself to CONTRIBUTORS.md
   - Write clear commit messages

2. **PR Description**
   - Describe what changes you made
   - Explain why the changes are needed
   - Reference related issues
   - Include any breaking changes

3. **Review Process**
   - Maintainers will review your PR
   - Address feedback promptly
   - Keep PRs focused and manageable
   - Be patient and respectful

## Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/iRESARCH-LABs.git
cd iRESARCH-LABs

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

## Questions?

If you have questions:
- Open an issue with the `question` label
- Check existing documentation
- Reach out to maintainers

Thank you for contributing to iRESARCH-LABs!
