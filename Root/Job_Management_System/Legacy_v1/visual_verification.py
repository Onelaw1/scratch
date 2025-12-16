import webbrowser
import uvicorn
import threading
import time
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_server():
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, log_level="info")

def verify_frontend():
    print("Starting Server for Visual Verification...")
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    print("Opening Browser...")
    # Open Dashboard
    webbrowser.open("http://127.0.0.1:8000/web/")
    
    print("\n[INSTRUCTION] Please verify the following pages in your browser:")
    print("1. Dashboard: http://127.0.0.1:8000/web/")
    print("2. Performance Review: http://127.0.0.1:8000/web/performance-review")
    print("3. Training Management: http://127.0.0.1:8000/web/training-management")
    
    input("\nPress Enter to stop the server and finish verification...")

if __name__ == "__main__":
    verify_frontend()
