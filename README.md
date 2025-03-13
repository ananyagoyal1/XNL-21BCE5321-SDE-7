 # Real-Time Performance Monitoring, Logging & Debugging System

   This project implements a comprehensive real-time performance monitoring, logging, and debugging system for a fintech application. The system provides actionable insights, enables debugging under heavy load, and supports rapid issue resolution.

   ## System Architecture

   The monitoring system consists of several key components:

   1. **Advanced Logging Infrastructure**:
      - Multi-level logging with structured JSON output
      - Log rotation and persistent storage
      - Separation of error logs for quick issue identification

   2. **Real-Time Performance Monitoring**:
      - Custom metrics collection similar to Prometheus
      - Transaction counters, error rates, and processing duration histograms
      - Visualization of metrics through generated dashboards

   3. **Load Testing Framework**:
      - Simulation of user behavior and transaction processing
      - Configurable user count and test duration
      - JSON output of performance results

   ## Project Structure
   /
   ├── src/
   │   ├── app.py                    # Basic Flask application
   │   ├── advanced_logging.py       # Advanced logging infrastructure
   │   ├── metrics.py                # Metrics collection system
   │   ├── monitored_app.py          # App with logging and metrics
   │   ├── dashboard.py              # Dashboard generation script
   │   └── simulate_load.py          # Load simulation script
   ├── load_tests/
   │   └── results/                  # Load test result files
   ├── logs/                         # Application logs
   ├── metrics/                      # Collected metrics data
   ├── dashboards/                   # Generated dashboard visualizations
   └── README.md                     # Project documentation
   ## Setup and Installation

   1. Clone the repository:
      git clone https://github.com/yourusername/XNL-21BCE5321-SDE-7.git
      cd XNL-21BCE5321-SDE-7
   2. Set up virtual environment:
      # For Windows
      python -m venv venv
      venv\Scripts\activate

      # For macOS/Linux
      python -m venv venv
      source venv/bin/activate
   3. Install dependencies:
      pip install flask matplotlib requests
   ## Running the Application

   1. Start the monitored application:
      python src/monitored_app.py
   2. In a separate terminal, run the load simulation:
      python src/simulate_load.py
   3. Generate dashboards from collected metrics:
      python src/dashboard.py
   ## Features

   ### Advanced Logging

   - **Structured JSON Logs**: All logs are formatted as JSON for easy parsing and analysis
   - **Log Rotation**: Prevents logs from consuming too much disk space
   - **Log Levels**: Different log levels (INFO, ERROR, etc.) for better filtering
   - **Contextual Information**: Each log entry includes relevant metadata

   ### Metrics Collection

   - **Counters**: Track cumulative values like total transactions
   - **Gauges**: Track values that can go up and down like active requests
   - **Histograms**: Track distributions of values like transaction duration

   ### Load Testing

   - **Realistic User Simulation**: Simulates real user behavior with random transaction data
   - **Multi-threaded Testing**: Simulates concurrent users accessing the system
   - **Performance Metrics**: Captures response times, error rates, and throughput

   ### Visualization

   - **Metrics Dashboards**: Visual representation of all collected metrics
   - **Histogram Analysis**: Visualize distribution of transaction processing times
   - **Time-stamped Reports**: Dashboard images are saved with timestamps for historical comparison

   ## Debugging Strategies

   1. **Log Analysis**:
      - Use the structured JSON logs to quickly identify issues
      - Filter errors using the dedicated error log file
      - Trace transactions using the transaction_id across log entries

   2. **Performance Bottleneck Identification**:
      - Analyze histogram data to identify slow transactions
      - Compare error rates with transaction volume
      - Monitor active requests to detect potential overload

   3. **Load Testing Insights**:
      - Review load test results to identify breaking points
      - Analyze response time degradation under load
      - Identify error patterns that emerge only under stress
