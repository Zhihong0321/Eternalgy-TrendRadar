"""Test date extraction from a sample article"""
from ai_processing.services.ai_client import AIClient
from ai_processing.config import AIConfig

# Sample article with clear date
sample_content = """
Samaiden Group Berhad announce that its wholly-owned subsidiary has been shortlisted 
by the Energy Commission for the development of a 99.99 Megawatts Large Scale Solar 
Photovoltaic Plant in Pasir Mas, Kelantan. The letter of notification it said was 
issued on 23 December 2024, formally acknowledging the selection.
"""

config = AIConfig()
client = AIClient(
    api_url=config.api_url,
    api_key=config.api_key,
    model=config.model,
    timeout=config.timeout
)

prompt = f"""You are a professional news editor for a clean, ad-free news portal.

Article Content:
{sample_content}

Your tasks:
1. Remove ALL ads, promotional content, filler text, clickbait, and irrelevant information
2. Extract ONLY the core facts and news information
3. Create 3-5 clean bullet points, each with ONE clear factual statement
4. Select up to 3 most relevant tags from: Solar, Wind, EV, Big Project, Tech, Policy, Finance, Storage
5. Identify the origin country (2-letter code: MY, SG, CN, US, TH, ID, PH, etc.)
6. Extract the news date from the article (YYYY-MM-DD format). Look for dates in the content like "23 December 2024" and convert to "2024-12-23".
7. Maintain the original language

Return in this EXACT format:
TAGS: [tag1, tag2, tag3]
COUNTRY: [XX]
NEWS_DATE: [YYYY-MM-DD]
BULLETS:
• [First key fact]
• [Second key fact]
• [Third key fact]

Focus on facts only. No fluff, no repetition, no promotional language."""

messages = [
    {"role": "system", "content": "You are a professional news editor."},
    {"role": "user", "content": prompt}
]

print("Testing date extraction with gpt-5-nano...")
print("=" * 80)

response = client.chat_completion(messages=messages, temperature=0.3, max_tokens=500)
content = client.extract_content(response)

print("AI Response:")
print(content)
print("\n" + "=" * 80)

# Parse the response
lines = content.strip().split('\n')
for line in lines:
    line = line.strip()
    if line.startswith('NEWS_DATE:') or line.startswith('DATE:'):
        date_str = line.replace('NEWS_DATE:', '').replace('DATE:', '').strip().strip('[]')
        print(f"\nExtracted Date: {date_str}")
        break
else:
    print("\nNo date found in response")
