# MindTrace - Contributing Guide

## Contributing to MindTrace

We welcome contributions! Here's how you can help:

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/Manavarya09/MindTrace-Cognitive-Pattern-Analyzer.git
cd MindTrace
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Download NLTK data
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
```

5. Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

## Making Changes

1. Create a feature branch
```bash
git checkout -b feature-name
```

2. Make your changes

3. Test locally
```bash
jupyter notebook MindTrace.ipynb
```

4. Commit changes
```bash
git add .
git commit -m "Description of changes"
```

5. Push to GitHub
```bash
git push origin feature-name
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Reporting Issues

- Use GitHub Issues
- Describe the problem
- Include reproduction steps
- Attach relevant screenshots

## Feature Requests

- Open an Issue
- Describe the feature
- Explain use cases

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
