import json
import requests
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer

class CatalogLoader:
    def __init__(self):
        self.catalog_url = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"
        self.catalog = []
        self.vectorizer = None
        self.tfidf_matrix = None
        
    def load_catalog(self):
        """Load catalog from URL or local file"""
        # Try to download fresh copy
        try:
            print("📥 Downloading catalog...")
            response = requests.get(self.catalog_url, timeout=30)
            
            # Try to parse JSON with strict=False to handle control characters
            try:
                self.catalog = response.json()
                print(f"✅ Loaded {len(self.catalog)} items from URL")
                
                # Save clean copy
                with open('catalog.json', 'w', encoding='utf-8') as f:
                    json.dump(self.catalog, f, ensure_ascii=False)
                return self.catalog
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parse error: {e}")
                print("📝 Trying to clean the data...")
                
                # Try to clean the response text
                text = response.text
                # Replace control characters
                import re
                text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
                
                try:
                    self.catalog = json.loads(text)
                    print(f"✅ Loaded {len(self.catalog)} items after cleaning")
                    
                    # Save cleaned copy
                    with open('catalog.json', 'w', encoding='utf-8') as f:
                        json.dump(self.catalog, f, ensure_ascii=False)
                    return self.catalog
                except:
                    print("⚠️ Could not clean the data, trying local file...")
                    
        except Exception as e:
            print(f"⚠️ Error downloading: {e}")
            print("📂 Trying local catalog.json...")
        
        # Try local file
        if os.path.exists('catalog.json'):
            try:
                with open('catalog.json', 'r', encoding='utf-8') as f:
                    self.catalog = json.load(f)
                print(f"✅ Loaded {len(self.catalog)} items from local file")
                return self.catalog
            except Exception as e:
                print(f"⚠️ Error reading local file: {e}")
                print("📝 Trying to recover local file...")
                
                try:
                    with open('catalog.json', 'r', encoding='cp1252', errors='ignore') as f:
                        content = f.read()
                        # Clean control characters
                        import re
                        content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)
                        self.catalog = json.loads(content)
                    print(f"✅ Recovered {len(self.catalog)} items from local file")
                    return self.catalog
                except Exception as e2:
                    print(f"❌ Could not recover: {e2}")
        
        print("❌ No valid catalog found. Creating empty catalog...")
        self.catalog = []
        return self.catalog
    
    def build_index(self):
        """Build TF-IDF search index"""
        if not self.catalog:
            self.load_catalog()
        
        if not self.catalog:
            print("❌ No catalog items available!")
            return None
        
        print("🔨 Building search index with TF-IDF...")
        
        # Create text representations
        texts = []
        for item in self.catalog:
            if isinstance(item, dict):
                text = f"{item.get('name', '')} {item.get('description', '')} {' '.join(item.get('keys', []))}"
                texts.append(text)
        
        if not texts:
            print("❌ No valid text data found!")
            return None
        
        # Build TF-IDF matrix
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        print(f"✅ Index built with {len(self.catalog)} items")
        return self.tfidf_matrix
    
    def search(self, query, top_k=15):
        """Search using TF-IDF similarity"""
        if self.vectorizer is None or self.tfidf_matrix is None:
            self.load_catalog()
            self.build_index()
        
        if self.vectorizer is None or self.tfidf_matrix is None:
            return []
        
        # Transform query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity
        similarity = query_vector.dot(self.tfidf_matrix.T).toarray()[0]
        
        # Get top results
        top_indices = np.argsort(similarity)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarity[idx] > 0 and idx < len(self.catalog):
                results.append(self.catalog[idx])
        
        return results

if __name__ == "__main__":
    loader = CatalogLoader()
    loader.load_catalog()
    loader.build_index()
    
    # Test search
    results = loader.search("Java developer")
    print(f"\n🔍 Search results for 'Java developer':")
    for item in results[:3]:
        print(f"  - {item.get('name', 'Unknown')}")