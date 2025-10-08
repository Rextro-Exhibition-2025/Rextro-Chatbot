from locust import HttpUser, task, between, events
import time
import csv
import os
from datetime import datetime
import ssl

class HealthCheckUser(HttpUser):
    """
    Simulates a user hitting the health check endpoint.
    
    wait_time: Time between requests (1-2 seconds per user)
    """
    wait_time = between(1, 2)
    
    def on_start(self):
        """Called when a user starts. Configure client settings."""
        # Set connection timeout and disable SSL verification for testing
        self.client.timeout = 30  # 30 seconds timeout
        self.client.verify = False  # Disable SSL verification for testing
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    @task
    def health_check(self):
        """
        Task: Hit the health check endpoint
        Weight: 1 (100% of requests go here)
        """
        start_time = time.time()
        try:
            with self.client.get(
                "/",
                catch_response=True,
                name="Health Check",
                timeout=30  # Explicit timeout for this request
            ) as response:
                response_time = (time.time() - start_time) * 1000  # ms
                
                if response.status_code == 200:
                    response.success()
                    print(f"✅ Success: {response.status_code}, Time: {response_time:.0f}ms")
                else:
                    response.failure(f"Got status code: {response.status_code}")
                    print(f"❌ Failed: Status {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Request failed with exception: {e}")
            # Log the actual exception for debugging


# --- Event Handlers for Custom Metrics ---
results = []

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Capture each request for detailed analysis"""
    results.append({
        'timestamp': datetime.now(),
        'request_type': request_type,
        'name': name,
        'response_time': response_time,
        'response_length': response_length,
        'exception': str(exception) if exception else None,
        'success': exception is None
    })

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Save results to CSV after test completes"""
    if results:
        filename = f'load_test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✅ Results saved to: {filename}")
        print(f"📊 Total requests: {len(results)}")
        print(f"✅ Successful: {sum(1 for r in results if r['success'])}")
        print(f"❌ Failed: {sum(1 for r in results if not r['success'])}")


# --- Configuration Guide ---
"""
HOW TO RUN:

1. Basic Test (Web UI):
   locust -f locustfile.py --host=https://chatbot.internalbuildtools.online

   Then open: http://localhost:8089
   Set: 1000 users, Spawn rate: 100 users/second

2. Headless Mode (No UI):
   locust -f locustfile.py --host=https://chatbot.internalbuildtools.online \
          --users 1000 --spawn-rate 100 --run-time 1m --headless

3. Advanced Options:
   locust -f locustfile.py \
          --host=https://chatbot.internalbuildtools.online \
   Then open: http://localhost:8089
   Set: 1000 users, Spawn rate: 100 users/second

2. Headless Mode (No UI):
   locust -f locustfile.py --host=https://chatbot.internalbuildtools.online \
          --users 1000 --spawn-rate 100 --run-time 1m --headless

3. Advanced Options:
   locust -f locustfile.py \
          --host=https://chatbot.internalbuildtools.online \
          --users 1000 \
          --spawn-rate 50 \
          --run-time 2m \
          --html=report.html \
          --csv=results \
          --headless

PARAMETERS EXPLAINED:
- --users: Total number of concurrent users (1000)
- --spawn-rate: How many users to add per second (50-100)
- --run-time: How long to run the test (1m, 30s, etc.)
- --headless: Run without web UI
- --html: Generate HTML report
- --csv: Save results to CSV
"""