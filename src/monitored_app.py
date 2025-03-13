from flask import Flask, request, jsonify
import time
import random
import os
import json
import sys

# Import our custom modules
from advanced_logging import AdvancedLogger
from metrics import MetricsCollector

# Create our advanced logger
logger = AdvancedLogger("fintech-app")

# Create metrics collector
metrics = MetricsCollector("fintech-app")

# Define metrics
transaction_counter = metrics.counter("transactions_total", "Total number of transactions processed")
error_counter = metrics.counter("transaction_errors_total", "Total number of transaction errors")
active_requests = metrics.gauge("active_requests", "Number of requests currently being processed")
transaction_duration = metrics.histogram("transaction_duration_seconds", 
                                         [0.1, 0.5, 1.0, 2.0, 5.0], 
                                         "Transaction processing duration in seconds")

app = Flask(__name__)

@app.route('/')
def home():
    logger.info("Home endpoint accessed", user_agent=request.headers.get('User-Agent', 'Unknown'))
    return "Fintech Monitoring Demo"

@app.route('/api/transactions', methods=['POST'])
def process_transaction():
    start_time = time.time()
    active_requests.inc()
    
    try:
        # Simulate transaction processing
        transaction_data = request.json or {}
        transaction_id = random.randint(1000, 9999)
        
        # Log transaction details with metadata
        logger.info(
            f"Processing transaction {transaction_id}",
            transaction_id=transaction_id,
            amount=transaction_data.get('amount'),
            currency=transaction_data.get('currency'),
            user_id=transaction_data.get('user_id')
        )
        
        # Increment transaction counter
        transaction_counter.inc()
        
        # Simulate processing time
        processing_time = random.uniform(0.1, 2.0)
        time.sleep(processing_time)
        
        # Randomly generate errors for testing
        if random.random() < 0.1:  # 10% chance of error
            error_counter.inc()
            logger.error(
                f"Transaction {transaction_id} failed",
                transaction_id=transaction_id,
                error_code="PROC_ERR_001",
                processing_time=processing_time
            )
            return jsonify({"status": "error", "message": "Transaction failed"}), 500
        
        logger.info(
            f"Transaction {transaction_id} completed successfully",
            transaction_id=transaction_id,
            processing_time=processing_time,
            status="success"
        )
        return jsonify({"status": "success", "transaction_id": transaction_id})
    finally:
        # Record processing duration
        duration = time.time() - start_time
        transaction_duration.observe(duration)
        active_requests.dec()

@app.route('/metrics')
def get_metrics():
    # Return metrics in a format similar to Prometheus
    with open(f"metrics/fintech-app_metrics.json", "r") as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        metrics.stop()