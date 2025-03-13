import time
import threading
import json
import os

class MetricsCollector:
       def __init__(self, app_name, metrics_dir="metrics"):
           self.app_name = app_name
           self.metrics_dir = metrics_dir
           self.metrics = {
               "counters": {},
               "gauges": {},
               "histograms": {}
           }
           self.lock = threading.Lock()
           
           # Create metrics directory
           os.makedirs(metrics_dir, exist_ok=True)
           
           # Start background thread to save metrics periodically
           self.running = True
           self.bg_thread = threading.Thread(target=self._background_save)
           self.bg_thread.daemon = True
           self.bg_thread.start()
       
       def counter(self, name, description=""):
           """Create a counter metric"""
           with self.lock:
               if name not in self.metrics["counters"]:
                   self.metrics["counters"][name] = {
                       "value": 0,
                       "description": description
                   }
           return Counter(self, name)
       
       def gauge(self, name, description=""):
           """Create a gauge metric"""
           with self.lock:
               if name not in self.metrics["gauges"]:
                   self.metrics["gauges"][name] = {
                       "value": 0,
                       "description": description
                   }
           return Gauge(self, name)
       
       def histogram(self, name, buckets=[0.1, 0.5, 1.0, 2.0, 5.0], description=""):
           """Create a histogram metric"""
           with self.lock:
               if name not in self.metrics["histograms"]:
                   self.metrics["histograms"][name] = {
                       "count": 0,
                       "sum": 0,
                       "buckets": {str(b): 0 for b in buckets},
                       "description": description
                   }
           return Histogram(self, name)
       
       def _background_save(self):
           """Save metrics to disk periodically"""
           while self.running:
               with self.lock:
                   with open(f"{self.metrics_dir}/{self.app_name}_metrics.json", "w") as f:
                       json.dump(self.metrics, f, indent=2)
               time.sleep(10)  # Save every 10 seconds
       
       def stop(self):
           """Stop the background thread"""
           self.running = False
           self.bg_thread.join()
           
class Counter:
    def __init__(self, collector, name):
        self.collector = collector
        self.name = name
    
    def inc(self, value=1):
        with self.collector.lock:
            self.collector.metrics["counters"][self.name]["value"] += value

class Gauge:
    def __init__(self, collector, name):
        self.collector = collector
        self.name = name
    
    def set(self, value):
        with self.collector.lock:
            self.collector.metrics["gauges"][self.name]["value"] = value
    
    def inc(self, value=1):
        with self.collector.lock:
            self.collector.metrics["gauges"][self.name]["value"] += value
    
    def dec(self, value=1):
        with self.collector.lock:
            self.collector.metrics["gauges"][self.name]["value"] -= value

class Histogram:
    def __init__(self, collector, name):
        self.collector = collector
        self.name = name
    
    def observe(self, value):
        with self.collector.lock:
            metrics = self.collector.metrics["histograms"][self.name]
            metrics["count"] += 1
            metrics["sum"] += value
            
            # Update buckets
            for bucket in metrics["buckets"]:
                if value <= float(bucket):
                    metrics["buckets"][bucket] += 1