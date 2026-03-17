# MindTrace - Model Serving Module

"""
Model serving with Flask REST API
"""

from flask import Flask, request, jsonify
import pickle
import joblib

app = Flask(__name__)
model = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    global model
    
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    # Make prediction
    result = model.predict([text])[0]
    
    return jsonify({'prediction': result})

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    global model
    
    data = request.json
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({'error': 'No texts provided'}), 400
    
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    results = model.predict(texts).tolist()
    
    return jsonify({'predictions': results})

@app.route('/load_model', methods=['POST'])
def load_model():
    global model
    
    data = request.json
    model_path = data.get('model_path', 'model.pkl')
    
    try:
        model = joblib.load(model_path)
        return jsonify({'status': 'Model loaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def start_server(model_path='model.pkl', port=5000):
    global model
    try:
        model = joblib.load(model_path)
    except:
        pass
    
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    start_server()
