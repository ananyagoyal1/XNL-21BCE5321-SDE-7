import json
import matplotlib
# Set the backend to Agg (non-interactive)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import os
import sys

def create_dashboard(metrics_file, output_dir="dashboards"):
    """Create visualizations of metrics data"""
    print(f"Creating dashboard from metrics file: {metrics_file}")
    print(f"Output directory: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load metrics data
    try:
        print(f"Attempting to open metrics file...")
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
        print(f"Successfully loaded metrics data")
        print(f"Metrics content: {json.dumps(metrics, indent=2)}")
    except FileNotFoundError:
        print(f"Error: Metrics file {metrics_file} not found")
        return
    except json.JSONDecodeError:
        print(f"Error: Metrics file {metrics_file} contains invalid JSON")
        return
    
    # Create timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    print(f"Using timestamp: {timestamp}")
    
    # Plot counters
    if "counters" in metrics and metrics["counters"]:
        print(f"Generating counter plots...")
        plt.figure(figsize=(10, 6))
        counter_names = list(metrics["counters"].keys())
        counter_values = [metrics["counters"][name]["value"] for name in counter_names]
        
        plt.bar(counter_names, counter_values)
        plt.title("Counters")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        counter_file = f"{output_dir}/counters_{timestamp}.png"
        print(f"Saving counter plot to: {counter_file}")
        plt.savefig(counter_file)
        plt.close()
        
        # Verify file was created
        if os.path.exists(counter_file):
            print(f"Successfully created counter plot: {counter_file}")
            print(f"File size: {os.path.getsize(counter_file)} bytes")
        else:
            print(f"ERROR: Failed to create counter plot!")
    else:
        print("No counters found in metrics data")
    
    # Plot gauges
    if "gauges" in metrics and metrics["gauges"]:
        print(f"Generating gauge plots...")
        plt.figure(figsize=(10, 6))
        gauge_names = list(metrics["gauges"].keys())
        gauge_values = [metrics["gauges"][name]["value"] for name in gauge_names]
        
        plt.bar(gauge_names, gauge_values)
        plt.title("Gauges")
        plt.ylabel("Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        gauge_file = f"{output_dir}/gauges_{timestamp}.png"
        print(f"Saving gauge plot to: {gauge_file}")
        plt.savefig(gauge_file)
        plt.close()
        
        # Verify file was created
        if os.path.exists(gauge_file):
            print(f"Successfully created gauge plot: {gauge_file}")
            print(f"File size: {os.path.getsize(gauge_file)} bytes")
        else:
            print(f"ERROR: Failed to create gauge plot!")
    else:
        print("No gauges found in metrics data")
    
    # Plot histograms
    if "histograms" in metrics and metrics["histograms"]:
        for name, hist in metrics["histograms"].items():
            print(f"Generating histogram plot for: {name}")
            plt.figure(figsize=(10, 6))
            bucket_names = list(hist["buckets"].keys())
            bucket_values = list(hist["buckets"].values())
            
            plt.bar(bucket_names, bucket_values)
            plt.title(f"Histogram: {name}")
            plt.xlabel("Bucket")
            plt.ylabel("Count")
            plt.tight_layout()
            
            hist_file = f"{output_dir}/histogram_{name}_{timestamp}.png"
            print(f"Saving histogram plot to: {hist_file}")
            plt.savefig(hist_file)
            plt.close()
            
            # Verify file was created
            if os.path.exists(hist_file):
                print(f"Successfully created histogram plot: {hist_file}")
                print(f"File size: {os.path.getsize(hist_file)} bytes")
            else:
                print(f"ERROR: Failed to create histogram plot!")
    else:
        print("No histograms found in metrics data")
    
    print(f"Dashboard visualizations saved to {output_dir}/")
    
    # List all files in the output directory
    print("Files in output directory:")
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        print(f"  - {file} ({os.path.getsize(file_path)} bytes)")

if __name__ == "__main__":
    # Use absolute path to find metrics file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    metrics_path = os.path.join(base_dir, "metrics", "fintech-app_metrics.json")
    dashboards_dir = os.path.join(base_dir, "dashboards")
    
    print(f"Script directory: {script_dir}")
    print(f"Base directory: {base_dir}")
    print(f"Metrics path: {metrics_path}")
    print(f"Dashboards directory: {dashboards_dir}")
    
    # Check if file exists
    if not os.path.exists(metrics_path):
        print(f"Metrics file not found at: {metrics_path}")
        print("Creating sample metrics file for testing...")
        
        # Create metrics directory if it doesn't exist
        os.makedirs(os.path.join(base_dir, "metrics"), exist_ok=True)
        
        # Create sample metrics data
        sample_metrics = {
            "counters": {
                "transactions_total": {"value": 50, "description": "Total number of transactions processed"},
                "transaction_errors_total": {"value": 5, "description": "Total number of transaction errors"}
            },
            "gauges": {
                "active_requests": {"value": 0, "description": "Number of requests currently being processed"}
            },
            "histograms": {
                "transaction_duration_seconds": {
                    "count": 50,
                    "sum": 45.2,
                    "buckets": {"0.1": 5, "0.5": 15, "1.0": 20, "2.0": 8, "5.0": 2},
                    "description": "Transaction processing duration in seconds"
                }
            }
        }
        
        # Write sample metrics to file
        with open(metrics_path, "w") as f:
            json.dump(sample_metrics, f, indent=2)
        
        print(f"Sample metrics file created at: {metrics_path}")
    
    # Create dashboard using the metrics file
    create_dashboard(metrics_path, dashboards_dir)