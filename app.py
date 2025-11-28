import os
import logging
import threading
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from quiz_solver import QuizSolver

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

EMAIL = os.getenv('EMAIL')
SECRET = os.getenv('SECRET')
solver = QuizSolver()

@app.route('/quiz', methods=['POST'])
def handle_quiz():
    try:
        data = request.get_json()
    except Exception as e:
        logger.error(f"Invalid JSON: {e}")
        return jsonify({"error": "Invalid JSON"}), 400
    
    if not data or 'secret' not in data:
        return jsonify({"error": "Missing secret"}), 400
    
    if data['secret'] != SECRET:
        logger.warning(f"Invalid secret: {data.get('secret')}")
        return jsonify({"error": "Invalid secret"}), 403
    
    url = data.get('url')
    if not url:
        return jsonify({"error": "Missing url"}), 400
    
    logger.info(f"Received quiz task: {url}")
    
    # Start solving in background thread
    thread = threading.Thread(target=solver.solve_quiz_chain, args=(url, EMAIL, SECRET))
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "processing", "url": url}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
