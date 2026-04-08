from prometheus_client import (
    Counter, Gauge, Summary, Histogram, Info, Enum,
    CollectorRegistry, start_http_server, Metric,
    REGISTRY
)
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
import time
import random
import threading

# 1. Counter
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

# 2. Gauge
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

# 3. Summary
request_latency = Summary(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

# 4. Histogram
response_time = Histogram(
    'response_time_seconds',
    'Response time in seconds',
    ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, float('inf')]
)

# 5. Info
app_info = Info('app', 'Application information')
app_info.info({
    'version': '1.0.0',
    'language': 'python',
    'framework': 'prometheus_client'
})

# 6. Enum
app_state = Enum(
    'app_state',
    'Current application state',
    states=['starting', 'running', 'degraded', 'stopped']
)
app_state.state('running')

# 7. Counter with Labels
error_total = Counter(
    'errors_total',
    'Total errors by type',
    ['error_type', 'severity']
)

# 8. Histogram with Exemplars
request_duration = Histogram(
    'request_duration_seconds',
    'Request duration with exemplars'
)

# 9. Custom Collector
class DatabaseCollector:
    def collect(self):
        connections = GaugeMetricFamily(
            'db_connections',
            'Database connections',
            labels=['state']
        )
        connections.add_metric(['active'], random.randint(1, 50))
        connections.add_metric(['idle'], random.randint(0, 10))
        yield connections

        queries = CounterMetricFamily(
            'db_queries_total',
            'Total database queries',
            labels=['type']
        )
        queries.add_metric(['select'], random.randint(100, 10000))
        queries.add_metric(['insert'], random.randint(10, 1000))
        yield queries

REGISTRY.register(DatabaseCollector())

# 10. Gauge with callback
cpu_usage = Gauge('cpu_usage_percent', 'Simulated CPU usage')
cpu_usage.set_function(lambda: random.uniform(10.0, 90.0))


def simulate_traffic():
    """Background thread to generate metric data."""
    while True:
        # Counter
        method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
        endpoint = random.choice(['/api/users', '/api/orders', '/api/products'])
        http_requests_total.labels(method=method, endpoint=endpoint).inc()

        # Gauge
        active_connections.set(random.randint(1, 100))

        # Summary with labels
        request_latency.labels(endpoint=endpoint).observe(random.uniform(0.01, 2.0))

        # Histogram with labels
        response_time.labels(endpoint=endpoint).observe(random.uniform(0.01, 5.0))

        # Counter with labels
        error_type = random.choice(['timeout', 'connection', 'validation', 'auth'])
        severity = random.choice(['low', 'medium', 'high'])
        error_total.labels(error_type=error_type, severity=severity).inc()

        # Histogram with exemplars
        trace_id = f"trace-{random.randint(1000, 9999)}"
        request_duration.observe(
            random.uniform(0.1, 3.0),
            exemplar={'trace_id': trace_id}
        )

        # Enum state changes
        if random.random() < 0.05:
            app_state.state(random.choice(['running', 'degraded']))

        time.sleep(2)


if __name__ == '__main__':
    print("Starting metrics server on port 8000...")
    start_http_server(8000)
    print("Metrics available at http://localhost:8000/metrics")

    traffic_thread = threading.Thread(target=simulate_traffic, daemon=True)
    traffic_thread.start()

    while True:
        time.sleep(1)
