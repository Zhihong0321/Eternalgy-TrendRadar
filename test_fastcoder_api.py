import requests
import json

# API Configuration
BASE_URL = "https://api.fastcoder.my"
API_KEY = "random generated test"
MODEL = "gemini-2.5-pro"

def test_api():
    """Test the OpenAI Compatible API server"""
    
    url = f"{BASE_URL}/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Hello! Please respond with 'API is working' if you receive this message."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    print(f"Testing API at: {BASE_URL}")
    print(f"Model: {MODEL}")
    print("-" * 50)
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ API Response:")
            print(json.dumps(result, indent=2))
            
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {}).get("content", "")
                print("-" * 50)
                print(f"✓ AI Response: {message}")
        else:
            print(f"✗ Error Response:")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("✗ Request timed out after 30 seconds")
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_api()
