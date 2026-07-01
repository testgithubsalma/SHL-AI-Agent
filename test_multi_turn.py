import requests
import json

print("💬 Testing multi-turn conversation...")

messages = []

# Turn 1: User
messages.append({"role": "user", "content": "I need to hire a Java developer"})
response = requests.post("http://localhost:8000/chat", json={"messages": messages})
if response.status_code == 200:
    data = response.json()
    print(f"\n🤖 Turn 1 Agent: {data['reply'][:100]}...")
    messages.append({"role": "assistant", "content": data['reply']})

# Turn 2: User provides more info
messages.append({"role": "user", "content": "It's a senior role with 5+ years experience, they need Spring Boot and AWS"})
response = requests.post("http://localhost:8000/chat", json={"messages": messages})
if response.status_code == 200:
    data = response.json()
    print(f"\n🤖 Turn 2 Agent: {data['reply'][:100]}...")
    messages.append({"role": "assistant", "content": data['reply']})
    print(f"\n📋 Recommendations: {len(data.get('recommendations', []))}")
    for rec in data.get('recommendations', [])[:3]:
        print(f"  - {rec['name']}")

# Turn 3: User confirms
messages.append({"role": "user", "content": "That's perfect, thanks!"})
response = requests.post("http://localhost:8000/chat", json={"messages": messages})
if response.status_code == 200:
    data = response.json()
    print(f"\n🤖 Turn 3 Agent: {data['reply'][:100]}...")
    print(f"End of conversation: {data.get('end_of_conversation', False)}")