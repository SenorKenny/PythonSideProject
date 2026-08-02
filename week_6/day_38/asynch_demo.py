import requests
import time
import asyncio
import curl_cffi


async def together(url):
    responses=[]
    async with curl_cffi.AsyncSession() as session:
        responses= [session.get(url) for i in range(4)]
        results=await asyncio.gather(*responses)
        i=0
        for result in results:
                print(f'response {i+1} has status code of {results.status_code}')
                i+=1
  
url="https://httpbin.org/delay/2"    
start=time.perf_counter()
asyncio.run(together(url))
end=time.perf_counter()
total=end-start
print(f'total time was {total:.2f} seconds')
"""
response1=requests.get("https://tls.peet.ws/api/all")
response2=curl_cffi.requests.get("https://tls.peet.ws/api/all")

print(response1.text)
print("\n" + "="*40 + "\n")
print("\n" + "="*40 + "\n")
print(response2.text)"""