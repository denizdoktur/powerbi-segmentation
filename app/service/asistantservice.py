import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_experimental.agents import create_csv_agent
from langchain_community.chat_models import ChatOpenAI
import traceback
from langchain.memory import ConversationBufferMemory
from service.chat_db import init_db, insert_message

class AsistantService:
    @staticmethod
    def answer_question(question: str):
        """
        Kullanıcının sorduğu soruyu alır, CSV veri kümesi üzerinde bir LLM agent
        ile çalıştırır, sonucu veritabanına kaydeder ve yanıtı döner.
        Hata durumunda bir 'error' anahtarına sahip dict ile döner.
        """
        try:
            # Ortam değişkenlerini .env dosyasından yükle
            load_dotenv()

            # Chat geçmişi için SQLite veritabanını hazırla
            init_db()

            # CSV dosyasının yolunu belirle
            csv_file_path = Path(__file__).resolve().parent.parent / "data/df.csv"
            # Eğer CSV bulunamazsa hata mesajı döndür
            if not csv_file_path.exists():
                return {"error": f"CSV dosyası bulunamadı: {csv_file_path}"}

            # Agent için konuşma belleği (memory) oluştur
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

            # CSV agentı oluştur:
            agent = create_csv_agent(
                llm=ChatOpenAI(temperature=0.2),
                path=str(csv_file_path),
                verbose=False,
                memory=memory,
                handle_parsing_errors=True,
                allow_dangerous_code=True,
            )

            # Agentı çalıştırarak soruyu sor ve yanıtını al
            response = agent.run(question)

            # Soru ve yanıtı veritabanına kaydet
            insert_message(question, response)

            # Başarılı sonucu JSON formatında döndür
            return {"question": question, "answer": response}

        except Exception as e:
            # Hata durumunda hata mesajını konsola yaz ve stack-trace bas
            print("AsistantService hata:", str(e))
            traceback.print_exc()
            # Kullanıcıya dönecek hata formatı
            return {"error": str(e)}

# Servis örneğini dışarıya aktar
asistansSerive = AsistantService()
