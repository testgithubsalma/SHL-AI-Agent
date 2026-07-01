import os
import re
import requests

print("🧪 Testing traces (simple version)...")
print("="*50)

traces_folder = r"C:\Users\Asus\Desktop\shl-assessment-agent\data\conversations\GenAI_SampleConversations"

if not os.path.exists(traces_folder):
    print(f"❌ Traces folder not found: {traces_folder}")
    exit()

for filename in sorted(os.listdir(traces_folder)):
    if not filename.endswith('.md'):
        continue
    
    print(f"\n📝 Testing: {filename}")
    
    # Read the file
    with open(os.path.join(traces_folder, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract user messages
    user_messages = re.findall(r'\*\*User\*\*\s*\n> (.*?)\n', content)
    
    messages = []
    for user_msg in user_messages[:3]:  # Test first 3 turns
        messages.append({"role": "user", "content": user_msg.strip()})
        
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"messages": messages},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  User: {user_msg[:50]}...")
                print(f"  Agent: {data['reply'][:50]}...")
                print(f"  Recs: {len(data.get('recommendations', []))}")
            else:
                print(f"  ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")