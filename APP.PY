import pkgutil
import funcionalidades
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn

# 1. Limiter Global (Proteção contra Brute Force e DoS)
limiter = Limiter(key_func=get_remote_address)
seguranca.py
app = FastAPI(title="GeralJá API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Segurança CORS (Ajustado para produção de alto tráfego)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://suavitrine.com.br"], # Restrito ao seu domínio
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 3. Auto-descoberta de Funcionalidades (O Maestro que não precisa de manutenção)
for loader, module_name, is_pkg in pkgutil.iter_modules(funcionalidades.__path__):
    module = importlib.import_module(f"funcionalidades.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router, prefix=f"/{module_name}")

@app.get("/health")
async def health_check():
    """Monitoramento de status para o Cloudflare saber que o site está vivo"""
    return {"status": "online", "performance": "optimal"}
