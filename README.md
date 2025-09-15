# HTTPbin Pytest API Framework

A Python-based API automation framework using **pytest** to test HTTPbin endpoints. This framework supports generating HTML reports and can integrate with RabbitMQ for messaging tests.

---

## 🛠 Prerequisites

- Python 3.8+
- pip
- Docker (if using RabbitMQ)
- RabbitMQ (for messaging tests)

Install required Python packages:

```bash
pip install -r requirements.txt
=======================================================================================
⚡ Features

API testing using pytest

HTML test reports

RabbitMQ integration for messaging tests

Easy configuration and setup

CI/CD friendly

🚀 Running Tests

Run all tests and generate HTML report:

pytest --maxfail=1 --disable-warnings -q --html=reports/report.html

Open the report:

reports/report.html

🔹 Running RabbitMQ Tests

Start RabbitMQ (using Docker):

docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management


Access management UI at http://localhost:15672

Username: guest, Password: guest

Then run the tests.

📁 Project Structure
HTTPbin_Pytest_API_Framework/
│
├── tests/                  # All API test cases
├── conftest.py             # Fixtures
├── requirements.txt        # Python dependencies
├── reports/                # Generated test reports
└── README.md               # Project documentation


