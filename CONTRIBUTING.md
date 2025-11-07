# Contributing to APOS

Thank you for your interest in contributing to the Advanced Prompt Optimization System (APOS)! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Provide constructive feedback
- Focus on what is best for the community

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/learnaikid-collab/iRESARCH-LABs/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Error messages or logs

### Suggesting Enhancements

1. Check if the enhancement has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach
   - Any relevant examples or references

### Contributing Code

#### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/iRESARCH-LABs.git
cd iRESARCH-LABs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black flake8 mypy isort pytest-cov
```

#### Development Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Format Code**
   ```bash
   # Format with black
   black src/ tests/
   
   # Sort imports
   isort src/ tests/
   
   # Check linting
   flake8 src/ tests/
   
   # Type check
   mypy src/
   ```

4. **Write Tests**
   - Add tests for new features
   - Ensure existing tests pass
   - Aim for good test coverage
   
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check coverage
   pytest --cov=src tests/
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```
   
   Commit message guidelines:
   - Use present tense ("Add feature" not "Added feature")
   - Be descriptive but concise
   - Reference issues if applicable (#123)

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a pull request on GitHub with:
   - Clear title and description
   - Link to related issues
   - Summary of changes
   - Testing performed

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable and function names
- Keep functions focused and small
- Add docstrings to modules, classes, and functions
- Use type hints where appropriate

Example:
```python
def analyze_task(request: str) -> TaskAnalysis:
    """
    Analyze a user request to determine task characteristics.
    
    Args:
        request: The user's request/prompt
        
    Returns:
        TaskAnalysis object with complete analysis
        
    Raises:
        ValueError: If request is empty
    """
    if not request.strip():
        raise ValueError("Request cannot be empty")
    
    # Implementation...
    return analysis
```

### Documentation Style

- Use Markdown for documentation files
- Include code examples where helpful
- Keep language clear and concise
- Update relevant docs when changing features

### Testing Guidelines

- Test both success and failure cases
- Use descriptive test names
- Keep tests independent
- Mock external dependencies (API calls, etc.)

Example:
```python
def test_task_analyzer_classifies_code_generation():
    """Test that code generation tasks are properly classified."""
    analyzer = TaskAnalyzer()
    request = "Write a Python function to sort a list"
    
    analysis = analyzer.analyze(request)
    
    assert analysis.task_type == TaskType.CODE_GENERATION
    assert analysis.requires_examples is True
```

## Project Structure

Understanding the project structure helps with contributions:

```
iRESARCH-LABs/
├── src/                    # Source code
│   ├── core/              # Core components
│   ├── optimization/      # Optimization algorithms
│   ├── knowledge/         # Knowledge management
│   ├── safety/           # Safety and alignment
│   └── web/              # Web interface
├── tests/                 # Test files
├── docs/                  # Documentation
├── config/               # Configuration files
└── requirements.txt      # Dependencies
```

## Areas for Contribution

### High Priority

- [ ] Additional optimization algorithms
- [ ] Improved safety checking
- [ ] Performance optimizations
- [ ] Better error handling
- [ ] More comprehensive tests

### Medium Priority

- [ ] Additional LLM provider support (OpenAI, Anthropic)
- [ ] Enhanced web UI features
- [ ] Batch processing capabilities
- [ ] Advanced RAG implementation
- [ ] Analytics and visualization

### Good First Issues

- [ ] Documentation improvements
- [ ] Additional test cases
- [ ] Code examples and tutorials
- [ ] Bug fixes
- [ ] UI/UX enhancements

## Review Process

1. All contributions require review
2. Reviewers will check:
   - Code quality and style
   - Test coverage
   - Documentation updates
   - Functionality
3. Address reviewer feedback
4. Once approved, code will be merged

## Release Process

- Semantic versioning (MAJOR.MINOR.PATCH)
- Changelog maintained in releases
- Tagged releases on GitHub

## Getting Help

- Ask questions in [GitHub Discussions](https://github.com/learnaikid-collab/iRESARCH-LABs/discussions)
- Check existing documentation
- Review closed issues and PRs for similar problems

## Recognition

Contributors will be:
- Listed in the project README
- Mentioned in release notes
- Thanked in the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to APOS! 🚀
