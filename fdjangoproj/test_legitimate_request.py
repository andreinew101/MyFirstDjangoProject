"""
Test legitimate browser request vs attack script
"""
import requests
import time

URL = "http://127.0.0.1:8000/item_list"

# Test 1: Request with proper browser headers (legitimate)
print("Test 1: Legitimate browser request with proper headers")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
}
response = requests.get(URL, headers=headers, timeout=5)
print(f"Status: {response.status_code}")

# Test 2: Request with missing headers (script-like)
print("\nTest 2: Script-like request with minimal headers")
headers_minimal = {
    'User-Agent': 'python-requests/2.28.1',  # DETECTED!
}
response = requests.get(URL, headers=headers_minimal, timeout=5)
print(f"Status: {response.status_code}")

# Test 3: Request with aiohttp (like your attack)
print("\nTest 3: Request with aiohttp signature")
headers_aiohttp = {
    'User-Agent': 'aiohttp/3.9.0',  # DETECTED!
}
response = requests.get(URL, headers=headers_aiohttp, timeout=5)
print(f"Status: {response.status_code}")

print("\n✅ Script detection working!")
