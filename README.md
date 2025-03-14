# Real-time system for debugging, logging, and performance monitoring

   For a fintech application, this project puts in place a thorough real-time performance monitoring, logging, and debugging system. The system facilitates quick problem solving, allows debugging under high load, and offers actionable insights.

   ## Architecture of the System

   Several essential parts make up the monitoring system:

   1. **Advanced Logging Infrastructure**: - Structured JSON output and multi-level logging
      Rotation of logs and long-term storage
      Error logs are separated for speedy problem identification.

  2. **Real-Time Performance Monitoring**:   - Transaction counters, error rates, and processing duration histograms - Prometheus-like custom metrics collection
      Metric visualization using dashboards that are generated

3. **Load Testing Framework**: which includes: - JSON output of performance results - Configurable user count and test duration - Simulation of user behavior and transaction processing

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

   ### More Complex Logging

   - **Structured JSON Logs**: All logs are formatted as JSON for seamless analysis and parsing - **Log Rotation**: Keeps logs from taking up excessive disk space - **Log Levels**: Various log levels (INFO, ERROR, etc.) for improved filtering - **Contextual Information**: Every log entry contains pertinent metadata

   ### Gathering Metrics

   **Counters**: Monitor total transactions and other cumulative values; **Gauges**: Monitor values that fluctuate, such as active requests; **Histograms**: Monitor value distributions, such as transaction duration

   ### Testing for Loads

   Realistic User Simulation: This uses random transaction data to simulate real user behavior. Multi-threaded Testing: This simulates multiple users accessing the system at once. Performance Metrics: Record response times, error rates, and throughput.

### Visual Aids

   **Metrics Dashboards**: An illustration of every metric that has been gathered
   **Histogram Analysis**: Show how transaction processing times are distributed

   - **Time-stamped Reports**: Timestamps are appended to dashboard photos for future reference.

   ## Techniques for Debugging

   1. **Log Analysis**: - To swiftly detect problems, use the structured JSON logs.
      Use the specific error log file to filter errors.
      Utilize the transaction_id to track transactions across log entries.

   2. **Identifying Performance Bottlenecks**: - Examine histogram data to find slow transactions - Examine error rates in relation to transaction volume - Keep an eye on active requests to spot possible overload

   3. **Insights from Load Testing**: Examine load test results to find any breaking points.
      Examine how response time deteriorates under load and look for error patterns that appear only under stress.


