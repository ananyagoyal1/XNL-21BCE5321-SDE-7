import logging
import time
import random
import os
from flask import Flask, request, jsonify

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    logger.info("Home endpoint accessed")
    return "Fintech Monitoring Demo"

@app.route('/api/transactions', methods=['POST'])
def process_transaction():
    # Simulate transaction processing
    transaction_data = request.json
    transaction_id = random.randint(1000, 9999)
    
    # Log transaction details
    logger.info(f"Processing transaction {transaction_id}: {transaction_data}")
    
    # Simulate processing time
    processing_time = random.uniform(0.1, 2.0)
    time.sleep(processing_time)
    
    # Randomly generate errors for testing
    if random.random() < 0.1:  # 10% chance of error
        logger.error(f"Transaction {transaction_id} failed")
        return jsonify({"status": "error", "message": "Transaction failed"}), 500
    
    logger.info(f"Transaction {transaction_id} completed successfully in {processing_time:.2f}s")
    return jsonify({"status": "success", "transaction_id": transaction_id})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)