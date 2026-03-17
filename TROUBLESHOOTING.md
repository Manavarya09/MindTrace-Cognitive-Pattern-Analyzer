# MindTrace - Troubleshooting Guide

## Common Issues

## Installation Issues

### Issue: NLTK data not found
**Solution:**
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')
```

### Issue: spaCy model not found
**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### Issue: ModuleNotFoundError
**Solution:**
```bash
pip install -r requirements.txt
```

## Runtime Issues

### Issue: Empty dataframe after loading
**Check:**
- CSV has 'timestamp' and 'text' columns
- Date format matches expected format
- File encoding is UTF-8

### Issue: Sentiment analysis returns all neutral
**Possible causes:**
- Text is very short
- Text contains no emotional words
**Solution:** Check text preprocessing

### Issue: Clustering shows only one cluster
**Possible causes:**
- Not enough data
- Text is too similar
**Solution:** Increase n_samples or use more diverse data

## Visualization Issues

### Issue: Plotly charts not displaying
**Solution:**
```python
import plotly.io as pio
pio.renderers.default = "browser"
```

### Issue: Word cloud is empty
**Possible causes:**
- All text was filtered as stopwords
- Text is too short
**Solution:** Check preprocessing

## Memory Issues

### Issue: Out of memory with large dataset
**Solution:**
- Reduce n_samples
- Use sampling in aggregation
- Process in batches

## Performance Issues

### Issue: Analysis is slow
**Possible causes:**
- Too many entries
- Complex NLP operations
**Solution:**
- Reduce sample size
- Skip optional preprocessing

## Data Format Issues

### Issue: Timestamp parsing errors
**Supported formats:**
- 2024-01-01 10:30:00
- 2024-01-01
- 01/01/2024 10:30:00
- 01/01/2024

### Issue: Text column not found
**Solution:** Ensure CSV has 'text' column name
