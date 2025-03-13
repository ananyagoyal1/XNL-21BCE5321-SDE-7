import requests
import time
import random
import threading
import json
import os
from datetime import datetime

def generate_transaction():
    """Generate a random transaction"""
    return {
        "user_id": random.randint(1000, 9999),
        "amount": round(random.uniform(10, 1000), 2),
        "currency": random.choice(["USD", "EUR", "GBP", "JPY"]),
        "type": random.choice(["payment", "transfer", "deposit", "withdrawal"]),
        "description": "Test transaction"
    }

def send_transactions(server_url, num_transactions, results_file, thread_id):
    """Send a batch of transactions and record results"""
    results = []
    
    for i in range(num_transactions):
        transaction = generate_transaction()
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{server_url}/api/transactions",
                json=transaction,
                headers={"Content-Type": "application/json"}
            )
            
            duration = time.time() - start_time
            status = response.status_code
            success = 200 <= status < 300
            
            results.append({
                "transaction_id": i,
                "thread_id": thread_id,
                "duration": duration,
                "status_code": status,
                "success": success,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            results.append({
                "transaction_id": i,
                "thread_id": thread_id,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            })
        
        # Random delay between requests
        time.sleep(random.uniform(0.1, 0.5))
    
    # Save results to file
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

def run_load_test(server_url="http://localhost:5000", 
                 num_threads=5, 
                 transactions_per_thread=20):
    """Run a multi-threaded load test"""
    os.makedirs("load_tests/results", exist_ok=True)
    
    threads = []
    for i in range(num_threads):
        results_file = f"load_tests/results/thread_{i}_results.json"
        thread = threading.Thread(
            target=send_transactions,
            args=(server_url, transactions_per_thread, results_file, i)
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Aggregate results
    aggregate_results(num_threads)

def aggregate_results(num_threads):
    """Aggregate results from all threads"""
    all_results = []
    
    for i in range(num_threads):
        try:
            with open(f"load_tests/results/thread_{i}_results.json", 'r') as f:
                thread_results = json.load(f)
                all_results.extend(thread_results)
        except:
            print(f"Error reading results from thread {i}")
    
    # Calculate statistics
    durations = [r.get('duration', 0) for r in all_results if 'duration' in r]
    success_count = sum(1 for r in all_results if r.get('success', False))
    
    if durations:
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)
    else:
        avg_duration = max_duration = min_duration = 0
    
    # Save summary
    summary = {
        "total_transactions": len(all_results),
        "successful_transactions": success_count,
        "success_rate": success_count / len(all_results) if all_results else 0,
        "avg_duration": avg_duration,
        "max_duration": max_duration,
        "min_duration": min_duration,
        "timestamp": datetime.now().isoformat()
    }
    
    with open("load_tests/results/summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("Load test completed!")
    print(f"Total transactions: {len(all_results)}")
    print(f"Success rate: {summary['success_rate']:.2%}")
    print(f"Average duration: {avg_duration:.4f}s")

if __name__ == "__main__":
    run_load_test()