import zipfile
import os

def extract_conversations():
    """Extract the conversations zip file"""
    # Look for the zip file
    possible_locations = [
        r"C:\Users\Asus\Downloads\sample_conversations.zip",
        r"C:\Users\Asus\Downloads\sample_conversations (3).zip",
        r"C:\Users\Asus\Desktop\sample_conversations.zip",
        r"C:\Users\Asus\Desktop\sample_conversations (3).zip",
    ]
    
    zip_path = None
    for loc in possible_locations:
        if os.path.exists(loc):
            zip_path = loc
            break
    
    if not zip_path:
        print("❌ Could not find conversations.zip")
        print("Please specify the path:")
        custom_path = input("Path: ").strip()
        if os.path.exists(custom_path):
            zip_path = custom_path
        else:
            print("❌ File not found")
            return
    
    # Extract
    extract_to = r"C:\Users\Asus\Desktop\shl-assessment-agent\data\conversations"
    os.makedirs(extract_to, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"✅ Extracted to: {extract_to}")
        
        # Show what was extracted
        print("\n📁 Extracted files:")
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                if file.endswith('.md'):
                    print(f"  - {file}")

if __name__ == "__main__":
    extract_conversations()