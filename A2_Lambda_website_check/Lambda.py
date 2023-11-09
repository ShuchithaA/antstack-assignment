import json
import http.client
from urllib.parse import urlparse
import socket

def lambda_handler(event, context):
    try:
        print("event", event)
    # Extract the website URL from the query parameters in the event
        website_url = event.get("queryStringParameters", {}).get("website_url", '')
        print(website_url)
        if not website_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing website_url parameter"})
            }

        # Ensure the URL has the 'http://' or 'https://' prefix
        if not website_url.startswith("http://") and not website_url.startswith("https://"):
            website_url = "https://" + website_url

        # Parse the URL to separate components
        parsed_url = urlparse(website_url)
        print(website_url)

        # Check if the port is specified in the URL
        if ":" in parsed_url.netloc:
            hostname, port = parsed_url.netloc.split(":")
            port = int(port)
        else:
            hostname = parsed_url.netloc
            port = 443  # Default to HTTPS port (443)

    
        # Attempt to establish an HTTPS connection
        conn = http.client.HTTPSConnection(hostname, port=port)
        conn.request("GET", parsed_url.path)
        response = conn.getresponse()

        if response.status == 200:
            website_is_healthy=True
            return {
                
                "statusCode": 200,
                "body": json.dumps({"message": "Website is healthy"})
            }
        else:
            return {
                "statusCode": response.status,
                "body": json.dumps({"message": f"Website is not healthy (HTTP {response.status})"})
            }
        
    except socket.gaierror as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Website doesn't exist "})
        }
    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid URL format"})
        }
