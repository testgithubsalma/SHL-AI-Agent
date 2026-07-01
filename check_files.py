import os

def check_structure():
    """Verify the folder structure"""
    base = r"C:\Users\Asus\Desktop\shl-assessment-agent"
    
    print("📂 Checking folder structure...")
    print("="*50)
    
    # Check main files
    files_to_check = [
        'main.py', 'agent.py', 'catalog_loader.py', 
        'test_traces.py', 'requirements.txt'
    ]
    
    all_ok = True
    for file in files_to_check:
        path = os.path.join(base, file)
        if os.path.exists(path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_ok = False
    
    # Check traces
    traces_folder = os.path.join(base, "data", "conversations", "GenAI_SampleConversations")
    if os.path.exists(traces_folder):
        md_files = [f for f in os.listdir(traces_folder) if f.endswith('.md')]
        print(f"\n✅ Traces folder found with {len(md_files)} markdown files")
        for file in sorted(md_files)[:5]:
            print(f"   - {file}")
        if len(md_files) > 5:
            print(f"   ... and {len(md_files)-5} more")
    else:
        print("\n❌ Traces folder not found!")
        print("   Expected: data/conversations/GenAI_SampleConversations/")
    
    print("\n" + "="*50)
    if all_ok:
        print("✅ All files are in place!")
        print("\nNext steps:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Run: python main.py")
        print("3. In another terminal: python test_traces.py")
    else:
        print("⚠️ Some files are missing. Please create them.")

if __name__ == "__main__":
    check_structure()