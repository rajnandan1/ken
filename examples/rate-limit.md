# Rate Limiting

**Task:** "Add rate limiting to my FastAPI endpoint so users can't spam it."

Verbatim model output from a benchmark run — Claude Haiku 4.5, no-skill arm vs ken arm, temperature 1, source `benchmarks/output.json`. Reproduce: `npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml`.

## Without Ken — 117 lines of code

# Rate Limiting for FastAPI

Here are several approaches, from simplest to most robust:

## 1. **Using `slowapi` (Recommended - Easiest)**

```bash
pip install slowapi
```

```python
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429,
    content={"detail": "Rate limit exceeded"}
))

@app.get("/api/data")
@limiter.limit("5/minute")  # 5 requests per minute
async def get_data():
    return {"message": "Here's your data"}
```

### More Examples:
```python
@limiter.limit("10/hour")      # 10 per hour
@limiter.limit("100/day")      # 100 per day
@limiter.limit("1/second")     # 1 per second
```

---

## 2. **Per-User Rate Limiting**

```python
from fastapi import FastAPI, Depends, Header
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

async def get_api_key(x_api_key: str = Header(...)) -> str:
    return x_api_key

@app.get("/api/data")
@limiter.limit("100/hour")
async def get_data(api_key: str = Depends(get_api_key)):
    return {"message": "Data for user"}
```

---

## 3. **Custom Rate Limiting with `aiolimiter`**

```bash
pip install aiolimiter
```

```python
from fastapi import FastAPI, HTTPException
from aiolimiter import AsyncLimiter
from contextlib import asynccontextmanager
import time

# 10 requests per 60 seconds
limiter = AsyncLimiter(max_rate=10, time_period=60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/api/data")
async def get_data():
    try:
        await asyncio.wait_for(limiter.acquire(), timeout=1)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=429, detail="Rate limited")
    
    return {"message": "Here's your data"}
```

---

## 4. **Advanced: Redis-Based Rate Limiting**

For distributed systems with multiple workers:

```bash
pip install redis aiolimiter
```

```python
from fastapi import FastAPI, Request, HTTPException
from redis import asyncio as aioredis
import time

app = FastAPI()
redis_client = None

@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = await aioredis.from_url("redis://localhost")

@app.on_event("shutdown")
async def shutdown():
    await redis_client.close()

async def rate_limit_check(request: Request, max_requests: int = 10, window: int = 60):
    client_id = request.client.host
    key = f"rate_limit:{client_id}"
    
    current = await redis_client.incr(key)
    if current == 1:
        await redis_client.expire(key, window)
    
    if current > max_requests:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

@app.get("/api/data")
async def get_data(request: Request):
    await rate_limit_check(request, max_requests=10, window=60)
    return {"message": "Here's your data"}
```

---

## 5. **Middleware Approach (Global Rate Limiting)**

```python
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from time import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests=100, window=60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host
        now = time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            return HTTPException(status_code=429, detail="Rate limited")
        
        self.requests[client_id].append(now)
        return await call_next(request)

app = FastAPI()
app.add_middleware(RateLimitMiddleware, max_requests=100, window=60)

@app.get("/api/data")
async def get_data():
    return {"message": "Here's your data"}
```

---

## Comparison Table

| Method | Pros | Cons |
|--------|------|------|
| **slowapi** | Easy, well-documented, decorator-based | Memory-based, not distributed |
| **aiolimiter** | Simple, async-native | Memory-based |
| **Redis** | Distributed, scalable | Requires Redis setup |
| **Middleware** | Customizable, global | More verbose |

---

## My Recommendation

**Use `slowapi`** for most cases:

```python
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )
)

@app.get("/api/data")
@limiter.limit("5/minute")
async def get_data():
    return {"data": "value"}
```

This is production-ready and handles most use cases! 🚀

## With Ken — 50 lines of code

# Think first

What's the real constraint? Users hammering one endpoint floods it. Rate limiting needs: (1) a request counter keyed by user or IP, (2) a time window, (3) rejection when over limit. FastAPI has no built-in; the stdlib has nothing. A dependency exists (`slowapi`) but it wraps `limits` — I'd rather use `limits` direct or roll ten lines.

The minimal truths: track hits per key in a dict, clear old window entries, reject on breach. One dict, one timestamp check per request. Brute force until you hit scale.

---

## Code

```python
from fastapi import FastAPI, HTTPException, Request
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

app = FastAPI()

# State: {key: [(timestamp, count_in_window), ...]}
rate_limit_state = defaultdict(list)
WINDOW_SECONDS = 60
MAX_REQUESTS = 10
CLEANUP_INTERVAL = 300  # seconds

def get_client_key(request: Request) -> str:
    """Extract client identifier: forwarded IP or remote."""
    return request.headers.get("x-forwarded-for", request.client.host)

def cleanup_old_entries():
    """Prune entries older than window. Run periodically."""
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=WINDOW_SECONDS)
    for key in list(rate_limit_state.keys()):
        rate_limit_state[key] = [
            (ts, count) for ts, count in rate_limit_state[key]
            if ts > cutoff
        ]
        if not rate_limit_state[key]:
            del rate_limit_state[key]

async def rate_limit_check(request: Request) -> bool:
    """Return True if request allowed, False if over limit."""
    cleanup_old_entries()
    
    key = get_client_key(request)
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=WINDOW_SECONDS)
    
    # Prune old entries for this key
    rate_limit_state[key] = [
        (ts, count) for ts, count in rate_limit_state[key]
        if ts > cutoff
    ]
    
    # Sum requests in current window
    request_count = sum(count for ts, count in rate_limit_state[key])
    
    if request_count >= MAX_REQUESTS:
        return False
    
    # Add this request
    if rate_limit_state[key]:
        rate_limit_state[key][0] = (rate_limit_state[key][0][0], request_count + 1)
    else:
        rate_limit_state[key].append((now, 1))
    
    return True

@app.get("/api/endpoint")
async def my_endpoint(request: Request):
    """Example endpoint with rate limiting."""
    if not await rate_limit_check(request):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: 10 requests per 60 seconds"
        )
    
    return {"status": "ok", "message": "Request succeeded"}
```

---

## Notes

→ **Stole:** The per-IP tracking idea from classic HTTP middleware patterns.  
→ **Threw away:** The dependency. `slowapi` + `limits` add config boilerplate and a layer.  
→ **Ceiling:** `// ken: dict + linear scan; redis or token-bucket when > 1000 unique IPs measured under load`. This brute-force dict works fine up to a few thousand keys; swap to Redis or an in-memory token bucket once measurement says scaling is real.

---

**To use:** Decorate your endpoint with the check, or wrap it in middleware to apply to all routes. The state lives in memory — survives per-process only. For multi-worker deployment, move state to Redis or an external service (that's the upgrade trigger).

**117 → 50 lines of code** — same model, same prompt.
