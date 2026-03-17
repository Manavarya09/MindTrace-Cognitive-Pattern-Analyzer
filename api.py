# MindTrace - Web API Module

"""
Flask API for MindTrace
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize analyzer
analyzer = None

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    sentiment = sia.polarity_scores(text)
    emotions = nlp_analyzer.detect_emotions(text)
    
    return jsonify({
        'text': text,
        'sentiment': {
            'polarity': sentiment['compound'],
            'label': 'positive' if sentiment['compound'] > 0.05 else 'negative' if sentiment['compound'] < -0.05 else 'neutral'
        },
        'emotions': emotions
    })

@app.route('/batch', methods=['POST'])
def batch_analyze():
    data = request.json
    texts = data.get('texts', [])
    
    results = []
    for text in texts:
        sentiment = sia.polarity_scores(text)
        results.append({
            'text': text,
            'polarity': sentiment['compound']
        })
    
    return jsonify({'results': results})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
