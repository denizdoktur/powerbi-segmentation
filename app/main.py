from fastapi import FastAPI, Request
from router.router import router
from fastapi.middleware.cors import CORSMiddleware
import time

# FastAPI uygulamasını oluştur
app = FastAPI()

# CORS ayarları:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router modülündeki tüm endpointleri uygulamaya dahil et
app.include_router(router)

# Uygulama doğrudan bu dosyadan çalıştırıldığında (örneğin `python main.py`),
# Uvicorn sunucusunu başlat:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
