import httpx

API_URL = "http://localhost:8000/web/positions-json"

try:
    print(f"Fetching {API_URL}...")
    r = httpx.get(API_URL)
    print(f"Status Code: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Count: {len(data)}")
        print(f"First Item: {data[0] if data else 'None'}")
    else:
        print(f"Error: {r.text}")
except Exception as e:
    print(f"Exception: {e}")
