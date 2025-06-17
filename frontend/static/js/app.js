// Bu dosya hem sohbet asistanı (askQuestion, sendMessage) hem de fatura tabanlı ürün öneri
// (suggestInvoice) işlemlerini içerir. Nginx reverse-proxy sayesinde tüm istekler aynı origin’den yapılır.

// askQuestion: Kullanıcının sorusunu "/ask" endpoint’ine POST eder ve JSON yanıtını döner.
async function askQuestion(q) {
  const res = await fetch('/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: q })
  });
  return res.json();
}

// suggestInvoice: Verilen fatura numarasıyla "/suggest" endpoint’ine POST eder ve JSON yanıtını döner.
async function suggestInvoice(inv) {
  const res = await fetch('/suggest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fatura_no: inv })
  });
  return res.json();
}

// sendMessage: 
async function sendMessage() {
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-button');
  const icon = sendBtn.querySelector('i');
  const text = input.value.trim();
  if (!text) return;

  // 1) Kullanıcı mesajını ekle
  appendMessage('user', text);
  input.value = '';

  // 2) Gönder butonuna animasyon ekle
  icon.classList.add('sending');

  // 3) Bot düşünme mesajı ekle
  const botThinking = document.createElement('div');
  botThinking.className = 'chat-message bot';
  botThinking.id = 'thinking';
  botThinking.innerText = 'bi sn...';
  document.getElementById('chat-messages').appendChild(botThinking);
  scrollToBottom();

  try {
    // 4) API çağrısı
    const data = await askQuestion(text);
    const answer = data.answer || 'Yanıt alınamadı.';
    
    // Düşünüyor mesajını temizle
    const thinkEl = document.getElementById('thinking');
    thinkEl.innerText = '';
    thinkEl.removeAttribute('id');
    
    // 5) Yanıtı tipe tipe göster
    typeWriterEffect(answer, thinkEl);
  } catch (err) {
    // Hata durumunda bilgi göster
    const thinkEl = document.getElementById('thinking');
    thinkEl.innerText = '';
    thinkEl.removeAttribute('id');
    typeWriterEffect('Sunucuya bağlanılamadı.', thinkEl);
  } finally {
    // Animasyonu kaldır
    setTimeout(() => icon.classList.remove('sending'), 600);
  }
}

// appendMessage: Chat penceresine kullanıcı/assistant mesajı ekleyen yardımcı fonksiyon.
function appendMessage(role, msg) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-message ${role}`;
  msgDiv.innerText = msg;
  document.getElementById('chat-messages').appendChild(msgDiv);
  scrollToBottom();
}

// typeWriterEffect: Metni harf harf, yazı makinesi efektiyle gösterir.
function typeWriterEffect(text, element) {
  let i = 0;
  function typeChar() {
    if (i < text.length) {
      element.innerText += text.charAt(i);
      i++;
      scrollToBottom();
      setTimeout(typeChar, 20);
    }
  }
  typeChar();
}

// scrollToBottom: Chat içeriğini her zaman en alt öğe görünür olacak şekilde kaydırır.
function scrollToBottom() {
  const chatBody = document.getElementById('chat-messages');
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Fatura numarası seçildiğinde suggestInvoice çağrısı tetiklenir,
// dönen veriye göre sepet ve öneriler tabloları güncellenir.
document.getElementById("faturaNo").addEventListener("change", async function() {
  const faturaNo = this.value;
  try {
    const data = await suggestInvoice(faturaNo);

    // Sepet bilgilerini DOM’a yaz
    if (data?.sepet) {
      document.getElementById("urunSayisi").textContent = data.sepet.urun_sayisi;
      document.getElementById("toplamFiyat").textContent = `₺${data.sepet.toplam_fiyat}`;
      const urunler = data.sepet.urunler || [];
      const urunTableBody = document.getElementById("sepetUrunleriBody");
      urunTableBody.innerHTML = "";
      urunler.forEach(urun => {
        urunTableBody.innerHTML += `
          <tr>
            <td><strong>${urun.UrunAdi}</strong></td>
            <td>${urun.StokKodu}</td>
            <td><span class="price-tag">₺${urun.BirimFiyat}</span></td>
          </tr>`;
      });
    }

    // Cross-sell, Up-sell ve Kombine önerileri tablolarına yaz
    const tabloMap = {
      crosssell: "crossTableBody",
      upsell: "upTableBody",
      kombine: "comboTableBody"
    };
    Object.keys(tabloMap).forEach(key => {
      const tbody = document.getElementById(tabloMap[key]);
      tbody.innerHTML = "";
      const list = data?.oneriler?.[key] || [];
      list.forEach(urun => {
        tbody.innerHTML += `
          <tr>
            <td><strong>${urun.UrunAdi}</strong></td>
            <td>${urun.StokKodu}</td>
            <td>${urun.UrunTipi}</td>
            <td><span class="price-tag">₺${urun.BirimFiyat}</span></td>
          </tr>`;
      });
    });

  } catch (err) {
    alert("API hatası: " + err.message);
  }
});
