import httpx 
import base64

JUDGE0_URL = "http://localhost:2358/submissions/?wait=true&base64_encoded=true"
def b64(s :str)->str:
    return base64.b64encode(s.encode()).decode()

async def run_code(source_code: str, language_id : int, stdin: str):
    payload = {
        "source_code": b64(source_code),
        "language_id": language_id,
        "stdin": b64(stdin),
        "cpu_time_limit": 1.0,      # 1 second time limit
        "memory_limit": 512000,     # 512 MB in kilobytes (512 * 1000)
    }

    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.post(
            JUDGE0_URL,
            json=payload
        )
        return res.json()