from fastapi import APIRouter, HTTPException, Request
from service.suggestservice import suggestService

class SuggestController:
    def __init__(self):
        # APIRouter örneğini oluştur ve "/suggest" endpoint’ini POST metodu ile tanımla
        self.router = APIRouter()
        self.router.add_api_route("/suggest", self.suggest, methods=["POST"])

    async def suggest(self, request: Request):
        """
        İstemciden gelen JSON içindeki 'fatura_no' alanını alır,
        SuggestService.get_recommendation_by_invoice ile öneri üretir,
        ve JSON olarak döner. Hata durumlarında uygun HTTPException fırlatır.
        """
        try:
            # İstek gövdesini JSON olarak oku
            body = await request.json()
            fatura_no = body.get("fatura_no")

            # Fatura numarası gönderilmemişse 400 Bad Request dön
            if not fatura_no:
                raise HTTPException(status_code=400, detail="Fatura numarası girilmedi.")

            # Servisi çağırıp öneri sonucunu al
            result = suggestService.get_recommendation_by_invoice(fatura_no)

            # Service içinden hata gelmişse 404 Not Found dön
            if "error" in result:
                raise HTTPException(status_code=404, detail=result["error"])

            # Başarılı öneri bilgisini JSON olarak geri gönder
            return result

        except HTTPException:
            # HTTPException zaten doğru status kodunu içerir, tekrar fırlat
            raise
        except Exception as e:
            # Beklenmeyen hatalar için generic 500 Internal Server Error dön
            raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")

# Controller örneğini dışarı aktar; main.py içinde router.include_router ile kullanılacak
suggestController = SuggestController()
