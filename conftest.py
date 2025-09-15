import pytest
import pika
import time
from prometheus_client import Summary, Counter, start_http_server

# ----------------------------
# RabbitMQ Fixture
# ----------------------------
@pytest.fixture(scope="function")
def rabbitmq_channel():
    """
    Fixture to create a RabbitMQ channel for tests.
    Handles setup and teardown automatically.
    """
    # Setup: connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Ensure queue exists before tests
    channel.queue_declare(queue="test_queue")

    yield channel  # provide the channel to the test

    # Teardown: close connection
    connection.close()

# Prometheus Metrics
# Metrics
TEST_DURATION = Summary(
    "test_duration_seconds",
    "Duration of each test in seconds",
    ["test_name"]
)
TEST_RETRIES = Counter(
    "test_retries_total",
    "Number of retries during tests"
)

# Start Prometheus metrics server (exposes at http://localhost:8000/metrics)
start_http_server(8000)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    """Measure and export test duration to Prometheus."""
    start = time.time()
    outcome = yield  # run the actual test
    duration = time.time() - start
    TEST_DURATION.labels(test_name=item.name).observe(duration)