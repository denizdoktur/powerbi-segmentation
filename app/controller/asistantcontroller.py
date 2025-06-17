from fastapi import APIRouter, HTTPException, Request
from service.asistantservice import asistansSerive

class AsistantController:
    def __init__(self):
        # Router nesnesi oluştur ve "/ask" endpoint’ini POST metodu ile ekle
        self.router = APIRouter()
        self.router.add_api_route("/ask", self.ask, methods=["POST"])

    async def ask(self, request: Request):
        """
        İstemciden gelen JSON içindeki 'question' alanını alır,
        AsistantService ile soruyu işler ve JSON olarak cevap döner.
        Hata durumlarında uygun HTTPException fırlatır.
        """
        try:
            # Request gövdesini oku ve 'question' anahtarını al
            body = await request.json()
            question = body.get("question")

            # Eğer soru gönderilmemişse 400 Bad Request döndür
            if not question:
                raise HTTPException(status_code=400, detail="Soru girilmedi.")

            # AsistantService üzerinden yanıt üret
            result = asistansSerive.answer_question(question)

            # Service içinden hata gelmişse 500 döndür
            if "error" in result:
                raise HTTPException(status_code=500, detail=result["error"])

            # Başarılı yanıtı JSON olarak geri gönder
            return result

        except HTTPException:
            # HTTPException zaten uygun status kodu içerir; yeniden yükselt
            raise
        except Exception as e:
            # Beklenmeyen tüm hatalar için generic 500 hatası
            raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")

# Controller örneğini dışarı aktar, router.include_router ile kullanılsın
asistantController = AsistantController()
