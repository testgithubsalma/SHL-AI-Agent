import requests
import json

# Test with specific query
print("💬 Testing with specific query...")
response = requests.post(
    "http://localhost:8000/chat",
    json={"messages": [
        {"role": "user", "content": "I'm hiring a senior Java developer with 5+ years experience, Spring Boot, and AWS"}
    ]}
)

if response.status_code == 200:
    data = response.json()
    print(f"\n🤖 Agent Reply:\n{data['reply']}")
    print(f"\n📋 Recommendations: {len(data.get('recommendations', []))}")
    for rec in data.get('recommendations', [])[:5]:
        print(f"  - {rec['name']} ({rec['test_type']})")
else:
    print(f"Error: {response.status_code}")