import requests
import json

# Test health
print("🔍 Testing health endpoint...")
response = requests.get("http://localhost:8000/health")
print(f"Health: {response.json()}")

# Test chat
print("\n💬 Testing chat endpoint...")
response = requests.post(
    "http://localhost:8000/chat",
    json={"messages": [{"role": "user", "content": "I need to hire a Java developer with 5 years experience"}]}
)

if response.status_code == 200:
    data = response.json()
    print(f"Reply: {data['reply'][:200]}...")
    print(f"Recommendations: {len(data.get('recommendations', []))}")
    if data.get('recommendations'):
        print("\n📋 Recommendations:")
        for rec in data['recommendations'][:3]:
            print(f"  - {rec['name']} ({rec['test_type']})")
else:
    print(f"Error: {response.status_code}")
    print(response.text)