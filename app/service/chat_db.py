import sqlite3
from pathlib import Path

# Veri tabanı dosyasının yolu (uygulama kök dizininde chat_history.db)
DB_PATH = Path("chat_history.db")

def init_db():
    """
    SQLite veritabanını başlatır.  
    Eğer 'chat_log' tablosu yoksa, gerekli sütunlarla birlikte oluşturur.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_message(question, answer):
    """
    Yeni bir sohbet kaydı ekler.  
    question ve answer parametreleri ile chat_log tablosuna satır ekler.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_log (question, answer) VALUES (?, ?)",
        (question, answer)
    )
    conn.commit()
    conn.close()

def fetch_all_messages():
    """
    Tüm sohbet geçmişini getirir.  
    chat_log tablosundaki tüm kayıtları ID sırasına göre döndürür.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT question, answer FROM chat_log ORDER BY id ASC"
    )
    messages = c.fetchall()
    conn.close()
    return messages

def clear_all_messages():
    """
    Sohbet geçmişini temizler.  
    chat_log tablosundaki tüm satırları siler.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM chat_log")
    conn.commit()
    conn.close()
