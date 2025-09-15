import pytest #Framework to run tests
import requests #To make HTTP requests
import json #Tests needs to interact with JSON Data
import base64 # for Utilities 
import time # for Utilities
from config import Config  # Contains configuration like BASE_URL
from custom_decorators import retry # custom decorator to retry failed test cases
from test_utils import generate_random_user_data, generate_random_string # Helper functions for test data

# Base URL for the API from the configuration file
BASE_URL = Config.BASE_URL #Get the base API endpoint("https://httpbin.org")
#this is pulled from config.py, So the URL can be changed w/o editing test files

# Allure decorators for reporting
from allure import epic, feature, story, title, step

@epic("HTTPBin API Testing")
@feature("Response Formats")
class TestResponseFormats:
    """
    Tests for various response formats returned by httpbin.org.
    """
    @story("JSON Response")
    @title("Test GET /json endpoint")
    def test_get_json_response(self):
        """
        Tests the /json endpoint to ensure it returns a valid JSON response with the expected keys.
        """
        with step("Send GET request to /json"):
            response = requests.get(f"{BASE_URL}/json")

        with step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        with step("Verify content type is application/json"):
            assert 'application/json' in response.headers.get('Content-Type'), "Content-Type is not application/json"

        with step("Verify response body contains expected keys"):
            try:
                json_data = response.json()
                assert "slideshow" in json_data, "Response body does not contain 'slideshow' key"
            except json.JSONDecodeError:
                pytest.fail("Failed to decode JSON response")

    @story("HTML Response")
    @title("Test GET /html endpoint")
    def test_get_html_response(self):
        """
        Tests the /html endpoint to ensure it returns a valid HTML response.
        """
        with step("Send GET request to /html"):
            response = requests.get(f"{BASE_URL}/html")
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            
        with step("Verify content type is text/html"):
            assert 'text/html' in response.headers.get('Content-Type'), "Content-Type is not text/html"
            
        with step("Verify response body contains expected HTML tag"):
            assert "<h1>Herman Melville - Moby-Dick</h1>" in response.text, "HTML body does not contain expected header"

    @story("XML Response")
    @title("Test GET /xml endpoint")
    def test_get_xml_response(self):
        """
        Tests the /xml endpoint to ensure it returns a valid XML response.
        """
        with step("Send GET request to /xml"):
            response = requests.get(f"{BASE_URL}/xml")
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            
        with step("Verify content type is application/xml"):
            assert 'application/xml' in response.headers.get('Content-Type'), "Content-Type is not application/xml"
            
        with step("Verify response body contains expected XML tags"):
            assert "<slideshow" in response.text, "XML body does not contain <slideshow> tag"

    @story("Plain Text Response (robots.txt)")
    @title("Test GET /robots.txt endpoint")
    def test_get_robots_txt_response(self):
        """
        Tests the /robots.txt endpoint to ensure it returns plain text.
        """
        with step("Send GET request to /robots.txt"):
            response = requests.get(f"{BASE_URL}/robots.txt")

        with step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            
        with step("Verify content type is text/plain"):
            assert 'text/plain' in response.headers.get('Content-Type'), "Content-Type is not text/plain"
            
        with step("Verify response body content"):
            assert "User-agent: *" in response.text and "Disallow: /deny" in response.text, "robots.txt content is not as expected"

    @story("Brotli Encoded Response")
    @title("Test GET /brotli endpoint")
    def test_get_brotli_response(self):
        """
        Tests the /brotli endpoint to ensure it returns a valid brotli-encoded response.
        """
        with step("Send GET request to /brotli"):
            response = requests.get(f"{BASE_URL}/brotli")

        with step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            
        with step("Verify content encoding is br"):
            assert 'br' in response.headers.get('Content-Encoding'), "Content-Encoding is not 'br'"
            
    @story("Deflate Encoded Response")
    @title("Test GET /deflate endpoint")
    def test_get_deflate_response(self):
        """
        Tests the /deflate endpoint to ensure it returns a valid deflate-encoded response.
        """
        with step("Send GET request to /deflate"):
            response = requests.get(f"{BASE_URL}/deflate")

        with step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
            
        with step("Verify content encoding is deflate"):
            assert 'deflate' in response.headers.get('Content-Encoding'), "Content-Encoding is not 'deflate'"

@epic("HTTPBin API Testing")
@feature("Request Inspection")
class TestRequestInspection:
    """
    Tests for endpoints that inspect and return details about the incoming request.
    """
    @story("IP Address Inspection")
    @title("Test GET /ip endpoint")
    def test_get_ip_address(self):
        """
        Tests the /ip endpoint to verify it returns a valid IP address.
        """
        with step("Send GET request to /ip"):
            response = requests.get(f"{BASE_URL}/ip")

        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /ip"

        with step("Verify response body contains a valid IP address"):
            data = response.json()
            assert "origin" in data and len(data["origin"]) > 0, "IP address not found or is empty"

    @story("Headers Inspection")
    @title("Test GET /headers endpoint")
    def test_get_headers(self):
        """
        Tests the /headers endpoint to verify it returns the sent headers.
        """
        custom_header = {"X-Custom-Header": "TestValue"}
        
        with step("Send GET request to /headers with custom headers"):
            response = requests.get(f"{BASE_URL}/headers", headers=custom_header)
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /headers"

        with step("Verify response body contains the sent custom header"):
            data = response.json()
            assert "X-Custom-Header" in data["headers"], "Custom header not found in the response"
            assert data["headers"]["X-Custom-Header"] == "TestValue", "Custom header value is incorrect"

    @story("User-Agent Inspection")
    @title("Test GET /user-agent endpoint")
    def test_get_user_agent(self):
        """
        Tests the /user-agent endpoint to verify it returns a user-agent header.
        """
        user_agent_value = "MyTestClient/1.0"
        headers = {"User-Agent": user_agent_value}

        with step("Send GET request to /user-agent with a custom User-Agent"):
            response = requests.get(f"{BASE_URL}/user-agent", headers=headers)
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /user-agent"
            
        with step("Verify response body contains the correct User-Agent"):
            data = response.json()
            assert "user-agent" in data, "user-agent key not found in the response"
            assert data["user-agent"] == user_agent_value, "User-Agent value is incorrect"

@epic("HTTPBin API Testing")
@feature("Dynamic Data & Behavior")
class TestDynamicData:
    """
    Tests for endpoints that generate random/dynamic data or have dynamic behavior.
    """
    @story("Base64 Decoding")
    @title("Test GET /base64/{value} endpoint")
    def test_base64_decoding(self):
        """
        Tests the /base64 endpoint by encoding a string and validating the decoded result.
        """
        original_string = generate_random_string()
        encoded_string = base64.b64encode(original_string.encode()).decode()
        
        with step("Send GET request to /base64 with encoded string"):
            response = requests.get(f"{BASE_URL}/base64/{encoded_string}")
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /base64"
        
        with step("Verify decoded response matches original string"):
            assert response.text == original_string, "Decoded string does not match original"

    @story("Delayed Response")
    @title("Test GET /delay/{delay} endpoint")
    @retry(max_attempts=Config.RETRY_ATTEMPTS, delay_seconds=Config.RETRY_DELAY_SECONDS)
    def test_get_delay_endpoint(self):
        """
        Tests the /delay endpoint with a specified delay. This test is flaky and uses the retry decorator.
        """
        delay = 3
        
        with step(f"Send GET request to /delay with a {delay}s delay"):
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/delay/{delay}")
            end_time = time.time()
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /delay"
        
        with step(f"Verify request took at least {delay} seconds"):
            duration = end_time - start_time
            assert duration >= delay, f"Request took {duration:.2f}s, less than expected {delay}s"

    @story("Delayed Response - POST method")
    @title("Test POST /delay/{delay} endpoint")
    @retry(max_attempts=Config.RETRY_ATTEMPTS, delay_seconds=Config.RETRY_DELAY_SECONDS)
    def test_post_delay_endpoint(self):
        """
        Tests the /delay endpoint with a POST request.
        """
        delay = 2
        payload = generate_random_user_data()
        
        with step(f"Send POST request to /delay with a {delay}s delay"):
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/delay/{delay}", json=payload)
            end_time = time.time()
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /delay"
        
        with step(f"Verify request took at least {delay} seconds"):
            duration = end_time - start_time
            assert duration >= delay, f"Request took {duration:.2f}s, less than expected {delay}s"

    @story("Delayed Response - DELETE method")
    @title("Test DELETE /delay/{delay} endpoint")
    @retry(max_attempts=Config.RETRY_ATTEMPTS, delay_seconds=Config.RETRY_DELAY_SECONDS)
    def test_delete_delay_endpoint(self):
        """
        Tests the /delay endpoint with a DELETE request.
        """
        delay = 2
        
        with step(f"Send DELETE request to /delay with a {delay}s delay"):
            start_time = time.time()
            response = requests.delete(f"{BASE_URL}/delay/{delay}")
            end_time = time.time()
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /delay"
        
        with step(f"Verify request took at least {delay} seconds"):
            duration = end_time - start_time
            assert duration >= delay, f"Request took {duration:.2f}s, less than expected {delay}s"

    @story("Links Generation")
    @title("Test GET /links/{n}/{offset} endpoint")
    def test_links_generation(self):
        """
        Tests the /links endpoint to ensure it returns the correct number of links.
        """
        with step("Send GET request to /links/10/0"):
            response = requests.get(f"{BASE_URL}/links/10/0")
        
        with step("Verify response status code is 200"):
            assert response.status_code == 200, "Failed to get a 200 response from /links"
        
        with step("Count the number of links in the response"):
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
        
        with step("Verify the correct number of links were returned"):
            assert len(links) >= 9, f"Expected at least 9 links, but got {len(links)}"
