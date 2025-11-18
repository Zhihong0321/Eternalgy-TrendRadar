import requests
import json

# API Configuration
API_URL = "https://api.bltcy.ai/v1/chat/completions"
API_KEY = "sk-jW4WLdgCGCshSyFY9VbKXwj8y2YXclFHxw2x2WbXElFkcAlD"
MODEL = "gpt-4o-mini-search-preview"

# Test prompt
PROMPT = "please do a web search and return malaysia solar pv news in october 2025, please return news link URL in arrary only. No descriptive words. Return maximum 10 link"

def test_websearch():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": PROMPT
            }
        ]
    }
    
    print("Testing API with web search capability...")
    print(f"API URL: {API_URL}")
    print(f"Model: {MODEL}")
    print(f"Prompt: {PROMPT}\n")
    print("-" * 80)
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        print(f"Status Code: {response.status_code}\n")
        
        if response.status_code == 200:
            result = response.json()
            print("Response JSON:")
            print(json.dumps(result, indent=2))
            print("\n" + "-" * 80)
            
            # Extract the assistant's message
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print("\nAssistant Response:")
                print(content)
                print("\n" + "-" * 80)
                
                # Check if response contains URLs
                if "http" in content.lower():
                    print("\n✓ Response contains URLs - Web search appears to be working!")
                else:
                    print("\n✗ No URLs found in response - Web search may not be enabled")
            
        else:
            print("Error Response:")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("Request timed out after 60 seconds")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_websearch()
