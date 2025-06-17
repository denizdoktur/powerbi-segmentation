import pandas as pd
import os
import pickle
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

class SuggestService:
    def get_recommendation_by_invoice(self, fatura_no: str, model_dir="model/basket_models_backup/model_20250531_074105"):
        """
        Verilen fatura numarasına göre cross-sell, up-sell ve kombine öneriler döner.
        - fatura_no: İncelenecek fatura numarası
        - model_dir: Öneri modellerinin bulunduğu dizin
        """
        try:
            # CSV verisini oku
            df = pd.read_csv("data/df.csv", encoding="utf-8")
            # İlgili faturaya ait verileri filtrele
            basket_data = df[df['FaturaNo'] == fatura_no]
            if basket_data.empty:
                # Fatura bulunamazsa hata bilgisi ve örnek numaralar dön
                return {
                    'error': f'Fatura {fatura_no} bulunamadı',
                    'available_invoices': df['FaturaNo'].head(10).tolist()
                }

            # Sepet kalem kodlarını ve detay bilgisini al
            basket_items = basket_data['StokKodu'].tolist()
            basket_info = basket_data[['StokKodu', 'UrunAdi', 'BirimFiyat']].drop_duplicates()

            # Model ve yardımcı nesneleri başlat
            lightfm_model = None
            dataset = None
            item_encoder = None
            lgb_model = None
            popular_items = []

            # LightFM modeli ve item encoder yükleme denemesi
            try:
                with open(os.path.join(model_dir, 'lightfm_model.pkl'), 'rb') as f:
                    lightfm_model = pickle.load(f)
                with open(os.path.join(model_dir, 'dataset.pkl'), 'rb') as f:
                    dataset = pickle.load(f)
                item_encoder = joblib.load(os.path.join(model_dir, 'item_encoder.pkl'))
            except:
                # Yükleme hatalarında sessizce geç
                pass

            # LightGBM modeli yükleme denemesi
            try:
                lgb_model = joblib.load(os.path.join(model_dir, 'lgb_model.pkl'))
            except:
                pass

            # Popüler ürünler bileşenini yükleme veya CSV'den hazırla
            try:
                with open(os.path.join(model_dir, 'components.pkl'), 'rb') as f:
                    components = pickle.load(f)
                    popular_items = components['popular_items']
            except:
                popular_items = df['StokKodu'].value_counts().head(10).index.tolist()

            # Cross-sell öneri listesi
            crosssell = []
            if lightfm_model and item_encoder is not None:
                try:
                    all_items = item_encoder.classes_
                    # Sepet dışı kalemleri filtrele
                    item_indices = [np.where(all_items == item)[0][0] for item in basket_items if item in all_items]

                    if item_indices:
                        # LightFM ile skorları hesapla
                        scores = lightfm_model.predict(0, np.arange(len(all_items)))
                        mask = np.ones(len(all_items), dtype=bool)
                        mask[item_indices] = False
                        filtered_scores = scores * mask
                        top_indices = np.argsort(filtered_scores)[::-1][:20]
                        candidate_items = [all_items[i] for i in top_indices]

                        # Eğer LightGBM varsa skorlama ile rafine et
                        if lgb_model is not None:
                            scored_items = []
                            for candidate in candidate_items:
                                candidate_scores = []
                                for basket_item in basket_items:
                                    try:
                                        item1 = df[df['StokKodu'] == basket_item]
                                        item2 = df[df['StokKodu'] == candidate]
                                        if not item1.empty and not item2.empty:
                                            features = np.array([[
                                                item1['BirimFiyat'].iloc[0],
                                                item2['BirimFiyat'].iloc[0],
                                                len(basket_items)
                                            ]])
                                            score = lgb_model.predict_proba(features)[0][1]
                                            candidate_scores.append(score)
                                    except:
                                        continue
                                if candidate_scores:
                                    avg_score = np.mean(candidate_scores)
                                    scored_items.append((candidate, avg_score))
                            # Skorlanan ürünleri sıralayıp al
                            if scored_items:
                                scored_items.sort(key=lambda x: x[1], reverse=True)
                                crosssell = [item for item, _ in scored_items[:10]]
                            else:
                                crosssell = candidate_items[:10]
                        else:
                            crosssell = candidate_items[:10]
                except:
                    pass

            # Eğer LightFM yoksa popüler ürünlerden öneri
            if not crosssell:
                crosssell = [item for item in popular_items[:5] if item not in basket_items]

            # Up-sell öneri listesi
            upsell = []
            try:
                for item in basket_items:
                    row = df[df['StokKodu'] == item]
                    if not row.empty:
                        t = row['UrunTipi'].iloc[0]
                        p = row['BirimFiyat'].iloc[0]
                        higher = df[(df['UrunTipi'] == t) & (df['BirimFiyat'] > p * 1.2) & (~df['StokKodu'].isin(basket_items))]
                        top3 = higher['StokKodu'].value_counts().head(3)
                        upsell.extend(top3.index.tolist())
                upsell = list(set(upsell))[:5]
            except:
                pass

            # Cross ve up listesinde çakışanları temizle
            upsell = [i for i in upsell if i not in crosssell]

            # Ürün kodlarından detay bilgisi almak için yardımcı fonksiyon
            def get_product_info(codes):
                if not codes:
                    return []
                subset = df[df['StokKodu'].isin(codes)][['StokKodu','UrunAdi','BirimFiyat','UrunTipi']]
                return subset.drop_duplicates('StokKodu').sort_values('BirimFiyat', ascending=False).to_dict('records')

            # Sonuç sözlüğü oluştur
            result = {
                'fatura_no': fatura_no,
                'sepet': {
                    'urun_sayisi': len(basket_items),
                    'toplam_fiyat': float(basket_info['BirimFiyat'].sum()),
                    'urunler': basket_info.to_dict('records')
                },
                'oneriler': {
                    'crosssell': get_product_info(crosssell),
                    'upsell': get_product_info(upsell),
                    'kombine': get_product_info(list(set(crosssell+upsell))[:8])
                },
                'model_status': {
                    'lightfm_loaded': lightfm_model is not None,
                    'lightgbm_loaded': lgb_model is not None,
                    'hybrid_mode': lightfm_model is not None and lgb_model is not None
                }
            }

            return result

        except Exception as e:
            # Beklenmeyen hataları error formatında döndür
            return {'error': f'Test hatası: {str(e)}'}

# Servis örneğini dışarıya aktar
suggestService = SuggestService()
