import aiohttp
import asyncio
import time

URL = "http://127.0.0.1:8000/item_list"
TOTAL_REQUESTS = 10000 # Massive amount of requests
CONCURRENCY_LIMIT = 3000  # Number of open connections at once

async def send_request(session, semaphore):
    # The semaphore limits how many requests are active at once 
    # so you don't run out of file descriptors/ports on your OS
    async with semaphore:
        try:
            async with session.get(URL) as response:
                await response.read() # Ensure we download the body
                if response.status != 200:
                     print(f"Status: {response.status}")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    # One session for all requests (Keep-Alive optimization)
    # Using a customized TCPConnector to allow high concurrency
    connector = aiohttp.TCPConnector(limit=None)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        print(f"Preparing {TOTAL_REQUESTS} async requests...")
        
        for _ in range(TOTAL_REQUESTS):
            tasks.append(send_request(session, semaphore))
            
        print("Firing requests...")
        start_time = time.time()
        
        # Run all requests
        await asyncio.gather(*tasks)
        
        duration = time.time() - start_time
        print(f"Completed {TOTAL_REQUESTS} requests in {duration:.2f} seconds")
        print(f"Requests Per Second: {TOTAL_REQUESTS / duration:.2f}")

if __name__ == "__main__":
    # Windows users might need to change the event loop policy
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())