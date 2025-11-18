"""Search client for GPT-4o-mini-search-preview"""
import requests
import json
from typing import List, Optional
from .config import SEARCH_API_URL, SEARCH_API_KEY, SEARCH_MODEL, REQUEST_TIMEOUT


class SearchClient:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_url = SEARCH_API_URL
        self.api_key = api_key or SEARCH_API_KEY
        self.model = model or SEARCH_MODEL
    
    def search(self, prompt: str) -> Optional[List[str]]:
        """
        Execute search query and return list of URLs
        
        Args:
            prompt: Search prompt (should request URLs in array format)
        
        Returns:
            List of URLs or None if error
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Remove markdown code blocks if present
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]  # Remove ```json
                if content.startswith("```"):
                    content = content[3:]  # Remove ```
                if content.endswith("```"):
                    content = content[:-3]  # Remove trailing ```
                content = content.strip()
                
                # Parse JSON array from response
                urls = json.loads(content)
                
                if isinstance(urls, list):
                    return urls
                else:
                    print(f"Unexpected response format: {content}")
                    return None
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return None
                
        except json.JSONDecodeError as e:
            print(f"Failed to parse response as JSON: {e}")
            print(f"Response content: {response.text if 'response' in locals() else 'No response'}")
            return None
        except requests.exceptions.Timeout:
            print(f"Request timed out after {REQUEST_TIMEOUT} seconds")
            return None
        except Exception as e:
            print(f"Search error: {str(e)}")
            return None
    
    def get_usage_stats(self, response_data: dict) -> dict:
        """Extract token usage from API response"""
        if "usage" in response_data:
            usage = response_data["usage"]
            return {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
        return {}
