import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from input.ncs_client import NCSClient

def test_ncs_client():
    print("Testing NCS Client...")
    # Initialize without key to test warning/dummy data or with key if env var is set
    client = NCSClient()
    
    # Test search (will fail if no key, but should handle gracefully if we implemented it right)
    # Actually my implementation prints error and returns empty dict.
    data = client.search_ncs(page=1, per_page=5)
    
    if data:
        print("API Call Successful (or Dummy Data returned if mocked)")
        print(data)
    else:
        print("API Call Failed or returned empty (Expected if no API Key)")
        
    # Test Dummy Data explicitly if needed, but the client doesn't expose it directly in search
    # unless we modify it. For now, just checking if it runs without crashing.

if __name__ == "__main__":
    test_ncs_client()
