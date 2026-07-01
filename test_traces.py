import os
import re
import json
import requests

def parse_traces():
    """Parse all conversation traces from markdown files"""
    traces_folder = r"C:\Users\Asus\Desktop\shl-assessment-agent\data\conversations\GenAI_SampleConversations"
    
    if not os.path.exists(traces_folder):
        print(f"❌ Folder not found: {traces_folder}")
        return []
    
    traces = []
    
    for filename in sorted(os.listdir(traces_folder)):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(traces_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract conversation turns
        turns = re.findall(
            r'### Turn (\d+)\s*\n\*\*User\*\*\s*\n> (.*?)\n\*\*Agent\*\*\s*\n(.*?)(?=\n### Turn|\n_`end_of_conversation`|$)',
            content,
            re.DOTALL
        )
        
        trace = {'filename': filename, 'conversation': [], 'expected': []}
        
        for turn_num, user_msg, agent_msg in turns:
            # Extract recommendations from this turn
            recs = []
            if '| # | Name' in agent_msg and '|---' in agent_msg:
                rows = re.findall(
                    r'\|\s*\d+\s*\|\s*(.*?)\s*\|\s*([A-Z, ]+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|',
                    agent_msg
                )
                for row in rows:
                    if len(row) >= 6 and row[0].strip():
                        recs.append(row[0].strip())
            
            trace['conversation'].append({
                'turn': int(turn_num),
                'user': user_msg.strip(),
                'agent': agent_msg.strip(),
                'recommendations': recs
            })
        
        # Get expected shortlist from final recommendations
        if trace['conversation']:
            trace['expected'] = trace['conversation'][-1].get('recommendations', [])
        
        traces.append(trace)
        print(f"✅ Parsed {filename}: {len(trace['conversation'])} turns, {len(trace['expected'])} expected")
    
    return traces

def test_agent(base_url="http://localhost:8000"):
    """Test agent against all traces"""
    print("\n" + "="*60)
    print("🧪 Testing Agent with Conversation Traces")
    print("="*60)
    
    traces = parse_traces()
    if not traces:
        return
    
    results = []
    
    for trace in traces:
        print(f"\n📝 Testing: {trace['filename']}")
        print("-"*40)
        
        messages = []
        trace_results = {'recalls': []}
        
        for turn in trace['conversation']:
            messages.append({'role': 'user', 'content': turn['user']})
            
            try:
                response = requests.post(
                    f"{base_url}/chat",
                    json={'messages': messages},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    rec_names = [r['name'] for r in data.get('recommendations', [])]
                    
                    # Calculate recall if we have expected
                    expected = turn['recommendations']
                    if expected and rec_names:
                        hits = set(rec_names) & set(expected)
                        recall = len(hits) / len(expected) if expected else 0
                        trace_results['recalls'].append(recall)
                        print(f"  Turn {turn['turn']}: Recall = {recall:.2%}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Average recall for this trace
        if trace_results['recalls']:
            avg_recall = sum(trace_results['recalls']) / len(trace_results['recalls'])
            results.append(avg_recall)
            print(f"  📊 Average Recall: {avg_recall:.2%}")
        else:
            print("  ⚠️ No recall data")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    if results:
        print(f"✅ Traces tested: {len(results)}")
        print(f"✅ Overall Average Recall: {sum(results)/len(results):.2%}")
        print(f"✅ Pass rate (>50%): {sum(1 for r in results if r > 0.5)}/{len(results)}")
    else:
        print("❌ No results")

if __name__ == "__main__":
    # Check if agent is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Agent is running!")
            test_agent()
        else:
            print("❌ Agent not responding")
    except:
        print("❌ Agent not running. Start it first with: python main.py")