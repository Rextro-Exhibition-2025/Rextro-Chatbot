# Stress Testing for Rextro Chatbot

A comprehensive load testing suite for the Rextro Chatbot application using Locust framework.

## 📋 Overview

This project provides automated stress testing capabilities for the Rextro Chatbot deployed at `https://chatbot.internalbuildtools.online`. It simulates concurrent users hitting the health check endpoint to measure performance, response times, and system reliability under load.

## 🚀 Features

- **Health Check Load Testing**: Automated testing of the chatbot's health endpoint
- **Configurable User Load**: Simulate 1-1000+ concurrent users
- **Real-time Monitoring**: Live metrics during test execution
- **Detailed Reporting**: CSV and HTML reports with comprehensive metrics
- **SSL/TLS Support**: Handles HTTPS endpoints with SSL verification options
- **Error Handling**: Robust exception handling and timeout management

## 🛠️ Requirements

- Python 3.13+
- Locust 2.41.5+
- Internet connection to reach the target endpoint

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd stress_testing
   ```

2. **Install dependencies using uv (recommended):**
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Web UI Mode (Recommended for interactive testing)

1. **Start Locust with Web UI:**
   ```bash
   cd locust_test
   locust -f locustfile.py --host=https://chatbot.internalbuildtools.online
   ```

2. **Open your browser to:** `http://localhost:8089`

3. **Configure test parameters:**
   - Number of users: `1000`
   - Spawn rate: `100` users/second
   - Host: `https://chatbot.internalbuildtools.online`

4. **Start the test** and monitor real-time metrics

### Headless Mode (For automated testing)

**Quick 1-minute test:**
```bash
cd locust_test
locust -f locustfile.py --host=https://chatbot.internalbuildtools.online \
       --users 1000 --spawn-rate 100 --run-time 1m --headless
```

**Extended test with reports:**
```bash
cd locust_test
locust -f locustfile.py \
       --host=https://chatbot.internalbuildtools.online \
       --users 1000 \
       --spawn-rate 50 \
       --run-time 2m \
       --html=report.html \
       --csv=results \
       --headless
```

## 📊 Test Configuration

### User Behavior
- **Wait Time**: 1-2 seconds between requests per user
- **Target Endpoint**: `/` (health check)
- **Request Timeout**: 30 seconds
- **SSL Verification**: Disabled for testing (configurable)

### Load Parameters
- **Recommended Users**: 100-1000 concurrent users
- **Spawn Rate**: 50-100 users/second
- **Test Duration**: 1-5 minutes for standard tests

## 📈 Output & Reports

### Console Output
Real-time feedback during test execution:
```
✅ Success: 200, Time: 45ms
❌ Failed: Status 500
📊 Total requests: 15000
✅ Successful: 14850
❌ Failed: 150
```

### Generated Files
- **CSV Reports**: `load_test_results_YYYYMMDD_HHMMSS.csv`
- **HTML Reports**: `report.html` (when using --html flag)
- **Raw CSV Data**: `results_stats.csv`, `results_failures.csv` (when using --csv flag)

### Metrics Tracked
- Response times (min, max, average, percentiles)
- Request rates (RPS)
- Error rates and failure types
- Response sizes
- Concurrent user simulation

## 🔧 Configuration Options

### Command Line Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--users` | Total concurrent users | `--users 1000` |
| `--spawn-rate` | Users added per second | `--spawn-rate 100` |
| `--run-time` | Test duration | `--run-time 5m` |
| `--host` | Target host URL | `--host https://example.com` |
| `--headless` | Run without web UI | `--headless` |
| `--html` | Generate HTML report | `--html=report.html` |
| `--csv` | Save CSV results | `--csv=results` |

### Environment Variables
You can customize the test by modifying variables in `locustfile.py`:
- `wait_time`: Delay between user requests
- `timeout`: Request timeout duration
- `verify`: SSL certificate verification

## 🧪 Test Scenarios

### Basic Health Check
Tests the primary health endpoint with standard HTTP GET requests.

### Load Patterns
1. **Gradual Ramp-up**: Slowly increase users to find breaking point
2. **Spike Testing**: Sudden load increases
3. **Sustained Load**: Constant high traffic over time

## 📁 Project Structure

```
stress_testing/
├── README.md                 # This file
├── main.py                   # Entry point (basic)
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
└── locust_test/
    ├── locustfile.py        # Main Locust test script
    ├── load_test_results_*.csv  # Historical test results
    └── __pycache__/         # Python cache files
```

## 🔍 Troubleshooting

### Common Issues

**Connection Timeouts:**
- Increase timeout values in `locustfile.py`
- Check network connectivity to target host

**SSL Certificate Errors:**
- SSL verification is disabled by default for testing
- Enable verification by setting `self.client.verify = True`

**High Error Rates:**
- Reduce spawn rate to allow gradual scaling
- Check target server capacity and logs

**Memory Issues:**
- Reduce number of concurrent users
- Increase test machine resources

### Debug Mode
Add verbose logging by modifying the locustfile.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Best Practices

1. **Start Small**: Begin with 10-50 users, then scale up
2. **Monitor Target**: Watch server metrics during tests
3. **Gradual Scaling**: Use appropriate spawn rates (10-100 users/sec)
4. **Test Duration**: Run tests for sufficient time (2-5 minutes minimum)
5. **Regular Testing**: Integrate into CI/CD pipeline for regression testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Rextro Exhibition 2025 initiative.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review Locust documentation: https://docs.locust.io/
- Create an issue in the repository

---

**⚡ Happy Load Testing!** 🚀
