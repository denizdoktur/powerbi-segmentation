# Müşteri Segmentasyonu Proje Açıklaması
 
Bu projede, e-ticaret şirketinin müşterileri analiz edilecek ve çeşitli müşteri segmentleri belirlenecektir. Proje boyunca veri ön işleme, RFM analizi, K-Means gibi kümeleme algoritmaları, veri görselleştirme ve interaktif dashboard geliştirme gibi pek çok adım gerçekleştirilecektir.
 
## Veri Seti Bilgisi
 
| Sütun Adı     | Açıklama                                                                 |
|---------------|--------------------------------------------------------------------------|
| FaturaNo      | Her işlemi benzersiz tanımlayan 6 haneli fatura numarası (`'C'` iptali belirtir) |
| StokKodu      | Ürün kodu                                                                |
| UrunAdi       | Ürün açıklaması                                                          |
| Miktar        | Satılan ürün adedi                                                       |
| FaturaTarihi  | Satışın gerçekleştiği tarih ve saat                                      |
| BirimFiyat    | Ürün fiyatı                                    						   |
| MusteriID     | Müşteri numarası                                                         |
| Sehir         | Müşterinin bulunduğu şehir                                               |
 
 
## Proje Hedefleri
 
1. Veri Ön İşleme
   - Eksik değerlerin analizi ve uygun şekilde ele alınması  
   - Fatura iptallerinin filtrelenmesi (`FaturaNo` içinde 'C' olanlar)  
   - Negatif `Miktar` ve `BirimFiyat` kayıtlarının temizlenmesi  
   - Gerekli feature engineering işlemleri  
 
2. RFM (Recency, Frequency, Monetary) Analizi
   - Müşterilerin satın alma davranışlarına göre puanlanması  
   - RFM skorlarının hesaplanması ve segmentlerin çıkarılması  
 
3. Kümeleme Algoritmaları (Clustering)
   - RFM skorlarına dayalı K-Means, Hierarchical Clustering gibi algoritmaların uygulanması  
   - Optimum küme sayısının belirlenmesi
   - Segmentlerin görselleştirilmesi  
 
4. Dashboard Geliştirme
   - Müşteri segmentlerinin ve özet metriklerin bulunduğu interaktif bir görsel rapor hazırlanması  
   - Tercihen Power BI, Tableau, Superset, Qlik veya Streamlit / Dash kullanılarak  
 
## Beklentiler
 
- Temizlenmiş ve analiz edilmiş veri seti  
- RFM analizi ile oluşturulmuş müşteri segmentleri  
- Uygulanan kümeleme algoritmaları ve çıktıları  
- Segmentlere dair görselleştirmeler  